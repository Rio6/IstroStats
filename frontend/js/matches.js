var config = {
    order: 'finished',
    orderDes: true,
    filters: {
        server: [],
        player: [],
        type: []
    },
    page: 0,
    rows: 20,
};

var matchData = null;

function filter(field) {
    let value = $('#filter-text').val();
    if(value && !config.filters[field].includes(value)) {
        config.filters[field].push(value);
        config.page = 0;
        reload();
    }
    $('#filter-text').val("");
}

function removeFilter(field, id) {
    config.filters[field].splice(id, 1);
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

    for(let f in config.filters) {
        if(config.filters[f].length > 0) {
            data[f] = config.filters[f];
        }
    }

    if(config.onlineOnly) data.online = true;

    $.ajax({
        url: '/api/match/',
        data: $.param(data, true), // required to send array to cherrypy
        success: (data) => {
            matchData = data;
            refresh();
        }
    });
}

function refresh() {
    if(!matchData) return;

    // filter tags
    $('#filters > div').remove();
    for(let field in config.filters) {
        let filters = config.filters[field]
        for(let i in filters) {
            $('#filters').append(`
            <div class="btn btn-info" onclick="removeFilter('${field}', ${i})">
                ${field}=${filters[i]}
            </div>
        `);
        }
    }

    // matches
    $('#matches > tr').remove();

    let {count, matches} = matchData;

    for(let match of matches) {
        match.players.forEach(p => {
            p.name = p.name.substring(0, 20);
        });

        $('#matches').append(`
            <tr>
                <td><a href="/match.html?id=${match.id}">${formatTime(match.finished)}</a></td>
                <td><a href="/server.html?name=${match.server}">${match.server}</a></td>
                <td>${match.type}</td>
                <td>${match.winningSide || "none"}</td>
                <td>${formatSeconds(match.time)}</td>
                <td>${
                    match.players
                        .sort((a, b) => b.winner - a.winner)
                        .map(p => p.ai ? p.name : `<a href="/player.html?name=${p.name}">${p.name}</a>`)
                }</td>
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
