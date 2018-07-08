//some button listeners

//this function makes sure the compare code only runs on the compare page
$(function(){
//This searches for a body element that has the class "compare". MAke sure that any new html includes the page name as a class on the body.
  if($('body').is('.compare')){
//When it finds a compare body, it applies the below code.
//This code adds an event listener onto a compare button. That listener runs the "buildComparePlot" function on click
    document.getElementById("compareBtn").addEventListener("click", buildComparePlot);
  }
});




//Compare Function - pull and display data for a single origin-destination pairing.
function buildComparePlot() {
//First step is to pull origin and destination from the UI. Finds the user input using ID
    var origin = document.getElementById("origin_input").value;
    var dest = document.getElementById("dest_input").value;
//Build URL using the above inputs
    var url = `/delaycomparison/${origin}/${dest}`;
//Go and get data from the newly build API destination. Data is already beautifully formatted (ha) for Plotly, so just pass results.
    Plotly.d3.json(url, function(error, response) {
  
      console.log(response);
      var data = [response];
      var layout = {
        margin:{
          l:200
        },
        xaxis: {
          title: 'Stressfulness',
          titlefont: {
            famly: 'Arial, sans-serif',
            size: 18,
            color: 'darkgrey'
          },
          showgrid: true,
          zeroline: true,
          mirror: 'ticks',
          gridcolor: '#bdbdbd',
          gridwidth: 2,
          zerolinecolor: '#969696',
          zerolinewidth: 4,
          linecolor: '#636363',
          linewidth: 6,
          tickfont: {
            famly: 'Arial, sans-serif',
            size: 18,
            color: 'darkgrey' 
          },
          range: [0, 100]},
        yaxis: {
          showgrid: false,
          zeroline: true,
          mirror: 'ticks',
          gridcolor: '#bdbdbd',
          gridwidth: 2,
          zerolinecolor: '#969696',
          zerolinewidth: 4,
          linecolor: '#636363',
          linewidth: 6,
          tickfont: {
            famly: 'Arial, sans-serif',
            size: 18,
            color: 'darkgrey' 
          },
        }
      };
      Plotly.newPlot("plot", data, layout);
    });
  }
  
//We do not run the function here, we wait for button click


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