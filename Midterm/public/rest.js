

isWarning = false
  // Save Input Height
function toggle_warning(isToggled) {
    if (isToggled){
        isWarning = !isWarning;
    }
    
    return isWarning;
    
    
  }
// display button function

function click_display() {
    // Get the current value from the text input box
    let sTime = document.getElementById('minTime').value
    let eTime = document.getElementById('maxTime').value
    let sDist = document.getElementById('minDist').value
    let eDist = document.getElementById('maxDist').value
    let alarm = toggle_warning(false)
  
    // This URL path is going to be the route defined in app.py
    let theURL='/photos/'+inHeight + '/'+inAge;
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
            if ((inHeight == 139)&&(inAge == 9)){
                
                let img = document.getElementById('image') 
                img.src = ""
                let img_owner = document.getElementById('Owner')
                img_owner.innerText = ""
                
                
            }
            else{
                
                let img = document.getElementById('image') 
                img.src = response['img_src']
                let img_owner = document.getElementById('Owner')
                img_owner.innerText = response['img_own']
                
                
            }
                
                     
            
        });
  }
