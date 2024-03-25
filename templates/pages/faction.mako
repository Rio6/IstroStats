<%namespace file="utils/list.mako" import="createList" />

<div class="container">
    <div class="row">
        <div class="col-lg">
            <h3 class="text-center mt-4">Faction Info</h3>
            <ul class="list-group">
                <li class="list-group-item">
                    <span id="name" class="align-middle display-4"></span>
                </li>
                ${createList("Average Rank", "Players", "Last Active", default=0)}
            </ul>
        </div>

        <div class="col-lg">
            <h3 class="mt-4 text-center">Players</h3>
            <ul id="player-list" class="list-group"></ul>
        </div>
    </div>
</div>
