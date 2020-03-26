<%namespace file="utils/list.mako" import="createList" />

<div class="container">
    <div class="row">
        <div class="col">
            <h3 class="text-center mt-4">Match Info</h3>
            <ul class="list-group">
                ${createList("Finished", "Server", "Mode", "Winner", "Time")}
            </ul>
        </div>

        <div class="col">
            <h3 class="mt-4 text-center">Players</h3>
            <ul id="players" class="list-group"></ul>
        </div>
    </div>
</div>
