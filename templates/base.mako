<%page args="page" />
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <link rel="stylesheet" href="/css/sticky-footer.css">
        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
        <script src="/js/utils.js"></script>
        <script src="/js/${page}.js"></script>
        <title>IstroStats</title>
    </head>
    <body>

        <%def name="navitem(title, path)">
            % if path == page:
                <a class="nav-link active">${title}</a>
            % else:
            <a class="nav-link" href="/${path}">${title}</a>
            % endif
        </%def>

        <nav class="nav border">
            % for (title, path) in (("Home", "index"), ("Players", "players"), ("Factions", "factions"), ("Servers", "servers"), ("Matches", "matches")):
                ${navitem(title, path)}
            % endfor
            <a class="btn btn-primary btn-sm ml-auto mt-1 mr-1 h-75" target="_blank" href="https://www.patreon.com/user?u=32408791">
                Help to run the server
            </a>
        </nav>

        <%include file="pages/${page}.mako" />

        <div class="footer text-muted bg-light text-center">
            Made by R26
        </div>
    </body>
</html>
