<%namespace file="utils/list.mako" import="createList" />

<div class="container">
    <div class="row">
        <div class="col">
            <h3 class="text-center mt-4">Player Info</h3>
            <ul class="list-group">
                <li class="list-group-item">
                    <span id="name" class="align-middle display-4"></span>
                    <img id="rank-img" class="float-right rounded-circle invisible" width="80px" height="80px" />
                </li>
                ${createList("Rank", "Faction", "Color", "Mode", "Server", "Online Time", "Last Active", "Games Played", "Win Rate")}
                ${createList("1v1", "1v1r", "1v1t", "2v2", "3v3", postfix='-rate')}
            </ul>
        </div>

        <div class="col">
            <h3 class="mt-4 text-center">Recent Matches</h3>
            <ul id="matches" class="list-group"></ul>
        </div>
    </div>
</div>
