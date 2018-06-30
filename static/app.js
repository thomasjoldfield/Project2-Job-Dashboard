//some button listeners
$(function(){
  if($('body').is('.compare')){
    document.getElementById("compareBtn").addEventListener("click", buildComparePlot);
  }
});




/*Thomas is adding this part here to build our comparison bar charts*/
function buildComparePlot() {
    /* data route */
    /*Make this dynamic*/
    var origin = document.getElementById("origin_input").value;
    var dest = document.getElementById("dest_input").value;
    var url = `/delaycomparison/${origin}/${dest}`;
    Plotly.d3.json(url, function(error, response) {
  
      console.log(response);

      var data = [response];
  
      Plotly.newPlot("plot", data);
    });
  }
  
//buildComparePlot();


function buildAirportMap() {
  /*data route */
var url = "/airports";

//Perform a call from the data 
d3.json(url,function(error, response){

 console.log(response);

 var data = response;
 console.log(data);
 console.log(data.length);



//Create a map object 
  var myMap = L.map("mainMap", {
  center: [38, -96],
  zoom: 5

});

// Adding a tile layer (the background map image) to our map
// We use the addTo method to add objects to our map
L.tileLayer(
  "https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
    "access_token=pk.eyJ1IjoiaGVhdGhlcjg5IiwiYSI6ImNqaWF2YjNsNjAwMW0zcHFyOWJzMnR4bXYifQ.OBd2HT7cnCJxqxgj0-haNA." +
    "T6YbdDixkOBWH_k9GbS8JQ"
).addTo(myMap);



// Loop through the cities array and create one marker for each city object
for (var i = 0; i <data.length; i++) {
  console.log(data[i])
  var latitude = data[i].lat
  console.log(latitude)
  var longitude = data[i].long
  console.log(longitude)
//  L.marker(L.latLng(parseFloat(latitude), parseFloat(longitude)))
  L.marker(L.latLng(longitude, latitude))
    .bindPopup("<h1>" + data[i].code +"</h1><br><h3>"+ data[i].name + "</h3>")
    .addTo(myMap);
}
}
)}

//experimental! and it works!
$(function(){
  if($('body').is('.index')){
    buildAirportMap()
  }
});

//buildAiportMap()