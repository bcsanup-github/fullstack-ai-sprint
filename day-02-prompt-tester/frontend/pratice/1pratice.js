/*Fetch + error handling. Write an async function that fetches
 https://jsonplaceholder.typicode.com/todos/1, logs the title field,
  and has a try/catch that logs a friendly message. Then deliberately
   break the URL (misspell it) and confirm your catch fires.*/

// working url
async function fetchTodo() {
    try {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/todos/1"
        );
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();

        console.log("Title:", data.title);
    } catch (error) {
        console.log("Something went wrong while fetching the data.");
    }
}

//Deliberately break the URL
//For example, misspell typicode as typicod

async function fetchTodoBroken() {
    try {
        const response = await fetch(
            "https://jsonplaceholder.typicod.com/todos/1"
        );
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();

        console.log("Title:", data.title);
    } catch (error) {
        console.log("Something went wrong while fetching the data.");
    }
}

fetchTodo();
fetchTodoBroken();
