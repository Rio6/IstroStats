var config = {
    reloadTime: 10
};

var datas = {};

var reloadTimeout = null;

function reload() {

    if(reloadTimeout) clearTimeout(reloadTimeout);
    reloadTimeout = setTimeout(reload, config.reloadTime * 1000);

    $.ajax({
        url: '/api/player/',
        data: {
            online: true,
            order: 'rank_des'
        },
        success: ({players}) => {
            datas.players = players;
        }
    });

    $.ajax({
        url: '/api/server/',
        data: {
            order: 'running_des'
        },
        success: ({servers}) => {
            datas.servers = servers;
        }
    });

    $.ajax({
        url: '/api/match/',
        data: {
            order: 'finished_des',
            limit: 20
        },
        success: ({matches}) => {
            datas.matches = matches;
        }
    });
}

function refresh() {
    if(datas.players) {
        $('#players > li').remove();
        for(let player of datas.players) {
            $('#players').append(`
                <li class="list-group-item">
                    <a href="/player.html?name=${player.name}">${player.name}</a>
                    ${player.servers.length > 0 ? player.servers.map(s => `<a href="/server.html?name=${s}">${s}</a>`)
                        : player.mode}
                </li>
            `);
        }
    }

    if(datas.servers) {
        $('#servers > li').remove();
        for(let server of datas.servers) {
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

    if(datas.matches) {
        $('#matches > li').remove();
        for(let match of datas.matches) {
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
}

$(document).ready(reload);
setInterval(refresh, 1000);
