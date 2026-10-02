//Given const nums = [4, 9, 1, 7], produce a new array of their squares, then their sum, using map and reduce.

const nums = [4,9,1,7];
const squares = nums.map(num => num * num);
const sum = squares.reduce((total, num) => total + num, 0);

console.log("squares:", squares);
console.log("sum:", sum);


//Write greet(name) as both a function declaration and an arrow function; log both.
//function declaration
function greet(name) {
    return `hello, ${name}!`;
}

//arrow function 
const greetarrow = (name) => {
    return  `hello, ${name}!`;
};

console.log(greet("sanup"));
console.log(greetArrow("sanup"));


//Build an array of 3 objects { name, value } and run console.table(yourArray) — it prints a neat table.
const students = [
    {name: "sanup", value:85 },
    {name: "ram", value: 86},
    {name: "sita", value: 92}
];

console.table(students);

//In app.js, select the button and, on click, append a new <li> with the current time to the <ul>
const button = document.querySelector("#timeBtn");
const list = document.querySelector("#timeList");

button.addEventListener("click", () => {
    const li = document.createElement("li");
    li.textContent = new Date().toLocaleDateString();
    list.appendChild(li);
});