async function loadPlayer() {
    const playerName = localStorage.getItem("playerName");
    const playerId = localStorage.getItem("playerId");

    const res = await fetch(`http://127.0.0.1:8000/player/${playerId}`);
    const data = await res.json();

    document.getElementById("playerName").innerText = playerName;
    document.getElementById("impactScore").innerText =
        "Impact Score: " + data.impact_score.toFixed(2);

    document.getElementById("height").innerText = data.height ?? "—";
    document.getElementById("weight").innerText = data.weight ?? "—";

    const grid = document.querySelector(".attributes-grid");
    grid.innerHTML = "";

    data.top_attributes.forEach(attr => {
        const chip = document.createElement("div");
        chip.className = "attribute-chip";
        chip.innerText = attr.replace("_", " ");
        grid.appendChild(chip);
    });
}

function goBack() {
    window.location.href = "index.html";
}

loadPlayer();
