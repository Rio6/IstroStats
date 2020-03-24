var name = null;
var player = null;
var matches = null;

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
        }
    });

    $.ajax({
        url: '/api/match/',
        data: {
            player: name,
            order: 'finished_des',
            limit: 100
        },
        success: data => {
            matches = data.matches;
        }
    });
}

function refresh() {
    $('#name').text(name);

    if(!player) return;
    $('#rank-img').css('background-color', player.color).attr('src', 'http://www.istrolid.com/img/ui/rank/' + rankImage(player.rank));
    $('#rank').text(player.rank);
    if(player.faction)
        $('#faction').html(`<a href="/faction.html?name=${player.faction}">${player.faction}</a>`);
    else
        $('#faction').text('');
    $('#color').text(player.color);
    $('#mode').text(player.mode);
    $('#servers').html(player.servers.map(s => `<a href="/server.html?name=${s}">${s}</a>`));
    $('#online-time').text(elapsed(player.logonTime) || 'Offline');
    $('#last-active').text(formatTime(player.lastActive));

    $('#matches > li').remove();

    let total = 0, games = 0;
    let wins = {
        '1v1': {wins: 0, games: 0},
        '1v1r': {wins: 0, games: 0},
        '1v1t': {wins: 0, games: 0},
        '2v2': {wins: 0, games: 0},
        '3v3': {wins: 0, games: 0}
    };

    if(!matches) return;
    for(let match of matches) {

        let player = match.players.find(p => p.name == name);
        if(!player) continue;

        if(match.winningSide && match.type in wins) {
            for(let type in wins) {
                if(match.type === type) {
                    if(player.winner)
                        wins[type].wins++;
                    wins[type].games++;
                }
            }

            if(player.winner)
                total++;
            games++;
        }

        if(total < 20) {
            $('#matches').append(`
                <li class="list-group-item">
                    <div class="text-right float-left pr-1 w-50">
                        <a href="/match.html?id=${match.id}">
                            ${formatTime(match.finished)}
                        </a>
                    </div>
                    <div class="text-left float-right pl-1 w-50">
                        ${match.type}
                        <a href="/server.html?name=${match.server}">
                            ${match.server}
                        </a>
                        ${match.winningSide ? player.winner ? "won" : "lost" : "draw"}
                    </div>
                </li>
            `);
        }
    }

    $('#games').text(games);
    if(games > 0)
        $('#total-rate').text(`${total}/${games} (${Math.round(total/games*100)}%)`);
    else
        $('#total-rate').text("N/A");

    for(let type in wins) {
        if(wins[type].games > 0) {
            let wins2 = wins[type].wins, games = wins[type].games;
            $(`#${type}-rate`).text(`${wins2}/${games} (${Math.round(wins2/games*100)}%)`);
        } else {
            $(`#${type}-rate`).text("N/A");
        }
    }
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
