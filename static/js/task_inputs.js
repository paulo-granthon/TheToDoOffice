console.log('folder_input')
// window.onload = add_listeners_to_task;

// checks if the task element is selected
function is_selected (e) {
    return e.classList.contains("task-selected");
}

// adds event listeners to the task elements
function add_listeners_to_task () {

    console.log("!!!!!!!!!!!!!!!!! add_listeners_to_task !!!!!!!!!!!!!!!!!")

    // get all .task elements
    var elements = document.getElementsByClassName("task");

    // loop through them
    for(var i = 0; i < elements.length; i++) {

        add_listeners_to_task2(elements[i])
    }
}

function add_listeners_to_task2 (element) {

    // add the event listener 'click' on the task (body)
    element.addEventListener("click", function(event) {

        // if ctrl is being pressed with the click
        if (event.ctrlKey) {

            // trigger the 'task_select_multi' event on the task
            this.querySelector('#task-selection-wrapper').querySelector('#task-select-multi').dispatchEvent(
                new Event("task_select_multi")
            );
        }

        // otherwise
        else {

            // trigger the 'task_select' event on the task
            this.querySelector('#task-selection-wrapper').querySelector('#task-select-single').dispatchEvent(
                new Event("task_select")
            );
        }
    });

    // task complete
    element.querySelector('#task-complete-box').addEventListener("click", function(event) {
        event.stopPropagation();
        this.dispatchEvent(
            new Event("task_complete")
        )
    });

    // task move
    element.querySelector('#task-move-button').addEventListener("click", function(event) {
        event.stopPropagation();
        this.dispatchEvent(
            new Event("task_move")
        )
    });


    // task delete
    element.querySelector('#del-btn').addEventListener("click", function(event) {
        event.stopPropagation();
        this.dispatchEvent(
            new Event("task_delete")
        )
    });
}

function task_select (element, event) {

    console.log(element);

    console.log(event.ctrlKey);

    // if ctrl is being pressed with the click
    if (event.ctrlKey) {

        // trigger the 'task_select_multi' event on the task
        element.querySelector('#task-selection-wrapper').querySelector('#task-select-multi').dispatchEvent(
            new Event("task_select_multi")
        );
    }

    // otherwise
    else {

        // trigger the 'task_select' event on the task
        element.querySelector('#task-selection-wrapper').querySelector('#task-select-single').dispatchEvent(
            new Event("task_select")
        );
    }
}

// task complete
function task_complete (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("task_complete")
    )
    element.querySelector("#checkbox").classList.toggle('check-box-active')
}

// task move
function task_move (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("task_move")
    );
}

// task delete
function task_delete (element, event) {
    event.stopPropagation();
    element.dispatchEvent(
        new Event("task_delete")
    );
}

function log_session() {
    let s = Request.log_session['sel_tasks'];
    console.log(s);
}
