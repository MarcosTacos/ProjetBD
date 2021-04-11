
// alert("app.js");
const cors = require("cors");
app.use(cors())

// Register click goes to sign-in page
function onButtonRegisterClick()
{
    // alert("Register");
    window.location.href = "sign-in.html";
}


// Client login
function onButtonLoginClick()
{
    var inputElementEmail = document.getElementById("email-input");
    var email = inputElementEmail.value;
    var inputElementPassword = document.getElementById("password-input");
    var password = inputElementPassword.value;

    alert(email+" "+password);
    postLogin(email, password)
    inputElementEmail.value = ""
    inputElementPassword.value = ""
}

function postLogin(email, password) {
    // postUrl = "login"
    postUrl = "/loginUser";

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    }).then(function(response) {
        alert("message1"+JSON.stringify(response));
        return response.json()
    }).then(function(data) {
        alert("message2"+JSON.stringify(data))
        console.log("worked")
    })
}




function postTodo(text) {
    postUrl = "add-todo"

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

function displayNewTodo(text) {
    var todosContainer = document.getElementById("todos-container");

    var newTodoElement = document.createElement("div");

    newTodoElement.innerHTML = text;

    todosContainer.appendChild(newTodoElement);
}
