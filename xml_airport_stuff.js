var queryUrl = "http://apps.tsa.dhs.gov/MyTSAWebService/GetTSOWaitTimes.ashx?ap=DEN"

var xhr = new XMLHttmRequest();
xhr.open("GET", queryURL, false);

xhr.setRequestHeader('Content-Type', 'text/xml');
xhr.send();

xmlDocument = xhr.responseXML;
console.log(xmlDocument.childNodes['0'].textContent);
