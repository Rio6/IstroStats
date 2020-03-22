var id = null;
var match = null;

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/match/',
        data: {
            matchId: id
        },
        success: data => {
            match = data;
            refresh();
        }
    });
}

function refresh() {
    if(!match) return;

    $(document).attr('title', `${match.type} ${match.server}`);

    $('#finished').text(formatTime(match.finished));
    $('#server').text(match.server);
    $('#type').text(match.type);
    $('#winning-side').text(match.winningSide !== '0' && match.winningSide || "none");
    $('#time').text(formatSeconds(match.time));

    $('#players > li').remove();

    match.players.sort((a, b) => a.winner - b.winner);
    for(let player of match.players) {
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

    if(param.has('id')) {
        id = param.get('id')
        reload();
    }
});

setInterval(refresh, 1000);
