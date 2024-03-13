const inputUsernameDiv = document.getElementsByClassName("input-username")[0];

let inputField = document.createElement("input");
inputField.setAttribute("type", "text");
inputField.setAttribute("placeholder", "Enter username");

// Create confirm button
let confirmButton = document.createElement("button");
confirmButton.textContent = "Confirm";

// Append input and button to the div
inputUsernameDiv.appendChild(inputField);
inputUsernameDiv.appendChild(confirmButton);

confirmButton.addEventListener("click", function() {
    // Get the value of the input
    const username = inputField.value;

    const url = 'https://ipese-mattermost.epfl.ch/hooks/jgdt4qu59fba5qzeujpe6kmaur';
    const data = {
    text: "please add this user to climact project"+username
    };

    fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
    })
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
    })
    .then(data => {
    console.log('Message sent:', data);
    })
    .catch(error => {
    console.error('There was a problem with your fetch operation:', error);
    });

});