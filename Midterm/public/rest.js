
isWarning = 'false'
// Save Input Height
function toggle_warning(isToggled) {
  if (isToggled == 'true'){
      if (isWarning == 'false'){
          isWarning = 'true';
      }
      else{
          isWarning = 'false';
      }
  }
  
  return isWarning;
  
  
}
// display button function

function click_display() {
  // Get the current value from the text input box
  let sTime = document.getElementById('minTime').value;
  let eTime = document.getElementById('maxTime').value;
  let sDist = document.getElementById('minDist').value;
  let eDist = document.getElementById('maxDist').value;
  let alarm = toggle_warning('false');

  if (sTime > eTime){
      temp = sTime;
      sTime = eTime;
      eTime = temp;

  }
  if (sDist > eDist){
      temp = sDist
      sDist = eDist
      eDist = temp

  }

  // This URL path is going to be the route defined in app.py
  let theURL='/data/'+ sTime + '/'+ eTime + '/'+ sDist + '/' + eDist + '/'+ alarm;
  // This logger is just to keep track of the function call.
  // You can use such log messages to debug your code if you need.
  console.log("Making a RESTful display request to the server!")
  // fetch is a Javascript function that sends a request to a server
  fetch(theURL)
      .then(response=>response.json()) // Convert response to JSON
      // Run the anonymous function on the received JSON response
      .then(function(response) {
          // Set the value of the img_src attribute of the img tag
          // and Owner value to relevant data from response, or
          // placeholders for no range inputs

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
          let result = document.getElementById('result');

          if ((sTime == eTime)&&(sDist == eDist)){
              result.innerHTML = "<table><tr><td> Time </td><td> Temperature </td><td> Humidity </td><td> Distance </td></tr></table>";   
          }
          else{
              result.innerHTML = "";
              result.appendChild(table);
          }
              
                   
          
      });
}
