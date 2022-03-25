function openInNewTab(url) {
    window.open(url, '_blank').focus();
}


function get_current_status_cleaned(ob_id) {
    current_class = document.getElementById(ob_id).className;
    current_class = current_class.replace("employee_", "");
    return current_class;
}


function clicked_on_circle_manager(ob_id) {
    old_class = get_current_status_cleaned(ob_id)
    change_status_visibility_manager(ob_id);
    new_class = get_current_status_cleaned(ob_id)
    if (old_class != new_class) {
        txt = document.getElementById('id_changes').innerHTML
        if (txt.search(ob_id) != -1) {
            if (txt.search(ob_id + ":not_done") != -1)
                txt = txt.replace(ob_id + ":not_done,", "");
            else if (txt.search(ob_id + ":pending_approval") != -1)
                txt = txt.replace(ob_id + ":pending_approval,", "");
            else if (txt.search(ob_id + ":not_approved") != -1)
                txt = txt.replace(ob_id + ":not_approved,", "");
            else if (txt.search(ob_id + ":approved") != -1)
                txt = txt.replace(ob_id + ":approved,", "");
        }


        new_txt = txt + "'" + ob_id + "'" + ":" + "'" + new_class + "'" + ",";
        document.getElementById('id_changes').innerHTML = new_txt;
        document.getElementById('approve_changes_button').style.display = "inline";
    }
}


function change_status_visibility_manager(ob_id) {

    current_class = document.getElementById(ob_id).className

    if (current_class == 'employee_not_done') {
        set_new_class = 'employee_pending_approval';
    } else if (current_class == 'employee_pending_approval') {
        set_new_class = 'employee_approved';
    } else if (current_class == 'employee_approved') {
        set_new_class = 'employee_not_approved';
    } else if (current_class == 'employee_not_approved') {
        set_new_class = 'employee_not_done';
    }

    document.getElementById(ob_id).className = set_new_class

}


function clicked_on_circle_worker(ob_id) {
    old_class = get_current_status_cleaned(ob_id)
    change_status_visibility_worker(ob_id);
    new_class = get_current_status_cleaned(ob_id)
    if (old_class != new_class) {
        txt = document.getElementById('id_changes').innerHTML
        if (txt.search(ob_id) != -1) {
            if (txt.search(ob_id + ":not_done") != -1)
                txt = txt.replace(ob_id + ":not_done,", "");
            else if (txt.search(ob_id + ":pending_approval") != -1)
                txt = txt.replace(ob_id + ":pending_approval,", "");
            else if (txt.search(ob_id + ":not_approved") != -1)
                txt = txt.replace(ob_id + ":not_approved,", "");
            else if (txt.search(ob_id + ":approved") != -1)
                txt = txt.replace(ob_id + ":approved,", "");
        }


        new_txt = txt + "'" + ob_id + "'" + ":" + "'" + new_class + "'" + ",";
        document.getElementById('id_changes').innerHTML = new_txt;
        document.getElementById('approve_changes_button').style.display = "inline";
    }
}


function change_status_visibility_worker(ob_id) {

    current_class = document.getElementById(ob_id).className

    if (current_class == 'employee_not_done') {
        set_new_class = 'employee_pending_approval';
    } else if (current_class == 'employee_pending_approval') {
        set_new_class = 'employee_not_done';
    } else if (current_class == 'employee_not_approved') {
        set_new_class = 'employee_pending_approval';
    } else if (current_class == 'employee_approved') {
        set_new_class = 'employee_approved';
    }

    document.getElementById(ob_id).className = set_new_class

}