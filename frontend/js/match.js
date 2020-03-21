$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('id')) {
        let id = param.get('id')

        $.ajax({
            url: '/api/match/',
            data: {
                matchId: id
            },
            success: match => {
                if(!match) return;
                $(document).attr('title', `${match.type} ${match.server}`);
                $('#server').text(match.server);
                $('#type').text(match.type);
                $('#winning-side').text(match.winningSide);
                let time = match.time;
                $('#time').text(`${Math.floor(time/60).toString().padStart(2, '0')}:${(time%60).toString().padStart(2, '0')}`);
                $('#finished').text(new Date(match.finished*1000));

                for(let player of match.players) {
                    $('#players').append(`
                        <li><a href="/player.html?name=${player.name}">${player.name}</a> AI: ${player.ai} ${player.side}</li>
                    `);
                }
            }
        });
    }
});

