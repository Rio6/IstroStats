var config = {
    order: 'playercount',
    orderDes: true,
    moreThanOne: true,
    seatch: null,
    page: 0,
    rows: 20,
};

var factionData = null;

function updateConfig() {
    config.moreThanOne = $('#multi-box').is(':checked');

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
        limit: config.rows,
        offset: config.page * config.rows
    };

    if(config.search) data.search = config.search;
    if(config.moreThanOne) data.minplayers = 2;

    $.ajax({
        url: '/api/faction/',
        data: data,
        success: data => {
            factionData = data;
            refresh();
        }
    });
}

function refresh() {
    if(!factionData) return;

    // factions
    $('#factions > tr').remove();

    let {count, factions} = factionData;

    for(let faction of factions) {
        $('#factions').append(`
            <tr>
                <td><a href="/faction?name=${faction.name}">${faction.name}</a></td>
                <td>${faction.size}</td>
                <td>${Math.round(faction.rank)}</td>
                <td>${formatTime(faction.lastActive)}</td>
            </tr>
        `);
    }

    // page buttons
    addPageButton(config.page, config.rows, count);
}

$(document).ready(reload);
setInterval(refresh, 1000);

