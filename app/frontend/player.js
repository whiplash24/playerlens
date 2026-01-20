const playerId = localStorage.getItem("playerId");
const playerName = localStorage.getItem("playerName");

if (!playerId) {
    window.location.href = "index.html";
}

async function loadPlayer() {
    const res = await fetch(`http://127.0.0.1:8000/player/${playerId}`);
    const data = await res.json();

    document.getElementById("playerName").innerText = playerName;
    document.getElementById("impactScore").innerText = data.impact_score.toFixed(2);

    document.getElementById("position").innerText = data.position || "—";
    document.getElementById("height").innerText = data.height ?? "—";
    document.getElementById("weight").innerText = data.weight ?? "—";

    // ✅ CORRECT ACCESS
    const breakdown = data.impact_breakdown;

    document.getElementById("abilityScore").innerText =
        breakdown.ability?.toFixed(1) ?? "—";

    document.getElementById("physicalScore").innerText =
        breakdown.physical?.toFixed(1) ?? "—";

    document.getElementById("consistencyScore").innerText =
        breakdown.consistency?.toFixed(1) ?? "—";
}

loadPlayer();
