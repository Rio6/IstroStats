<%def name="createList(*items, postfix='', default='')">
    % for item in items:
        <li class="list-group-item">
            <strong>${item}:</strong> <span id="${item.lower().replace(' ', '-')}${postfix}">${default}</span>
        </li>
    % endfor
</%def>
