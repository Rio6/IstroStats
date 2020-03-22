var config = {
    order: 'rank',
    orderDes: true,
    onlineOnly: false,
    search: null,
    page: 0,
    rows: 20,
};

var playerData = null;

function updateConfig() {
    config.onlineOnly = $('#online-box').is(':checked');

    let val = $('#search-text').val();
    if(val)
        config.search = `%${val.replace(/%/g, '[%]')}%`;
    else
        config.search = null;

    config.page = 0;
    reload();
}

function sortBy(order) {
    if(config.order === order) {
        config.orderDes = !config.orderDes;
    } else {
        config.order = order
        config.orderDes = true;
    }
    reload();
}

function setPage(page) {
    config.page = page;
    reload();
}

function reload() {
    pollTimeout(reload);

    let data = {
        order: config.order + (config.orderDes ? "_des" : "_asc"),
        ai: false,
        limit: config.rows,
        offset: config.page * config.rows
    };

    if(config.onlineOnly) data.online = true;
    if(config.search) data.search = config.search;

    $.ajax({
        url: '/api/player/',
        data: data,
        success: data => {
            playerData = data;
            refresh();
        }
    });
}

function refresh() {
    if(!playerData) return;

    // players
    $('#players > tr').remove();

    let {count, players} = playerData;

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

    // page buttons

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

$(document).ready(updateConfig);
setInterval(refresh, 1000);
