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

        $('#reports > .type-report').remove();
        for(let type of Object.keys(report.games.types).sort()) {
            $(`#reports`).append(e`
                <li class="type-report list-group-item">
                    <strong>${type}:</strong>
                    ${report.games.types[type] || 0}
                </li>
            `);
        }
    }

    if(players) {
        $('#player-count').text(players.length);
        $('#players > li').remove();
        for(let player of players) {
            $('#players').append(e`
                <li class="list-group-item">
                    <a href="/player?name=${player.name}">${player.name}</a>
                 `+`${player.servers.length > 0
                        ? player.servers.map(s => e`<a href="/server?name=${s}">${s}</a>`)
                        : esc(player.mode || "")
                    }
                </li>
            `);
        }
    }
}

$(document).ready(reload);
setInterval(refresh, 1000);
