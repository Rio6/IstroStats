var config = {
    reloadTime: 10
};

var name = null;
var player = null;
var matches = null;
var reloadTimeout = null;

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

    if(reloadTimeout) clearTimeout(reloadTimeout);
    reloadTimeout = setTimeout(reload, config.reloadTime * 1000);

    $.ajax({
        url: '/api/player/',
        data: {
            name: name
        },
        success: data => {
            player = data;
        }
    });

    $.ajax({
        url: '/api/match/',
        data: {
            player: name,
            order: 'finished_des'
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
    $('#faction').text(player.faction);
    $('#color').text(player.color);
    $('#mode').text(player.mode);
    $('#servers').text(player.servers);
    $('#online-since').text(elapsed(player.logonTime) || 'Offline');
    $('#last-active').text(formatTime(player.lastActive));

    $('#matches > li').remove();

    let win = 0, lose = 0, total = 0;
    for(let match of matches) {

        let player = match.players.find(p => p.name == name);
        if(!player) continue;
        let victory = player.side == match.winningSide;

        if(victory)
            win++;
        else
            lose++
        total++

        if(total < 20) {
            $('#matches').append(`
            <li class="list-group-item">
                <a href="/match.html?id=${match.id}">
                    ${formatTime(match.finished)}
                </a>
                ${match.type}
                <a href="/server.html?name=${match.server}">
                    ${match.server}
                </a>
                ${victory ? "won" : "lost"}
            </li>
        `);
        }
    }

    $('#wins').text(`${win}/${total} ${(win/total*100).toFixed(0)}%`);
    $('#loses').text(`${lose}/${total} ${(lose/total*100).toFixed(0)}%`);
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
