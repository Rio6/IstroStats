function elapsed(time) {
    if(!time) return null;
    let sec = (Date.now() - new Date(time*1000)) / 1000;
    if(sec)
        return formatSeconds(sec);
    return null;
}

function formatSeconds(sec) {
    return `${Math.floor(sec/3600).toString().padStart(2, '0')}:${Math.floor(sec%3600/60).toString().padStart(2, '0')}:${(sec%60).toFixed().padStart(2, '0')}`;
}

function formatTime(time) {
    if(!time) return null;
    let date = new Date(time*1000);
    return date.toLocaleString();
}

var poll = null;
function pollTimeout(fn, time=15000) {
    if(poll) clearTimeout(poll);
    poll = setTimeout(() => {
        if(document.visibilityState === 'visible') {
            fn();
        }
        pollTimeout(fn, time);
    }, time);
}

function compare(field, reverse, nulls) {
    return (a, b) => {
        let af = a[field], bf = b[field];
        if(af === null) af = nulls;
        if(bf === null) bf = nulls;
        let rst = af - bf;
        if(isNaN(rst))
            rst = ('' + af).localeCompare(bf)
        if(reverse) rst = -rst;
        return rst;
    };
}

// Calls setPage(page) function when button pressed
function addPageButton(currentPage, rowsPerPage, totalRows, extraBtns=2) {
    let pages = Math.ceil(totalRows / rowsPerPage) - 1;

    $('#page-button > li').remove()

    let pageBtn = $('#page-button');

    pageBtn.append(`
        <li class="page-item" onclick="setPage(0)">
            <a href='#' class="page-link"><</a>
        </li>
    `);

    let numBtns = extraBtns * 2 + 1;
    let startBtn = Math.max(Math.min(currentPage - extraBtns, pages - numBtns), 0);
    let endBtn = Math.min(startBtn + numBtns, pages);
    for(let i = startBtn; i <= endBtn; i++) {
        pageBtn.append(e`
            <li class="page-item ${i === currentPage ? 'active' : ''}" onclick="setPage(${i})">
                <a href='#' class="page-link">${i}</a>
            </li>
        `);
    }

    if(pages > extraBtns*2 + 1) {
        pageBtn.append(`
            <li class="page-item">
                <a class="page-link" style="cursor: pointer;" onclick="(() => {
                    let rst = prompt('Page Number');
                    if(rst != null && !isNaN(rst)) {
                        let page = +rst;
                        setPage(Math.max(Math.min(page, ${pages}), 0));
                    }
                })()">...</a>
            </li>
        `);
    }

    pageBtn.append(`
        <li class="page-item" onclick="setPage(${pages})">
            <a href='#' class="page-link">&gt;</a>
        </li>
    `);
}

function esc(str) {
    if(typeof(str) === 'string') {
        return str
            .replace(/&/g, '&amp;')
            .replace(/>/g, '&gt;')
            .replace(/</g, '&lt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&apos;');
    } else {
        return str;
    }
}

// Tagged template function for escaped template
function e(str, ...tags) {
    return str.reduce((a, c, i) => a + esc(tags[i-1]) + c);
}
