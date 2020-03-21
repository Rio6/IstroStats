$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('name')) {
        let name = param.get('name')

        $(document).attr('title', name);

        $.ajax({
            url: '/api/player/',
            data: {
                name: name
            },
            success: player => {
                if(!player) return;
                $('#name').text(player.name);
                $('#rank').text(player.rank);
                $('#faction').text(player.faction);
                $('#color').text(player.color);
                $('#mode').text(player.mode);
                $('#online-since').text(player.logonTime && new Date(player.logonTime*1000) || 'Offline');
                $('#last-active').text(new Date(player.lastActive*1000));
            }
        });

        $.ajax({
            url: '/api/match/',
            data: {
                player: name
            },
            success: matches => {
                let win = 0, lose = 0, total = 0;
                for(let match of matches) {
                    let player = match.players.find(p => p.name == name);
                    if(!player) continue;
                    if(player.side == match.winningSide)
                        win++;
                    else
                        lose++
                    total++
                }

                $('#wins').text(`${win}/${total} ${(win/total*100).toFixed(0)}%`);
                $('#loses').text(`${lose}/${total} ${(lose/total*100).toFixed(0)}%`);
            }
        });
    }
});
