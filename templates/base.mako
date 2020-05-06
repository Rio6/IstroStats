<%page args="page, root" />

## Setting subresource integrity can force browsers to reload scripts when updated
<%!
    import os
    import base64
    import hashlib
    cached_integrities = {}
%>
<%
    def with_sri(path):
        global cached_integrities
        if path not in cached_integrities:
            filepath = os.path.join(root, 'static/' + path)
            try:
                with open(filepath, 'rb') as file:
                    content = file.read()
                    integrity='sha384-' + base64.b64encode(hashlib.sha384(content).digest()).decode()
                    cached_integrities[path] = f'"{path}" integrity="{integrity}"'
            except Exception as e:
                print("Error with_sri:", e)
                cached_integrities[path] = f'"{path}"'

        return cached_integrities[path]
%>

<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <link rel="stylesheet" href=${with_sri('/css/sticky-footer.css')}>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <link id="theme-css" rel="stylesheet" crossorigin="anonymous">

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-165749121-1"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'UA-165749121-1');
        </script>


        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

        <script src=${with_sri('/js/utils.js')}></script>
        <script src=${with_sri('/js/themes.js')}></script>
        <script src=${with_sri(f'/js/{page}.js')}></script>
        <title>IstroStats</title>
    </head>

    <body>

        <%def name="navitem(title, path)">
            % if path == page or path == "" and page == "index":
                <a class="nav-link active">${title}</a>
            % else:
            <a class="nav-link" href="/${path}">${title}</a>
            % endif
        </%def>

        <nav class="nav shadow-sm">
            % for (title, path) in (("Home", ""), ("Players", "players"), ("Factions", "factions"), ("Servers", "servers"), ("Matches", "matches")):
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
                    <span class="btn dropdown-item" onclick="changeTheme(null)">
                        Default
                    </span>

                    <div id="theme-list"></div>

                    <span class="text-muted pl-2">
                        <small>
                            Themes from <a href="https://bootswatch.com/" target="_blank">Bootswatch</a>
                        </small>
                    </span>
                </div>
            </span>
        </nav>

        <%include file="pages/${page}.mako" />

        <div class="footer bg-transparent text-muted text-center">
            Made by R26
        </div>

        <script>
          if(localStorage['theme']) {
              $('body').hide();
              $('#theme-css').attr('href', localStorage['theme']);
              $('#theme-css').ready(() => $('body').show());
          }
        </script>
    </body>
</html>
