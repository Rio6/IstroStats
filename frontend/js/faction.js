var name = null;
var faction = null;

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/faction/',
        data: {
            name: name
        },
        success: data => {
            faction = data.factions[0];
            refresh();
        }
    });
}

function refresh() {
    $('#name').text(name);

    if(!faction) return;
    $('#rank').text(Math.round(faction.rank));
    $('#player-count').text(faction.players.length);
    $('#last-active').text(formatTime(faction.lastActive));

    $('#players > li').remove();

    faction.players.sort((a, b) => b.lastActive - a.lastActive);
    for(let player of faction.players) {
        $('#players').append(`
            <li class="list-group-item">
                <div class="text-right float-left pr-1 w-50">
                    <a href="/player.html?name=${player.name}">
                        ${player.name}
                    </a>
                </div>
                <div class="text-left float-right pl-1 w-50">
                    ${elapsed(player.logonTime) || formatTime(player.lastActive)}
                </div>
            </li>
        `);
    }
}

$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('name')) {
        name = param.get('name')
        $(document).attr('title', name);
        reload();
        refresh();
    }
});

setInterval(refresh, 1000);

