$(document).ready(() => {
    $.ajax({url: 'https://bootswatch.com/api/4.json', success: data => {
        $('#theme-list > .external-theme').remove();

        for(let theme of data.themes) {
            $('#theme-list').append(e`
                <span class="btn dropdown-item external-theme" onclick="changeTheme('${theme.cssCdn}')">
                    ${theme.name}
                </span>
            `);
        }

        changeTheme(localStorage['theme']);
    }});
});

function changeTheme(cdn) {
    $('#theme-css').attr('href', cdn);
    localStorage['theme'] = cdn;
}
