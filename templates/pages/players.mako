<div class="container">

    <h1 class="text-center">Players</h1>

    <div class="form-inline mb-2">
        <button class="btn btn-secondary mr-2" onclick="updateConfig()">
            search
        </button>
        <input type="text" id="search-text" onkeyup="if(event.keyCode === 13) updateConfig();" />
        <span class="form-check ml-2">
            <input id="online-box" type="checkbox" class="form-check-input" onclick="updateConfig()" />
            <label for="online-box">Online only</label>
        </span>
    </div>

    <table class="table">
        <thead><tr>
                <th onclick="sortBy('name')">Name</th>
                <th onclick="sortBy('faction')">Faction</th>
                <th onclick="sortBy('rank')">Rank</th>
                <th>Room</th>
                <th>Mode</th>
                <th onclick="sortBy('logon')">Active</th>
            </tr></thead>
            <tbody id="players" >
                <tr><td>
                    Loading
                </td></tr>
            </tbody>
    </table>

    <ul id="page-button" class="pagination"></ul>
</div>
