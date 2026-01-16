let players = [];

async function loadPlayers() {
    const res = await fetch("http://127.0.0.1:8000/players");
    players = await res.json();
}

function searchPlayer() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    const matches = players.filter(p =>
        p.player_name.toLowerCase().includes(query)
    );

    matches.slice(0, 5).forEach(player => {
        const div = document.createElement("div");
        div.innerText = player.player_name;
        div.onclick = () => {
            localStorage.setItem("playerId", player.player_api_id);
            localStorage.setItem("playerName", player.player_name);
            window.location.href = "player.html";
        };
        resultsDiv.appendChild(div);
    });
}

loadPlayers();
