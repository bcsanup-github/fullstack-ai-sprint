
const form = document.querySelector("#prompt-form");
const promptInput = document.querySelector("#prompt");
const submitBtn = document.querySelector("#submit-btn");
const output = document.querySelector("#output");


const API_URL = "http://localhost:8000/api/prompt/";

form.addEventListener("submit", async (event) => {
    event.preventDefault();        

    const prompt = promptInput.value.trim();
    if (!prompt) return;                 

    submitBtn.disabled = true;           
    output.textContent = "Thinking...";

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt, mode: "summarize" }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();

        
        const reply = typeof data.reply === "string"
            ? data.reply
            : JSON.stringify(data.reply, null, 2);

        output.textContent = reply + (data.mock ? "\n\n(demo mode — AI is mocked)" : "");
    } catch (err) {
        output.textContent = `Error: ${err.message}`;
    } finally {
        submitBtn.disabled = false;     
    }
});