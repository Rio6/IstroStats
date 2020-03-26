<%page args="page" />
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <link rel="stylesheet" href="/css/sticky-footer.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <link id="theme-css" rel="stylesheet" crossorigin="anonymous">

        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

        <script src="/js/utils.js"></script>
        <script src="/js/themes.js"></script>
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

        <nav class="nav shadow-sm">
            % for (title, path) in (("Home", "index"), ("Players", "players"), ("Factions", "factions"), ("Servers", "servers"), ("Matches", "matches")):
                ${navitem(title, path)}
            % endfor

            <span class="dropdown ml-auto mr-1">
                <a class="mt-1 mr-1 h-75" target="_blank" href="https://www.patreon.com/user?u=32408791">
                    Help to run the server
                </a>

                <button class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Themes
                </button>
                <div class="dropdown-menu">
                    <span class="dropdown-item" onclick="changeTheme(null)">
                        Default
                    </span>

                    <div id="theme-list"></div>

                    <span class="dropdown-item text-muted disabled">
                        <small>
                            Themes from <a href="https://bootswatch.com/">Bootswatch</a>
                        </small>
                    </span>
                </div>
            </span>
        </nav>

        <%include file="pages/${page}.mako" />

        <div class="footer bg-transparent text-muted text-center">
            Made by R26
        </div>
    </body>
</html>
