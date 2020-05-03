var name = null;
var server = null;

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/server/',
        data: {
            name: name
        },
        success: data => {
            server = data.servers[0];
            refresh();
        }
    });
}

function refresh() {
    $('#name').text(name);

    if(!server) return;
    $('#name').text(server.name);
    $('#mode').text(server.type);
    $('#state').text(server.state);
    $('#players').text(server.observers);
    $('#running-for').text(elapsed(server.runningSince) || "Not running");

    $('#player-list > li').remove();

    server.players.sort(compare('side'));
    for(let player of server.players) {
        player.name = player.name.substring(0, 20);
        $('#player-list').append(`
            <li class="list-group-item">
                <div class="text-right float-left pr-1 w-50">
                    ${!player.ai ? e`
                        <a href="/player?name=${player.name}">
                            ${player.name}
                        </a>
                    ` : esc(player.name)}
                </div>
            `+e`<div class="text-left float-right pl-1 w-50">
                    ${player.side}
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
    }
});

setInterval(refresh, 1000);
