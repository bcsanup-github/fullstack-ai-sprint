const form = document.querySelector("#prompt-form");
const promptInput = document.querySelector("#prompt");
const submitBtn = document.querySelector("#submit-btn");
const output = document.querySelector("#output");

const API_URL = "https://jsonplaceholder.typicode.com/posts";

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const prompt = promptInput.value.trim();
    if (!prompt) return;

    submitBtn.disabled = true;
    output.textContent = "Thinking...";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify({ prompt}),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    } finally {
        submitBtn.disabled = false;
    }
});