
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
            server = data;
            refresh();
        }
    });
}

function refresh() {
    $('#name').text(name);

    if(!server) return;
    $('#name').text(server.name);
    $('#type').text(server.type);
    $('#state').text(server.state);
    $('#observers').text(server.observers);
    $('#run-time').text(elapsed(server.runningSince) || "Not running");

    $('#players > li').remove();

    for(let player of server.players) {
        $('#players').append(`
            <li class="list-group-item">
                <div class="text-right float-left pr-1 w-50">
                    ${!player.ai ? `
                        <a href="/player.html?name=${player.name}">
                            ${player.name}
                        </a>
                    ` : player.name}
                </div>
                <div class="text-left float-right pl-1 w-50">
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
        refresh();
    }
});

//setInterval(refresh, 1000);
