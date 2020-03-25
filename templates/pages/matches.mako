<div class="container">

    <h1 class="text-center">Matches</h1>

    <div>
        <button class="btn btn-secondary" onclick="filter('server')">
            filter server
        </button>
        <button class="btn btn-secondary" onclick="filter('player')">
            filter player
        </button>
        <button class="btn btn-secondary" onclick="filter('type')">
            filter type
        </button>
        <input type="text" id="filter-text" />
    </div>

    <div id="filters"></div>

    <table class="table mt-2">
        <thead><tr>
                <th onclick="sortBy('finished')">Finished</th>
                <th>Server</th>
                <th>Mode</th>
                <th>Winner</th>
                <th onclick="sortBy('time')">Time</th>
                <th>Players</th>
            </tr></thead>
            <tbody id="matches">
                <tr><td>
                    Loading
                </td></tr>
            </tbody>
    </table>

    <ul id="page-button" class="pagination"></ul>
</div>
