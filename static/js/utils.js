function openInNewTab(url) {
    window.open(url, '_blank').focus();
}

function open_notes_windows() {
    window.onload = function() {
        document.querySelector('.comment_button').addEventListener("click",
            function() { document.querySelector(".bg-modal").style.display = 'block' });
        document.querySelector('.close').addEventListener("click",
            function() { document.querySelector(".bg-modal").style.display = 'none' });
    }
}


function change_status_visibility(ob_id) {

    current_class = document.getElementById(ob_id).className

    if (current_class == 'not_done') {
        set_new_class = 'pending_approval';
    } else if (current_class == 'pending_approval') {
        set_new_class = 'approved';
    } else if (current_class == 'approved') {
        set_new_class = 'not_approved';
    } else if (current_class == 'not_approved') {
        set_new_class = 'pending_approval';
    }

    document.getElementById(ob_id).className = set_new_class

}