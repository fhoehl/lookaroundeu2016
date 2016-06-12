require('./index.css')

var jsondb = require("json!./data.json");

var init = function () {
  var cities = {
    'manchester': [53.472225, -2.2936317],
    'chester': [53.1969395,-2.86239282],
  }

  var element = document.getElementById('map')

  var myOptions = {
    center: { lat: 53.439405723336094, lng: -4.30446978750002 },
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    mapTypeControl: false,
    panControl: false,
    scrollwheel: false,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL,
      position: google.maps.ControlPosition.TOP_RIGHT,
    },
  }

  var map = new google.maps.Map(element, myOptions)

  var panTo = function (x, y) {
    return (e) => {
      console.log(map.getCenter().lat(), map.getCenter().lng())
      e.preventDefault();
      map.panTo(new google.maps.LatLng(x, y))
      map.setZoom(10)
    }
  }

  var makeInfoWindow = function (marker) {
    let content = jsondb[marker.title]

    let contentString = `
    <h2>${marker.title}</h2>
    <p>${content.d}</p>
    <img class="center" src="http://placekitten.com/g/300/200"/>
    <p><a href="${content.s}">source</a></p>`

    let infowindow = new google.maps.InfoWindow({
      content: contentString,
      maxWidth: 360,
    })

    infowindow.open(map, marker)
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        let initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
        map.setCenter(initialLocation)
      },
      () => { map.setCenter(map.getCenter()) }
    )
  }

  for (var key in jsondb) {
    let val = jsondb[key]
    let point = val['p'].split(',')

    let latlng = new google.maps.LatLng(point[0], point[1])

    let marker = new google.maps.Marker({
      position: latlng,
      map: map,
      title: key,
    })

    marker.addListener('click', function (e) { makeInfoWindow(this) })
  }

  for (let city in cities) {
    let point = cities[city]
    let btnEl = document.getElementById(`${city}Btn`)

    if (btnEl)  {
      btnEl.addEventListener('click', panTo(point[0], point[1]))
    }
  }
}

window.addEventListener('load', init)

