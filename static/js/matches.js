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
                <td><a href="/match?id=${match.id}">${formatTime(match.finished)}</a></td>
                <td><a href="/server?name=${match.server}">${match.server}</a></td>
                <td>${match.type}</td>
                <td>${match.winningSide || "none"}</td>
                <td>${formatSeconds(match.time)}</td>
                <td>${
                    match.players
                        .sort((a, b) => b.winner - a.winner)
                        .map(p => p.ai ? p.name : `<a href="/player?name=${p.name}">${p.name}</a>`)
                }</td>
            </tr>
        `);
    }

    // page buttons
    addPageButton(config.page, config.rows, count);
}

$(document).ready(reload);
