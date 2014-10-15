import ny_parking_risk, json
from datetime import datetime, time

# time(0,0)

result = ny_parking_risk.determine_risk(40.725671, -73.984719, 150, datetime.now().time(), 60*3, 2013, True, True)

fo = open("test_output.json", "w")
fo.write(json.dumps(result));
fo.close()
