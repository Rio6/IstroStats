var players = {};

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/player/',
        data: {
            online: true,
            order: 'rank_des'
        },
        success: (data) => {
            players = data.players
        }
    });

    $.ajax({
        url: '/api/report/',
        data: {
            days: 1
        },
        success: (data) => {
            report = data;
        }
    });
}

function refresh() {
    if(report) {
        $('#active-players-report').text(report.players);
        $('#total-games-report').text(report.games.total);

        for(let type in report.games.types) {
            $(`#${type}-report`).text(report.games.types[type] || 0);
        }
    }

    if(players) {
        $('#player-count').text(players.length);
        $('#players > li').remove();
        for(let player of players) {
            $('#players').append(`
                <li class="list-group-item">
                    <a href="/player?name=${player.name}">${player.name}</a>
                    ${player.servers.length > 0 ? player.servers.map(s => `<a href="/server?name=${s}">${s}</a>`)
                        : (player.mode || "")}
                </li>
            `);
        }
    }
}

$(document).ready(reload);
setInterval(refresh, 1000);
