var map;
var lat;
var lng;
var circleradius;
var duration;
var currenttime;
var currentdate = new Date();
var hours;
var minutes;
var marker;
var parkcircle;
var infowindow;
var contentString;
var point_address;
var finedata=[];
var pointArray;
var count = 1;
var time;
var heatmap;
var pointArray;
var year_option;

var number_of_fines;
var number_of_dates_with_fines;
var most_likely_probability;
var p_interval_start;
var p_interval_end;
var number_of_possible_dates;
var time_distribution

google.load("visualization", "1", {packages:["corechart"]});


jQuery(document).ready(function($) {





	Number.prototype.round = function(places) {
  		return +(Math.round(this + "e+" + places)  + "e-" + places);
	}


	var ajaxrequest = function(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option){


		var data = {
			year_option: year_option,
			lat: lat,
			lng: lng,
			circleradius: circleradius,
			duration: duration,
			time:time
		};

		$.ajax({
		    type: "POST",
		    contentType: "application/json; charset=utf-8",
		    url: "/static/test_output.json",
		    data: data,
		    success: function (result) {

		    	if(year_option == 2010){

		    		number_of_fines = result.number_of_fines;
		    		number_of_dates_with_fines = result.number_of_dates_with_fines
		    		most_likely_probability = result.most_likely_probability
		    		p_interval_start = result.probability_interval[0];
		    		p_interval_end = result.probability_interval[1];
		    		number_of_possible_dates = result.number_of_possible_dates
		    		time_distribution = result.time_distribution;


			    	updateinfowindow2010(
			    		circleradius, 
			    		data.lat, 
			    		data.lng, 
			    		marker, 
			    		time, 
			    		duration,
			    		map,
			    		infowindow, 
			    		result.number_of_fines,
			    		result.number_of_dates_with_fines,
			    		result.most_likely_probability,
			    		result.probability_interval[1],
			    		result.number_of_possible_dates,
			    		result.probability_interval[0],
			    		point_address
			    		)


			    	createheatarray(result.historical_sample);

					pointArray = new google.maps.MVCArray(finedata);


					heatmap.setData(pointArray);


		    	}else if (year_option == 2013){

		    		number_of_fines = result.number_of_fines;
		    		number_of_dates_with_fines = result.number_of_dates_with_fines
		    		most_likely_probability = result.most_likely_probability
		    		p_interval_start = result.probability_interval[0];
		    		p_interval_end = result.probability_interval[1];
		    		number_of_possible_dates = result.number_of_possible_dates
		    		time_distribution = result.time_distribution;



			    	updateinfowindow2013(
			    		circleradius, 
			    		data.lat, 
			    		data.lng, 
			    		marker, 
			    		time, 
			    		duration,
			    		map,
			    		infowindow, 
			    		result.number_of_fines,
			    		result.number_of_dates_with_fines,
			    		result.most_likely_probability,
			    		result.probability_interval[1],
			    		result.number_of_possible_dates,
			    		result.probability_interval[0],
			    		point_address
			    		)

			    	createheatarray(result.historical_sample);

					pointArray = new google.maps.MVCArray(finedata);


					heatmap.setData(pointArray);

			    }

			}
		});
		lat = "";
		lng = "";


	}

	function drawChart(time_distribution) {


        // Create the data table.
        var data = google.visualization.arrayToDataTable(time_distribution);

        // Set chart options
        var options = {
          title: 'Hourly Parking Tickets',
          legend: 'none'
        };
                       
            var chart = new google.visualization.LineChart(document.getElementById('chart'));
            
            chart.draw(data, options);

      }



	var createheatarray = function(historical){

		for (i in historical){
			var heat_lat = historical[i].lat
			var heat_long = historical[i].lng
			var create_point = new google.maps.LatLng(heat_lat, heat_long);
			finedata.push(create_point)

		}

	}

	var createinfowindow = function(marker, map){
		contentString = ""

		infowindow = new google.maps.InfoWindow({
			content: contentString
		});
		infowindow.open(map,marker)

	}




	var updateinfowindow2013 = function(circleradius, lat, lng, marker, time, duration,map,infowindow, number_of_fines,number_of_periods_with_fines,most_likely_probability,p_interval_end, number_of_periods, p_interval_start, point_address){
		infowindow.close(map,marker)


		p_interval_start = p_interval_start*100;
		p_interval_end = p_interval_end*100;
		most_likely_probability = most_likely_probability*100;


		contentString = 
			"<div class='scrollFix'>Probability of a fine being issued in the specified area and time period: <br><b><span style='font-size:125%;color:#428bca'>"
			+most_likely_probability.round(2)+"%</span></b></div>"

		infowindow.setContent(contentString);

        infowindow.open(map,marker);
	}

	var updateinfowindow2010 = function(circleradius, lat, lng, marker, time, duration,map,infowindow, number_of_fines,number_of_periods_with_fines,most_likely_probability,p_interval_end, number_of_periods,p_interval_start, point_address){
		infowindow.close(map,marker)

		p_interval_start = p_interval_start*100;
		p_interval_end = p_interval_end*100;
		most_likely_probability = most_likely_probability*100;

		contentString = 
		"<div class='scrollFix'>Probability of a fine being issued in a specified area during a typical weekday: <br><b><span style='font-size:125%;color:#428bca'>"
			+most_likely_probability.round(2)+"%</span></b></div>"

		infowindow.setContent(contentString);



		infowindow.open(map,marker)
	}

	var plotMarkerCircle = function(circleradius, lat, lng, marker, parkcircle){


		marker.setPosition(new google.maps.LatLng(lat, lng))
		parkcircle.position = new google.maps.LatLng(lat, lng)
		parkcircle.setRadius(circleradius)



		setTimeout(function(){
			map.panTo(marker.position)

		}, 300);

	};

	var toggleHeatmap = function(heatmap) {
		heatmap.setMap(heatmap.getMap() ? null : map);

		count = count +1;
	}

	var geocodefunc = function(lat, lng){
		var latlng = new google.maps.LatLng(lat, lng);
		var geocoder= new google.maps.Geocoder();
		geocoder.geocode({'latLng': latlng}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
			    if (results[1]) {
			    	point_address = (results[1].formatted_address)

			    }else{
			    	point_address = "No results found"

			    }
			}else{
			    point_address = "Geocoder failed due to: " + status
			}

		});	
	}
	console.log("initialize")



	var initialize = function() {

		$('.RatingSlider').each(function(idx, elm) {
    			var name = elm.id.replace('Slider', '');
    			var	value = $(this).data('value');
    			var max = $(this).data('max');
    			var step = $(this).data('step');
    			var units = $(this).data('units');
    			var min = $(this).data('min');
			$('#' + elm.id).slider({
			        value: value,
		        	min: min,
		        	max: max,
		        	step: step,
		        	animate: true,
		        	slide: function(event, ui) {
		        	    $('#' + name).val("("+ui.value + " " + units+")");
		        	}
		    	});
		});

		$("#up").hide();
		$(".panel-heading").click(function(){

			setTimeout(function(){
				if($("#down").is(":visible")){
					$("#down").hide()
					$("#up").show()

				}else{
					$("#up").hide()
					$("#down").show()

				}

			}, 400);


		})

		$("#2010btn").click(function(){
			$("#2013btn").removeClass("active");
			$("#2010btn").addClass("active");

			year_option = 2010;

			$("#durationdiv").hide()
			$("#timediv").hide()
			$("#radiusdiv").removeClass('col-md-3')
			$("#radiusdiv").addClass('col-md-8')

			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);


		})

		$("#2013btn").click(function(){
			$("#2010btn").removeClass("active");
			$("#2013btn").addClass("active");

			year_option = 2013;

			$("#radiusdiv").removeClass('col-md-8')
			$("#radiusdiv").addClass('col-md-3')


			$("#durationdiv").show()
			$("#timediv").show()

			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);


		})

		$(window).resize(function(){
			if($("#myModal").hasClass('open')){
			    setTimeout(function(){
			    	drawChart(time_distribution);
			    }, 300);
			}
		});


		$("#modalbtn").click(function(){
			$("#myModal").removeClass("closed")
			$("#myModal").addClass("open")


			setTimeout(function(){
				drawChart(time_distribution)

			}, 400);

			$("#probabilitydiv").text((most_likely_probability*100).round(2) + "%")
			$("#intervaldiv").text((p_interval_start*100).round(2)+ "% to " + (p_interval_end*100).round(2) + "%")
			$("#dateswithfines").text(number_of_dates_with_fines)
			$("#numberfines").text(number_of_fines)
			$("#possibledates").text(number_of_possible_dates)


		})

		if(currentdate.getHours() < 10){
			hours = "0" + currentdate.getHours();
		}else{
			hours = currentdate.getHours();
		}

		if(currentdate.getMinutes() < 10){
			minutes = "0" + currentdate.getMinutes();
		}else{
			minutes = currentdate.getMinutes();
		}


		currenttime = hours + ":" + minutes;

		$('#time').val(currenttime);

		circleradius = $("#s1Slider").data('value');
		duration = $("#s2Slider").data('value');
		time = $('#time').val();

		lat = 40.6823;
		lng = -73.9558;

		point_address = "New York, NY 10024, USA"
		var mapOptions = {
		    zoom: 12,
		    center: new google.maps.LatLng(lat, lng)
		};

		map = new google.maps.Map(document.getElementById('map-canvas'),
			mapOptions);

		marker = new google.maps.Marker({
			position: new google.maps.LatLng(lat, lng),
			map: map,
			title: 'Probability of ticket by parking here',
			draggable: true
		});


		populationOptions = {
			strokeColor: '#FF0000',
			strokeOpacity: 0,
			strokeWeight: 2,
			fillColor: 'grey',
			fillOpacity: 0.3,
			map: map,
			center: new google.maps.LatLng(lat, lng),
			radius: Number(circleradius),
			draggable: true
		};

		parkcircle = new google.maps.Circle(populationOptions);

		parkcircle.bindTo('center', marker, 'position')

		plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);

		pointArray = new google.maps.MVCArray(finedata);

		heatmap = new google.maps.visualization.HeatmapLayer({
			data: pointArray,
			radius: 7

		});


  		heatmap.setMap(map);

		$("#heatmap1").click(function(){
			$("#heatmap2").removeClass('active')
			$("#heatmap1").addClass('active')
			if(count%2 == 0){
				toggleHeatmap(heatmap);
			}

		})

		$("#heatmap2").click(function(){
			$("#heatmap1").removeClass('active')
			$("#heatmap2").addClass('active')
			if(count%2 !=0){
				toggleHeatmap(heatmap);
			}
		})

		contentString = ""

		infowindow = new google.maps.InfoWindow({
			content: contentString
		});
		infowindow.open(map,marker)
		year_option = 2013;


		ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);





		google.maps.event.addListener(map, "click", function(event) {
			lat = event.latLng.lat();
			lng = event.latLng.lng();

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

			plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);


			geocodefunc(lat, lng)


			ajaxrequest(lat, lng, circleradius, duration, time,marker, map, infowindow, year_option);


		});


		google.maps.event.addListener(marker, "dragend", function(event) {
			lat = event.latLng.lat();
			lng = event.latLng.lng();

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

			plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);

			geocodefunc(lat, lng)


			ajaxrequest(lat, lng, circleradius, duration, time,marker, map, infowindow, year_option);


		});


		google.maps.event.addListener(marker, "drag", function(event) {
			lat = event.latLng.lat();
			lng = event.latLng.lng();

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

			plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);

		});

		google.maps.event.addListener(parkcircle, "dragend", function(event) {
			lat = event.latLng.lat();
			lng = event.latLng.lng();

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

			plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);

			geocodefunc(lat, lng)


			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);

		});

		$('#s1Slider').on("slide", function(event,ui){

			circleradius = $("#s1Slider").slider("option","value");
	    	var markerpos = marker.position

	    	lat = markerpos.lat();
	    	lng = markerpos.lng();

	    	plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);


		});


		$('#s1Slider').on("slidechange", function(event,ui){

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

	    	var markerpos = marker.position;

	    	lat = markerpos.lat();
	    	lng = markerpos.lng();

			plotMarkerCircle(circleradius, lat, lng, marker, parkcircle);

			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);

		});

		$('#s2Slider').on("slidechange", function(event,ui){

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

	    	var markerpos = marker.position;

	    	lat = markerpos.lat();
	    	lng = markerpos.lng();

			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);

		});

		$("#time").change(function(){

			circleradius = $("#s1Slider").slider("option","value");
			duration = $("#s2Slider").slider("option","value");
			time = $('#time').val();

	    	var markerpos = marker.position;

	    	lat = markerpos.lat();
	    	lng = markerpos.lng();


			ajaxrequest(lat, lng, circleradius, duration, time, marker, map, infowindow, year_option);


		})



	}
	google.maps.event.addDomListener(window, 'load', initialize);


});

