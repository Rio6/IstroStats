$(document).ready(() => {
    $.ajax({
        url: '/api/player',
        data: {
            online: true,
            order: 'rank_des'
        },
        success: players => {
            for(let player of players) {
                $('#players').append(`
                    <li><a href="/player.html?name=${player.name}">${player.name}</a>
                    ${player.mode}
                    ${player.servers.map(s => `<a href="/server.html?name=${s}">${s}</a>`)}</li>
                `);
            }
        }
    });

    $.ajax({
        url: '/api/server',
        data: {
            order: 'running_des'
        },
        success: servers => {
            for(let server of servers) {
                if(server.hidden) continue;
                $('#servers').append(`
                    <li><a href="/server.html?name=${server.name}">${server.name}</a>
                    ${server.type}
                    ${(() => {
                        if(server.runningSince) {
                            let time = (Date.now() - new Date(server.runningSince*1000)) / 1000;
                            return `${Math.floor(time/60).toString().padStart(2, '0')}:${(time%60).toFixed().padStart(2, '0')}`;
                        } else {
                            return "Not running";
                        }
                    })()}
                `);
            }
        }
    });

    $.ajax({
        url: '/api/match',
        data: {
            order: 'finished_des'
        },
        success: matches => {
            for(let match of matches) {
                $('#matches').append(`
                    <li><a href="/match.html?id=${match.id}">${match.server} ${match.type}
                    ${Math.floor(match.time/60).toString().padStart(2, '0')}:
                    ${(match.time%60).toFixed().padStart(2, '0')}</a></li>
                `);
            }
        }
    });
});
