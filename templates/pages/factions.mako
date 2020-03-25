<div class="container">
    <h1 class="text-center">Factions</h1>

    <div class="form-inline mb-2">
        <button class="btn btn-secondary mr-2" onclick="updateConfig()">
            search
        </button>
        <input type="text" id="search-text" onkeyup="if(event.keyCode === 13) updateConfig();" />
        <span class="form-check ml-2">
            <input id="multi-box" type="checkbox" checked class="form-check-input" onclick="updateConfig()" />
            <label for="online-box">More than 1 player</label>
        </span>
    </div>

    <table class="table">
        <thead><tr>
                <th onclick="sortBy('name')">Name</th>
                <th onclick="sortBy('playercount')">Players</th>
                <th onclick="sortBy('rank')">Average Rank</th>
                <th onclick="sortBy('active')">Active</th>
            </tr></thead>
            <tbody id="factions">
                <tr><td>
                    Loading
                </td></tr>
            </tbody>
    </table>

    <ul id="page-button" class="pagination"></ul>
</div>
