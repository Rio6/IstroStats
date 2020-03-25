<div class="container">
    <div class="row">
        <div class="col">
            <h3 class="text-center mt-4">Player Info</h3>
            <ul class="list-group">
                <li class="list-group-item">
                    <span id="name" class="align-middle display-4"></span>
                    <img id="rank-img" class="float-right rounded-circle invisible" width="80px" height="80px" />
                </li>
                % for item in ("Rank", "Faction", "Color", "Mode", "Server", "Online Time", "Last Active", "Games Played", "Win Rate"):
                    <li class="list-group-item">
                        <strong>${item}:</strong> <span id="${item.lower().replace(' ', '-')}"></span>
                    </li>
                % endfor

                % for item in ("1v1", "1v1r", "1v1t", "2v2", "3v3"):
                    <li class="list-group-item">
                        <strong>${item}:</strong> <span id="${item}-rate"></span>
                    </li>
                % endfor
            </ul>
        </div>

        <div class="col">
            <h3 class="mt-4 text-center">Recent Matches</h3>
            <ul id="matches" class="list-group"></ul>
        </div>
    </div>
</div>
