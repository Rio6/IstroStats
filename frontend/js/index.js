$(document).ready(() => {
    $.ajax({
        url: '/api/player/',
        data: {
            online: true,
            order: 'rank_des'
        },
        success: ({players}) => {
            for(let player of players) {
                $('#players').append(`
                    <li class="list-group-item">
                        <a href="/player.html?name=${player.name}">${player.name}</a>
                        ${player.servers.length > 0 ? player.servers.map(s => `<a href="/server.html?name=${s}">${s}</a>`)
                            : player.mode}
                    </li>
                `);
            }
        }
    });

    $.ajax({
        url: '/api/server/',
        data: {
            order: 'running_des'
        },
        success: ({servers}) => {
            for(let server of servers) {
                if(server.hidden) continue;
                $('#servers').append(`
                    <li class="list-group-item">
                        ${server.type}
                        <a href="/server.html?name=${server.name}">${server.name}</a>
                        ${elapsed(server.runningSince) || "Not running"}
                    </li>
                `);
            }
        }
    });

    $.ajax({
        url: '/api/match/',
        data: {
            order: 'finished_des',
            limit: 20
        },
        success: ({matches}) => {
            for(let match of matches) {
                $('#matches').append(`
                    <li class="list-group-item">
                        <a href="/match.html?id=${match.id}">
                            ${match.type} ${match.server}
                        </a>
                        ${Math.floor(match.time/60).toString().padStart(2, '0')}:
                        ${(match.time%60).toFixed().padStart(2, '0')}
                    </li>
                `);
            }
        }
    });
});
