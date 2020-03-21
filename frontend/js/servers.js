var config = {
    order: 'runningSince',
    orderDes: true,
};

function sortBy(order) {
    if(config.order === order) {
        config.orderDes = !config.orderDes;
    } else {
        config.order = order
        config.orderDes = true;
    }
    refresh();
}

function refresh() {
    $('#servers > tr').remove();

    $.ajax({
        url: '/api/server/',
        success: ({servers}) => {

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
    });
}

$(document).ready(refresh);
