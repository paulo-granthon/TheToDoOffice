window.onload = add_select_el_to_tasks;

function is_selected (e) {
    return e.classList.contains("selected");
}

function add_select_el_to_tasks () {
    var elements = document.getElementsByClassName("task");
    for(var i = 0; i < elements.length; i++) {
        elements[i].addEventListener("click", function(event) {
            if (event.ctrlKey) {
                // console.log("task_select_multi_" + this.id);
                this.children[0].children[2].dispatchEvent(
                    new Event("task_select_multi")
                );
            }
            else {
                // console.log("task_select_" + this.id);
                this.children[0].children[1].dispatchEvent(
                    new Event("task_select")
                );
            }
        });
    }
}

