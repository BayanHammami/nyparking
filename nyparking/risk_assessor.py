# from nyparking import app

from nyparking import app
import psycopg2
from flask import g

import math, datetime
from datetime import time, datetime

from nyparking.db_manager import get_db_cursor

# cursor = conn.cursor()

earth_radius = 6371000 # metres!

# # for verifying input
def accepts(*types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount
        def new_f(*args, **kwds):
            for (a, t) in zip(args, types):
                assert isinstance(a, t), \
                       "arg %r does not match %s" % (a,t)
            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts

def make_sure_params_wont_nuke_service(params):
    if params['radius'] > 1000:
        raise Exception("Radius is too large.")

    if params['duration'] > 60*24:
        raise Exception("Duration is too long.")

def get_number_of_valid_weekdays():
    cursor = get_db_cursor()
    sql = "SELECT count(*) FROM date_information WHERE is_weekday"
    print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    return int(result[0])

with app.app_context():
    number_of_valid_weekdays = get_number_of_valid_weekdays()

@accepts(float, float, int, int, str)
def get_time_distribution(latitude, longitude, radius, data_set, day_of_week):
    if radius > 1000:
        raise Exception("Radius is too large.")

    if data_set != 2013:
        raise Exception("data set %s not supported" % data_set)

    # First define a squareish object (defined by lat/long boundaries) for a quick first estimate of results.
    # A slower, but more accurate approach will follow.
    # There is an additional 0.1% added to the first squarish object to eliminate the slight risk of eliminating desired results.
    lat_rough_angle = (180 * radius) / (math.pi * earth_radius) * 1.001
    long_rough_angle = lat_rough_angle / math.cos(math.radians(latitude))

    parameters = {
        'radius': radius,
        'lat': latitude,
        'long': longitude,
        'lat_lower': latitude - lat_rough_angle,
        'lat_upper': latitude + lat_rough_angle,
        'long_lower': longitude - long_rough_angle,
        'long_upper': longitude + long_rough_angle,
        'day_of_week': day_of_week
    }

    # sql = "select count(*) from "

    sql = """SELECT EXTRACT(hour FROM issue_time) AS issue_hour, count(*) AS count FROM ny_parking_2013_consolidated2 c JOIN date_information di ON c.issue_date = di.date
        WHERE
            (di.day_of_week = %(day_of_week)s) AND
            (c.latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
            (c.longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
            (geo_distance(c.latitude, c.longitude, %(lat)s, %(long)s) < %(radius)s) AND
            di.is_weekday IS TRUE AND
            di.public_holiday IS FALSE
        GROUP BY EXTRACT(hour FROM issue_time)
        """

    print sql % parameters

    cursor = get_db_cursor()

    cursor.execute(sql, parameters)
    results = cursor.fetchall()

    result = [['hour'], ['count']]
    for i in range(0, len(results[0])):
        result[i].extend([value[i] for value in results])

    return result


@accepts(float, float, int, time, int, int)
def get_historical_sample(latitude, longitude, radius, start_time, duration, data_set = 2010):
    make_sure_params_wont_nuke_service(locals())

    # First define a squareish object (defined by lat/long boundaries) for a quick first estimate of results.
    # A slower, but more accurate approach will follow.
    # There is an additional 0.1% added to the first squarish object to eliminate the slight risk of eliminating desired results.
    lat_rough_angle = (180 * radius) / (math.pi * earth_radius) * 1.001
    long_rough_angle = lat_rough_angle / math.cos(math.radians(latitude))

    parameters = {
        'radius': radius,
        'lat': latitude,
        'long': longitude,
        'lat_lower': latitude - lat_rough_angle,
        'lat_upper': latitude + lat_rough_angle,
        'long_lower': longitude - long_rough_angle,
        'long_upper': longitude + long_rough_angle,
        'start_time': start_time.strftime("%H:%M") if data_set == 2013 else "NA",
        'duration': duration if data_set == 2013 else "NA"
    }
    
    if data_set == 2013:
        sql = """SELECT c.latitude, c.longitude, c.issue_date, c.issue_time FROM ny_parking_2013_consolidated2 AS c JOIN date_information AS di ON c.issue_date = di.date
        WHERE
            (c.latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
            (c.longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
            (geo_distance(c.latitude, c.longitude, %(lat)s, %(long)s) < %(radius)s) AND
            di.is_weekday IS TRUE AND
            di.public_holiday IS FALSE AND
            """
        sql += "(issue_time BETWEEN %(start_time)s AND (%(start_time)s::time + '%(duration)s minutes'::interval)) "
        sql += "ORDER BY RANDOM() LIMIT 100"

    elif data_set == 2010:
        sql = """SELECT c.latitude, c.longitude, c.issue_date_as_on_ticket AS issue_date FROM ny_parking_2010 AS c JOIN date_information AS di ON c.issue_date_as_on_ticket = di.date
        WHERE
            (c.latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
            (c.longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
            (geo_distance(c.latitude, c.longitude, %(lat)s, %(long)s) < %(radius)s) AND
            di.is_weekday IS TRUE AND
            di.public_holiday IS FALSE
            ORDER BY RANDOM() LIMIT 100
            """
    else:
        raise Exception("data set %s not supported" % data_set)

    # print sql % parameters  

    # print sql
    cursor = get_db_cursor()

    cursor.execute(sql, parameters)
    results = cursor.fetchall()

    return [{
        'lat': float(result[0]),
        'lng': float(result[1]),
        'date': result[2].strftime("%Y-%m-%d"),
        'time': result[3].strftime("%H:%M") if len(result) == 4 else "NA"
    } for result in results]

def main(latitude, longitude, radius, start_time, duration, data_set = 2010, include_historical = False, include_time_distribution = False):
    return determine_risk(latitude, longitude, radius, start_time, duration, data_set, include_historical, include_time_distribution)

@accepts(float, float, int, time, int, int, bool, bool)
def determine_risk(latitude, longitude, radius, start_time, duration, data_set = 2010, include_historical = False, include_time_distribution = False):
    make_sure_params_wont_nuke_service(locals())

    # First define a squareish object (defined by lat/long boundaries) for a quick first estimate of results.
    # A slower, but more accurate approach will follow.
    # There is an additional 0.1% added to the first squarish object to eliminate the slight risk of eliminating desired results.
    lat_rough_angle = (180 * radius) / (math.pi * earth_radius) * 1.001
    long_rough_angle = lat_rough_angle / math.cos(math.radians(latitude))

    parameters = {
        'radius': radius,
        'lat': latitude,
        'long': longitude,
        'lat_lower': latitude - lat_rough_angle,
        'lat_upper': latitude + lat_rough_angle,
        'long_lower': longitude - long_rough_angle,
        'long_upper': longitude + long_rough_angle,
        'start_time': start_time.strftime("%H:%M") if data_set == 2013 else "NA",
        'duration': duration if data_set == 2013 else "NA"
    }
    
    if data_set == 2013:
        # sql = """SELECT latitude, longitude, geo_distance(latitude, longitude, %(lat)s, %(long)s) As distance FROM ny_parking_2010 WHERE
        #     geo_distance(latitude, longitude, %(lat)s, %(long)s) < %(radius)s
        #     """

        # sql = """SELECT count(*) FROM ny_parking_2010 WHERE
        #     (latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
        #     (longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
        #     (geo_distance(latitude, longitude, %(lat)s, %(long)s) < %(radius)s)
        #     """

        # sql = """SELECT count(*) FROM ny_parking_2013_consolidated2 WHERE
        #     (latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
        #     (longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
        #     (issue_date BETWEEN %(start_date)s AND (%(start_date)s::date + '1 day'::interval)) AND
        #     (geo_distance(latitude, longitude, %(lat)s, %(long)s) < %(radius)s)
        #     """

        sql = """SELECT issue_date, count(*) AS count FROM ny_parking_2013_consolidated2 c JOIN date_information di ON c.issue_date = di.date
        WHERE
            (c.latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
            (c.longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
            (geo_distance(c.latitude, c.longitude, %(lat)s, %(long)s) < %(radius)s) AND
            di.is_weekday IS TRUE AND
            di.public_holiday IS FALSE AND
            """
        sql += "(issue_time BETWEEN %(start_time)s AND (%(start_time)s::time + '%(duration)s minutes'::interval)) "
        sql += "GROUP BY issue_date"
    elif data_set == 2010:
        sql = """SELECT issue_date_as_on_ticket AS issue_date, count(*) AS count FROM ny_parking_2010 c JOIN date_information di ON c.issue_date_as_on_ticket = di.date
        WHERE
            (c.latitude BETWEEN %(lat_lower)s AND %(lat_upper)s) AND
            (c.longitude BETWEEN %(long_lower)s AND %(long_upper)s) AND
            (geo_distance(c.latitude, c.longitude, %(lat)s, %(long)s) < %(radius)s) AND
            di.is_weekday IS TRUE AND
            di.public_holiday IS FALSE
            GROUP BY issue_date_as_on_ticket
            """
    else:
        raise Exception("data set %s not supported" % data_set)

    print sql % parameters  

    # print sql
    cursor = get_db_cursor()
    cursor.execute(sql, parameters)

    results = cursor.fetchall()
    # print "original result length: %s " % len(results)
    results = [result for result in results if result[1] > 0]
    # print "modified result length: %s " % len(results)

    number_of_valid_weekdays = get_number_of_valid_weekdays()

    number_of_fines = sum([result[1] for result in results])
    number_of_dates_with_fines = len([result[1] for result in results])

    result = {
        'number_of_fines': number_of_fines,
        'number_of_dates_with_fines': number_of_dates_with_fines,
        'number_of_possible_dates': number_of_valid_weekdays,
        'most_likely_probability': float(number_of_dates_with_fines) / float(number_of_valid_weekdays),
        'probability_interval': construct_interval(number_of_dates_with_fines, number_of_valid_weekdays),
        'inputs': {
            'lat': latitude,
            'lng': longitude,
            'radius': radius,
            'start_time': start_time.strftime("%H:%M") if data_set == 2013 else "NA",
            'duration': duration if data_set == 2013 else "NA",
            'data_set': data_set
        }
    }
    if include_historical:
        result['historical_sample'] = get_historical_sample(latitude, longitude, radius, start_time, duration, data_set)

    if data_set == 2013 and include_time_distribution:
        current_day_of_week = datetime.today().strftime("%A")

        result['time_distribution'] = get_time_distribution(latitude, longitude, radius, data_set, current_day_of_week)
        result['time_distribution_day'] = current_day_of_week
    return result

# x - number of successes
# n - number of trials
def construct_interval(x, n, conf_level = 0.95):
    x = float(x)
    n = float(n)
    print "WARNING: construct_interval is returning a fake result."
    result = (0.9*(x/n), x/n + ((1-(x/n)) * 0.1))
    return result

# 40.725671, -73.984719 - near East Village, Manhattan
# print determine_risk(40.725671, -73.984719, 1000, datetime.now(), 60, 2013)

# 40.713075 -73.957146 - near Williamsburg, Brooklyn
# print determine_risk(40.713075, -73.957146, 200, datetime.now(), 60*8, 2013)

# somewhere else in Brooklyn
# print determine_risk(40.650002, -74.006371, 200, datetime.now(), 60, 2013)
