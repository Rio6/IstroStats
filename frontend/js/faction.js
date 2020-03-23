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
        }
    });

    let sendPlayerRequest = (offset=0) => {
        $.ajax({
            url: '/api/player/',
            data: {
                faction: name,
                offset: offset,
            },
            success: nextPlayerData
        });
    };

    let nextPlayerData = data => {
        if(!faction) return;
        if(!faction.players) faction.players = [];

        faction.players.splice(-1, 0, ...data.players);

        if(faction.players.length < data.count) {
            sendPlayerRequest(faction.players.length);
        }
    };

    sendPlayerRequest();
}

function refresh() {
    $('#name').text(name);

    if(!faction) return;
    $('#rank').text(Math.round(faction.rank));
    $('#player-count').text(faction.players.length);
    $('#last-active').text(formatTime(faction.lastActive));

    $('#players > li').remove();

    if(faction.players) {
        faction.players.sort(compare('lastActive', true));
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

