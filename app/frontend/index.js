let players = [];
let filteredPlayers = [];
let selectedPlayer = null;

async function loadPlayers() {
    const res = await fetch("http://127.0.0.1:8000/players");
    players = await res.json();
}

const searchInput = document.getElementById("searchInput");
const resultsDiv = document.getElementById("results");
const searchBtn = document.getElementById("searchBtn");

searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    resultsDiv.innerHTML = "";
    selectedPlayer = null;

    if (!query) {
        resultsDiv.style.display = "none";
        return;
    }

    filteredPlayers = players
        .filter(p => p.player_name.toLowerCase().includes(query))
        .slice(0, 10);

    if (filteredPlayers.length === 0) {
        resultsDiv.innerHTML = `<div class="result-item muted">No players found</div>`;
        resultsDiv.style.display = "block";
        return;
    }

    filteredPlayers.forEach(player => {
        const div = document.createElement("div");
        div.className = "result-item";
        div.innerText = player.player_name;

        div.onclick = () => {
            searchInput.value = player.player_name;
            selectedPlayer = player;
            resultsDiv.innerHTML = "";
            resultsDiv.style.display = "none";
        };

        resultsDiv.appendChild(div);
    });

    resultsDiv.style.display = "block";
});

searchBtn.addEventListener("click", () => {
    // Auto-pick first match if user didn't click dropdown
    if (!selectedPlayer) {
        if (filteredPlayers.length === 0) {
            alert("No matching player found.");
            return;
        }
        selectedPlayer = filteredPlayers[0];
    }

    localStorage.setItem("playerId", selectedPlayer.player_api_id);
    localStorage.setItem("playerName", selectedPlayer.player_name);
    window.location.href = "player.html";
});

loadPlayers();
