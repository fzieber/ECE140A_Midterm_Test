
// display button function

function click_display() {
    // Get the current value from the text input box
    let photo_id = document.getElementById('textInput').value
  
    // This URL path is going to be the route defined in app.py
    let theURL='/photos/'+photo_id;
    // This logger is just to keep track of the function call.
    // You can use such log messages to debug your code if you need.
    console.log("Making a RESTful display request to the server!")
    // fetch is a Javascript function that sends a request to a server
    fetch(theURL)
        .then(response=>response.json()) // Convert response to JSON
        // Run the anonymous function on the received JSON response
        .then(function(response) {
            // Set the value of the img_src attribute of the img tag
            // to the value received from the server
            let img = document.getElementById('image') 
            img.src = 'images/' + response['img_src']
            let imgCrop = document.getElementById('imageCrop')
            imgCrop.src = 'images/' + 'Crop' + response['img_src']
            let text = document.getElementById('plate')
            if (text == "XXXXXXXX"){
                text.innerHTML = "Car Not Detected. Number Plate: XXXXXXX"
            }
            else{
                text.innerHTML = "Car Detected. Number Plate: " + response["text"]
            }
        });
  }

 