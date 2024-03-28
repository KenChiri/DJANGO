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

    document.getElementById('chargesheetli').addEventListener('click', function () {
        showPage('chargesheet');
    });

    document.getElementById('medicalreportli').addEventListener('click', function () {
        showPage('medicalreport');
    });

    document.getElementById('accidentAlertsli').addEventListener('click', function () {
        loadAccidentAlerts();
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
        var contentDiv = document.getElementById("accidentAlertsContent");
    
        // Check if the div is already populated
        if (contentDiv.innerHTML.trim() !== "") {
            console.log("accidentAlertsContent is already populated");
            return;
        }
    
        console.log("loadAccidentAlerts function called");  // Log when the function is called
    
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                contentDiv.innerHTML = this.responseText;
                console.log("AJAX request successful");  // Log when the AJAX request is successful
                console.log(this.responseText);  // Log the response text
            } else if (this.readyState == 4) {
                console.log("AJAX request failed");  // Log when the AJAX request fails
            }
        };
        xhttp.open("GET", "{% url 'emergency:alerts' %}", true);
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


document.getElementById('submit').addEventListener('click', function () {
    // Handle form submission logic here
    var vehicleRegNos = document.getElementsByName('vehicleRegNo[]');
    var regNosArray = Array.from(vehicleRegNos).map(function (input) {
        return input.value;
    });
    console.log(regNosArray);
    // Perform other actions like submitting data to the backend
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

//Submitting the names of witnesses 
document.getElementById('submit').addEventListener('click', function () {
    // Handle form submission logic here
    var witnessContainers = document.getElementById('witnessList').children;
    var witnessesData = Array.from(witnessContainers).map(function (container) {
        var nameInput = container.querySelector('input[name="witnessName[]"]');
        var addressInput = container.querySelector('input[name="witnessAddress[]"]');
        return {
            name: nameInput.value,
            address: addressInput.value
        };
    });
    console.log(witnessesData);
    // Perform other actions like submitting data to the backend
});
