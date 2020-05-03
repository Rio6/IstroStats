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
function addPageButton(currentPage, rowsPerPage, totalRows) {
    let pages = Math.ceil(totalRows / rowsPerPage) - 1;

    $('#page-button > li').remove()

    let pageBtn = $('#page-button');
    for(let i = 0; i <= pages; i++) {
        if(i > 0 && i < pages && Math.abs(i-currentPage) > 1) {
            pageBtn.append(`
                <li class="page-item disabled">
                    <a class="page-link">...</a>
                </li>
            `);
            if(i < currentPage - 1)
                i = currentPage - 2;
            else if(i > currentPage + 1)
                i = pages - 1;
        } else {
            pageBtn.append(e`
                <li class="page-item ${i === currentPage ? 'active' : ''}" onclick="setPage(${i})">
                    <a href='#' class="page-link">${i}</a>
                </li>
            `);
        }
    }
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
