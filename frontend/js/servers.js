var config = {
    order: 'runningSince',
    orderDes: true,
    reloadTime: 10
};

var servers = null;
var reloadTimeout = null;

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

    if(reloadTimeout) clearTimeout(reloadTimeout);
    reloadTimeout = setTimeout(reload, config.reloadTime * 1000);

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

    let compare = (field) => (a, b) => {
        if(config.orderDes)
            return ('' + b[field]).localeCompare(a[field])
        else
            return ('' + a[field]).localeCompare(b[field])
    };

    servers.sort(compare(config.order))

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