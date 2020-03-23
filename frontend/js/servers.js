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
            </tr>
        `);
    }
}

$(document).ready(reload);
setInterval(refresh, 1000);
