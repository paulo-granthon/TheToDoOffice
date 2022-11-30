console.log('folder_input')


function folder_delete (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("folder_delete")
    );
}

function folder_edit (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("folder_edit")
    );
}

// new folder modal select color
function new_folder_modal_select_color (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("folder_sel_color")
    )
}

function super_update () {
    document.querySelector("#sel-tasks-super-updater").dispatchEvent(
        new Event("update")
    )
    // htmx.trigger("#sel-tasks-super-updater", "update")
    console.log("iaushdiouashopdiuhasioudhiouh")
}