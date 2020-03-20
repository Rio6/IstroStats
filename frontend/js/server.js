$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('name')) {
        let name = param.get('name')

        $(document).attr('title', `${name}`);

        $.ajax({
            url: '/api/server',
            data: {
                name: name
            },
            success: server => {
                if(!server) return;
                $('#name').text(server.name);
                $('#type').text(server.type);
                $('#state').text(server.state);
                $('#observers').text(server.observers);
                if(server.runningSince) {
                    let time = (Date.now() - new Date(server.runningSince*1000)) / 1000;
                    $('#run-time').text(`${Math.floor(time/60).toString().padStart(2, '0')}:${(time%60).toFixed().padStart(2, '0')}`);
                } else {
                    $('#run-time').text("Not running");
                }

                for(let player of server.players) {
                    $('#players').append(`
                        <li><a href="/player.html?name=${player.name}">${player.name}</a> AI: ${player.ai} ${player.side}</li>
                    `);
                }
            }
        });
    }
});


