
// start tracking object function

function start_Tracking() {
    // Get the current value from the text input box
    let object_id = document.getElementById('object').value
  
    // This URL path is going to be the route defined in app.py
    let theURL='/track/'+object_id;
    // This logger is just to keep track of the function call.
    // You can use such log messages to debug your code if you need.
    console.log("Making a RESTful display request to the server!")
    // fetch is a Javascript function that sends a request to a server
    fetch(theURL)
        .then(response=>response.json()) // Convert response to JSON
        // Run the anonymous function on the received JSON response
        .then(function(response) {
            // Changes element GPS in index to "No Object Found" if nothing is found in Camera.py
            
          console.log(response)
          var count = Object.keys(response).length
          if (count == 0){
              document.getElementById("GPS").innerHTML = "No Object Found";
          }

          // Begin new table construction
          else{
              var cols = [];
              for (var i = 0; i < response.length; i++){
                  for (var k in response[i]){
                      if (cols.indexOf(k)===-1){
                          cols.push(k);

                      }

                  }

              }

              var table = document.createElement("table");

              var tableRow = table.insertRow(-1);
              
              for(var i=0; i<cols.length; i++){
                  var tableHeader = document.createElement("th");
                  tableHeader.innerHTML = cols[i];
                  tableRow.appendChild(tableHeader);

              }

              for(var i=0; i<response.length; i++){
                  tRow = table.insertRow(-1);
                  for(var j=0; j<cols.length; j++){
                      var cell = tRow.insertCell(-1);
                      cell.innerHTML = response[i][cols[j]];

                  }


              }
              console.log(table)

              //Replace Table element with new table
              
              document.getElementById('myTable').innerHTML = table.innerHTML;
              

              //Update GPS element accordingly




                var Coord = "Object found at Latitude: " + response[(response.length - 1)]["Latitude"] + " Longitude: " + response[(response.length - 1)]["Longitude"];
                document.getElementById("GPS").innerHTML = Coord;
            }
        });
  }

//Save collected data to found_objects table when called via app.py

function save_Table() {


  // Get the current value from the text input box
    let object_id = document.getElementById('object').value
  
    // This URL path is going to be the route defined in app.py
    let theURL='/save/'+object_id;
    // This logger is just to keep track of the function call.
    // You can use such log messages to debug your code if you need.
    console.log("Making a RESTful display request to the server!")
    // fetch is a Javascript function that sends a request to a server
    fetch(theURL)
        .then(response=>response.json()) // Convert response to JSON
        // Run the anonymous function on the received JSON response
        .then(function(response) {

        });
  }

