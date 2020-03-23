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
