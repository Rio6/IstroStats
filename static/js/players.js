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
        $('#players').append(e`
            <tr>
                <td><a href="/player?name=${player.name}">${player.name}</a></td>
             `+`<td>${player.faction ? e`<a href="/faction?name=${player.faction}">${player.faction}</a>` : ''}</td>
            `+e`<td>${player.rank}</td>
             `+`<td>${player.servers.map(s => e`<a href="/server?name=${s}">${s}</a>`)}</td>
            `+e`<td>${player.mode || ""}</td>
                <td>
                    ${elapsed(player.logonTime) || formatTime(player.lastActive)}
                </td>
            </tr>
        `);
    }

    // page buttons
    addPageButton(config.page, config.rows, count);
}

$(document).ready(updateConfig);
setInterval(refresh, 1000);
