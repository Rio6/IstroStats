var config = {
    order: 'runningSince',
    orderDes: true,
};

var servers = null;

function sortBy(order) {
    if(config.order === order) {
        config.orderDes = !config.orderDes;
    } else {
        config.order = order
        config.orderDes = true;
    }
    refresh();
}

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/server/',
        success: data => {
            servers = data.servers;
            refresh();
        }
    });
}

function refresh() {
    if(!servers) return;

    $('#servers > tr').remove();

    servers.sort(compare(config.order, config.orderDes, Infinity))

    for(let server of servers) {
        if(server.hidden) continue;

        server.players.forEach(p => {
            p.name = p.name.substring(0, 20);
        });

        let runTime = elapsed(server.runningSince);
        $('#servers').append(`
            <tr>
                <td><a href="/server.html?name=${server.name}">${server.name}</a></td>
                <td>${server.type}</td>
                <td>${server.state}</td>
                <td>${server.observers}</td>
                <td>
                    ${runTime || "Not running"}
                </td>
                <td>${
                    server.players
                        .filter(p => !p.ai && (p.side === 'alpha' || p.side === 'beta'))
                        .sort((a, b) => b.side - a.side)
                        .map(p => p.ai ? p.name : `<a href="/player.html?name=${p.name}">${p.name}</a>`)
                }</td>
            </tr>
        `);
    }
}

$(document).ready(reload);
setInterval(refresh, 1000);
