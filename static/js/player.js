var name = null;
var player = null;
var matches = null;
var totalMatches = 0;
var winRates = {
    '1v1': {wins: 0, games: 0},
    '1v1r': {wins: 0, games: 0},
    '1v1t': {wins: 0, games: 0},
    '2v2': {wins: 0, games: 0},
    '3v3': {wins: 0, games: 0}
};

function rankImage(rank) {
    if (rank < 25) {
        return "rank0@2x.png";
    } else if (rank < 75) {
        return "rank1@2x.png";
    } else if (rank < 150) {
        return "rank2@2x.png";
    } else if (rank < 225) {
        return "rank3@2x.png";
    } else if (rank < 300) {
        return "rank4@2x.png";
    } else if (rank < 400) {
        return "rank5@2x.png";
    } else if (rank < 500) {
        return "rank6@2x.png";
    } else if (rank < 600) {
        return "rank7@2x.png";
    } else if (rank < 700) {
        return "rank8@2x.png";
    } else if (rank < 800) {
        return "rank9@2x.png";
    } else if (rank < 1000) {
        return "rank10@2x.png";
    } else if (rank < 1250) {
        return "rank11@2x.png";
    } else if (rank < 1500) {
        return "rank12@2x.png";
    } else if (rank < 2000) {
        return "rank13@2x.png";
    } else if (rank >= 2000) {
        return "rank14@2x.png";
    }
};

function reload() {
    pollTimeout(reload);

    $.ajax({
        url: '/api/player/',
        data: {
            name: name,
            ai: false
        },
        success: data => {
            player = data.players[0];
            if(player) {
                $.ajax({
                    url: '/api/match/',
                    data: {
                        player: name,
                        order: 'finished_des',
                        limit: 15,
                    },
                    success: data => {
                        matches = data.matches;
                        totalMatches = data.count;
                    }
                });
                $.ajax({
                    url: '/api/winrate/',
                    data: {
                        name: name,
                        type: Object.keys(winRates),
                    },
                    success: data => {
                        Object.assign(winRates, data);
                    }
                });
            }
        }
    });
}

function refresh() {
    $('#name').text(name);

    if(!player) return;

    $('#rank-img').css('background-color', player.color).removeClass('invisible');
    if(player.rank > 0)
        $('#rank-img').attr('src', 'http://www.istrolid.com/img/ui/rank/' + rankImage(player.rank));
    else
        $('#rank-img').attr('src', 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');

    $('#rank').text(player.rank);

    if(player.faction)
        $('#faction').html(e`<a href="/faction?name=${player.faction}">${player.faction}</a>`);
    else
        $('#faction').text("");

    $('#color').text(player.color);
    $('#mode').text(player.mode || "");
    $('#server').html(player.servers.map(s => e`<a href="/server?name=${s}">${s}</a>`));
    $('#online-time').text(elapsed(player.logonTime) || 'Offline');
    $('#last-active').text(formatTime(player.lastActive));

    $('#matches > li').remove();

    if(!matches) return;
    for(let match of matches) {

        let matchPlayer = match.players.find(p => p.name == name);
        if(!matchPlayer) continue;

        $('#matches').append(e`
            <li class="list-group-item">
                <div class="text-right float-left pr-1 w-50">
                    <a href="/match?id=${match.id}">
                        ${formatTime(match.finished)}
                    </a>
                </div>
                <div class="text-left float-right pl-1 w-50">
                    ${match.type}
                    <a href="/server?name=${match.server}">
                        ${match.server}
                    </a>
                    ${match.winningSide ? matchPlayer.winner ? "won" : "lost" : "draw"}
                </div>
            </li>
        `);
    }

    $('#games-played').text(totalMatches);

    let totalWins = 0, totalGames = 0;
    for(let type in winRates) {
        let wins = winRates[type].wins;
        let games = winRates[type].games;

        totalWins += wins;
        totalGames += games;

        if(!player.hidden && winRates[type].games > 0) {
            $(`#${type}-rate`).text(`${wins}/${games} (${Math.round(wins/games*100)}%)`);
        } else {
            $(`#${type}-rate`).text("N/A");
        }
    }

    if(!player.hidden && totalGames > 0)
        $('#win-rate').text(`${totalWins}/${totalGames} (${Math.round(totalWins/totalGames*100)}%)`);
    else
        $('#win-rate').text("N/A");
}

$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('name')) {
        name = param.get('name')
        $(document).attr('title', name);
        reload();
        refresh();
    }
});

setInterval(refresh, 1000);
