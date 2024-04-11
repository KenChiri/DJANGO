document.addEventListener('DOMContentLoaded', function () {
    // Check if there's a hash in the URL and show the corresponding page
    var currentPage = window.location.hash.substring(1);
    if (currentPage) {
        showPage(currentPage);
    }

    // Add event listeners to navigation items
    document.getElementById('abstractli').addEventListener('click', function () {
        showPage('abstract');
    });

    document.getElementById('roughLi').addEventListener('click', function () {
        showPage('roughDraft');
    });

    document.getElementById('accidentAlertsli').addEventListener('click', function () {
        loadAccidentAlerts();
    });
    document.getElementById('crimeAlertsli').addEventListener('click', function () {
        loadCrimeAlerts();
    });
  


    function showPage(pageId) {
        // Hide all pages
        var pages = document.getElementsByClassName('sect');
        for (var i = 0; i < pages.length; i++) {
            pages[i].style.display = 'none';
        }

        // Show the selected page
        document.getElementById(pageId).style.display = 'block';

        // Update the hash in the URL to reflect the current page
        window.location.hash = pageId; //This will help us such that when we are in a specific div and we refresh it won't go back to the home
    }
    
    //This is the ajax code that will retrieve the emergency app html file
    
    function loadAccidentAlerts() {
        // Get the accidentAlertsContent div
        var contentDiv = document.getElementById("accidentAlerts");
    

    
        console.log("loadAccidentAlerts function called");  // Log when the function is called
       
    
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(xhttp.responseText);  // Log the response text
                showPage('accidentAlerts')
                // Include the fetched content in the div
                contentDiv.innerHTML = this.responseText;

                console.log("AJAX request successful");  // Log when the AJAX request is successful                
                console.log(this.responseText);  // Log the response text
            } else if (this.readyState == 4) {
                console.log("AJAX request failed");  // Log when the AJAX request fails
            }
        };
        xhttp.open("GET", 'alerts', true);
        
        xhttp.send();
    }

    function loadCrimeAlerts() {
        // Get the accidentAlertsContent div
        var contentDiv = document.getElementById("crimeAlerts");
    

    
        console.log("loadCrimeAlerts function called");  // Log when the function is called
       
    
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                console.log(xhttp.responseText);  // Log the response text
                showPage('crimeAlerts')
                // Include the fetched content in the div
                contentDiv.innerHTML = this.responseText;

                console.log("AJAX request successful");  // Log when the AJAX request is successful                
                console.log(this.responseText);  // Log the response text
            } else if (this.readyState == 4) {
                console.log("AJAX request failed");  // Log when the AJAX request fails
            }
        };
        xhttp.open("GET", 'crimes', true);
        
        xhttp.send();
    }
    
});





const listButtons = document.querySelectorAll('li');

listButtons.forEach(item => {
    item.addEventListener('click', (event) => {
        const link = item.querySelector('a');
        if(link) {
            window.location.href = link.href;
        }

    });
    item.style.cursor = 'pointer';
});

//Dynamically displaying the charged section through a radio button
/*const chargedRadioButtons = document.querySelectorAll('input[name="charged"]');
const chargeDetails = document.getElementById('chargeDetails');
chargeDetails.style.display = 'none';
chargedRadioButtons.forEach(radioButton => {
    radioButton.addEventListener('click', () => {
      if (radioButton.value === 'YES') {
        chargeDetails.style.display = 'block'; // Show if YES is selected
      } else {
        chargeDetails.style.display = 'none'; // Hide if NO is selected or any other value
      }
    });
  }); */

  //Adding new vehicle
  document.getElementById('addVehicle').addEventListener('click', function() {
    //Create a new input field
    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'vehicleRegNo[]';
    newInput.required = true;

    //Append the new input field to the list
    document.getElementById('vehicleList').appendChild(newInput);
});


document.getElementById('removeVehicle').addEventListener('click', function() {
    //Get the last input field in the list
    var vehicleList = document.getElementById('vehicleList');
    var lastInput = vehicleList.lastElementChild;

    if (lastInput) {
        // Remove the last input field
        vehicleList.removeChild(lastInput);
    }

});



//Adding a new witness
document.getElementById('addWitness').addEventListener('click', function() {
    //Create a new witness input field
    var newNameInput = document.createElement('input');
    newNameInput.type = 'text';
    newNameInput.name = 'witnessName[]';
    newNameInput.placeholder = 'Witness Name'
    newNameInput.required = true;


    //Create the adress field
    var newAddressInput = document.createElement('input');
    newAddressInput.type = 'text';
    newAddressInput.name = 'witnessAddress[]';
    newAddressInput.placeholder = 'Witness Address';
    newAddressInput.required = true;

    //create a div to append the two fields
    var witnessContainer = document.createElement('div');
    witnessContainer.appendChild(newNameInput);
    witnessContainer.appendChild(newAddressInput);

    //Now append the container to the div in the html (witness List)
    document.getElementById('witnessList').appendChild(witnessContainer);
});


document.getElementById('removeWitness').addEventListener('click', function() {
    //Get the last input field in the list and remove it
    var witnessList = document.getElementById('witnessList');
    var lastWitnessContainer = witnessList.lastElementChild;

    if (lastWitnessContainer) {
        // Remove the last witness container
        witnessList.removeChild(lastWitnessContainer);
    }

});

