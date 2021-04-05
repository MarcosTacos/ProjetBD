function displayNewTodo(text) {
    var todosContainer = document.getElementById("todos-container");

    var newTodoElement = document.createElement("div");

    newTodoElement.innerHTML = text;

    todosContainer.appendChild(newTodoElement);
}

function onButtonClick() {
    var inputElement = document.getElementById("todo-input");

    var newTodoText = inputElement.value;

    displayNewTodo(newTodoText)

    inputElement.value = ""

    postTodo(newTodoText)
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
