const API_BASE = "http://localhost:8088";
const container = document.querySelector("#cards");

async function loadMetrics() {
    container.textContent = "Loading...";
    try {
        const res = await fetch(`${API_BASE}/api/metrics/`);
        if (!res.ok) throw new Error(`HTTP  ${res.status}`);
        const metrics = await res.json();

        container.innerHTML = "";
        metrics.forEach(m => {
            const card = document.createElement("div");
            card.className = "card";
            card.textContent = `${m.name}: ${m.value} (${m.trend})`;
            container.appendChild(card);
        });
    } catch (err) {
        container.textContent = `failed to load metrics: ${err.message}`;
    }
}

loadMetrics();