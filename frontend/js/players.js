var config = {
    order: 'name',
    orderDes: true,
    onlineOnly: false,
    page: 0,
    rows: 20
};

function updateConfig() {
    config.onlineOnly = $('#online-box').is(':checked');
    config.page = 0;
    refresh();
}

function sortBy(order) {
    if(config.order === order) {
        config.orderDes = !config.orderDes;
    } else {
        config.order = order
        config.orderDes = true;
    }
    refresh();
}

function setPage(page) {
    config.page = page;
    refresh();
}

function refresh() {
    $('#players > tr').remove();

    let data = {
        order: config.order + (config.orderDes ? "_des" : "_asc"),
        ai: false,
        limit: config.rows,
        offset: config.page * config.rows
    };

    if(config.onlineOnly) data.online = true;

    $.ajax({
        url: '/api/player/',
        data: data,
        success: ({count, players}) => {
            for(let player of players) {
                let online = elapsed(player.logonTime);
                $('#players').append(`
                    <tr>
                        <td><a href="/player.html?name=${player.name}">${player.name}</a></td>
                        <td>${player.rank}</td>
                        <td>${player.servers.map(s => `<a href="/server.html?name=${s}">${s}</a>`)}</td>
                        <td>${player.mode}</td>
                        <td>
                            ${online || formatTime(player.lastActive)}
                        </td>
                    </tr>
                `);
            }

            $('#page-button > li').remove()
            let pageBtn = $('#page-button');
            pageBtn.append(`
                <li class="page-item ${config.page === 0 ? 'disabled"' : `" onclick="setPage(${config.page-1})`}">
                    <a href='#' class="page-link">&lt;</a href='#'>
                </li>
            `);

            let pages = Math.floor(count / config.rows);
            for(let i = 0; i <= pages; i++) {
                if(i > 0 && i < pages && Math.abs(i-config.page) > 1) {
                    pageBtn.append(`
                        <li class="page-item disabled">
                            <a class="page-link">...</a>
                        </li>
                    `);
                    if(i < config.page - 1)
                        i = config.page - 2;
                    else if(i > config.page + 1)
                        i = pages - 1;
                } else {
                    pageBtn.append(`
                        <li class="page-item ${i === config.page ? 'active' : ''}" onclick="setPage(${i})">
                            <a href='#' class="page-link">${i}</a>
                        </li>
                    `);
                }
            }
            pageBtn.append(`
                <li class="page-item ${config.page >= Math.floor(count/config.rows)
                        ? 'disabled"' : `" onclick="setPage(${config.page+1})"`}>
                    <a href='#' class="page-link">&gt;</a>
                </li>
            `);
        }
    });
}

$(document).ready(updateConfig);

