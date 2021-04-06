function displayNewTodo(text) {
    var todosContainer = document.getElementById("username-container");

    var newUsername = document.createElement("div");

    newUsername.innerHTML = text;

    todosContainer.appendChild(newUsername);
}

function onButtonClick() {
    var inputUsername = document.getElementById("username-input");

    var newUsername = inputUsername.value;

    displayNewTodo(newUsername)

    inputUsername.value = ""

    postUsername(newUsername)
}

function postUsername(text) {
    postUrl = "add-username"

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    }).then(function(response) {
        return response.json()
    }).then(function(data) {
        console.log("worked")
    })
}

function fetchTodos() {
    getUrl = "todos/"

    fetch(getUrl).then(function(response) {
        return response.json()
    }).then(function(data) {
        todos = data.todos;

        for(let todo of todos) {
            displayNewTodo(todo);
        }
    })
}
