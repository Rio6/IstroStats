var config = {
    order: 'finished',
    orderDes: true,
    type: null,
    page: 0,
    rows: 20
};

function updateConfig() {
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
    $('#matches > tr').remove();

    let data = {
        order: config.order + (config.orderDes ? "_des" : "_asc"),
        ai: false,
        limit: config.rows,
        offset: config.page * config.rows
    };

    if(config.onlineOnly) data.online = true;

    $.ajax({
        url: '/api/match/',
        data: data,
        success: ({count, matches}) => {
            for(let match of matches) {
                $('#matches').append(`
                    <tr>
                        <td><a href="/match.html?id=${match.id}">${formatTime(match.finished)}</a></td>
                        <td><a href="/server.html?name=${match.server}">${match.server}</a></td>
                        <td>${match.type}</td>
                        <td>${match.winningSide || "none"}</td>
                        <td>${formatSeconds(match.time)}</td>
                        <td>${match.players.map(({name}) => `<a href="/player.html?name=${name}">${name}</a>`)}</td>
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


