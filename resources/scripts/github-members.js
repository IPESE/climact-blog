const inputUsernameDiv = document.getElementsByClassName("input-username")[0];

let inputField = document.createElement("input");
inputField.setAttribute("type", "text");
inputField.setAttribute("placeholder", "Enter username");

// Create confirm button
let confirmButton = document.createElement("button");
confirmButton.textContent = "Confirm";

let validation = document.createElement("p");

// Append input and button to the div
inputUsernameDiv.appendChild(inputField);
inputUsernameDiv.appendChild(confirmButton);
inputUsernameDiv.appendChild(validation);

async function checkGitHubUser(username) {
    const url = `https://api.github.com/users/${username}`;
    
    try {
        const response = await fetch(url);
        
        if (response.ok) {
            const userData = await response.json();
            if(userData.message === "Not Found"){return false}
            return true;
        } else {
            throw new Error(errorData.message); // Handle other errors
        }
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

confirmButton.addEventListener("click", function() {
    // Get the value of the input
    const username = inputField.value;

    checkGitHubUser(username)
    .then(userData => {
        if (userData) {
            const url = 'https://ipese-web.epfl.ch/web-services/climact-member';
            const data = {
            username: username
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
                inputField.value=""
                validation.innerHTML="Username sent to IT support"
                validation.classList.add('success')
                inputField.classList.remove('error')
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
                validation.innerHTML="We had a problem. Try again later or contact the administrator"
                validation.classList.remove('success')
                inputField.classList.remove('success')
                validation.classList.add('error')
                inputField.classList.add('error')
            });
        } else {
            console.log(`User ${username} does not exist.`);
            validation.innerHTML=`User ${username} does not exist.`
            validation.classList.remove('success')
            inputField.classList.remove('success')
            validation.classList.add('error')
            inputField.classList.add('error')
        }
    });

});