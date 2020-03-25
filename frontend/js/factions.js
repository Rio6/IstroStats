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
                <td><a href="/faction.html?name=${faction.name}">${faction.name}</a></td>
                <td>${faction.size}</td>
                <td>${Math.round(faction.rank)}</td>
                <td>${formatTime(faction.lastActive)}</td>
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

$(document).ready(reload);
setInterval(refresh, 1000);

