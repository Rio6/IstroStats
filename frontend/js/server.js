$(document).ready(() => {
    let param = new URLSearchParams(window.location.search);

    if(param.has('name')) {
        let name = param.get('name')

        $(document).attr('title', `${name}`);

        $.ajax({
            url: '/api/server/',
            data: {
                name: name
            },
            success: server => {
                if(!server) return;
                $('#name').text(server.name);
                $('#type').text(server.type);
                $('#state').text(server.state);
                $('#observers').text(server.observers);
                $('#run-time').text(elapsed(server.runningSince) || "Not running");

                for(let player of server.players) {
                    $('#players').append(`
                        <li><a href="/player.html?name=${player.name}">${player.name}</a> AI: ${player.ai} ${player.side}</li>
                    `);
                }
            }
        });
    }
});


