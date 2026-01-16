async function loadPlayer() {
    const playerName = localStorage.getItem("playerName");
    const playerId = localStorage.getItem("playerId");

    const res = await fetch(`http://127.0.0.1:8000/player/${playerId}`);
    const data = await res.json();

    document.getElementById("playerName").innerText = playerName;
    document.getElementById("impactScore").innerText =
        "Impact Score: " + data.impact_score.toFixed(2);

    document.getElementById("position").innerText = data.position;
    document.getElementById("height").innerText = data.height ?? "—";
    document.getElementById("weight").innerText = data.weight ?? "—";

    // Impact Breakdown
    document.querySelectorAll(".breakdown-value")[0].innerText =
        data.impact_breakdown.ability.toFixed(1);

    document.querySelectorAll(".breakdown-value")[1].innerText =
        data.impact_breakdown.physical.toFixed(1);

    document.querySelectorAll(".breakdown-value")[2].innerText =
        data.impact_breakdown.consistency.toFixed(1);

    // Top attributes
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
