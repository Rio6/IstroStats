<%namespace file="utils/list.mako" import="createList" />

<div class="container text-center">

    <h1>IstroStats</h1>

    <div class="row">
        <div class="col-lg">
            <h2>Last 24 Hours</h2>
            <ul id="reports" class="list-group">
                ${createList("Active Players", "Total Games", postfix="-report", default=0)}
            </ul>
        </div>

        <div class="col-lg">
            <h2>Online Players (<span id="player-count">0</span>)</h2>
            <ul class="list-group" id="players"></ul>
        </div>
    </div>
</div>
</div>
