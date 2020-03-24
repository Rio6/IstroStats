var id = null;
var match = null;

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/match/',
        data: {
            id: id
        },
        success: data => {
            match = data.matches[0];
            refresh();
        }
    });
}

function refresh() {
    if(!match) return;

    $(document).attr('title', `${match.type} ${match.server}`);

    $('#finished').text(formatTime(match.finished));
    $('#server').html(`<a href="/server.html?name=${match.server}">${match.server}</a>`);
    $('#type').text(match.type);
    $('#winning-side').text(match.winningSide || "none");
    $('#time').text(formatSeconds(match.time));

    $('#players > li').remove();

    match.players.sort(compare('winner', true));
    for(let player of match.players) {
        player.name = player.name.substring(0, 20);
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
