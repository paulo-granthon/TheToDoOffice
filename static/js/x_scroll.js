
// window.onload = x_scroll_apply;

function x_scroll_apply() {
    const container = document.getElementById("task-list");
    container.addEventListener("wheel", function (e) {
        if (e.deltaY > 0) {
            container.scrollLeft += 100;
            e.preventDefault();
        }
        else {
            container.scrollLeft -= 100;
            e.preventDefault();
        }
    });
    // container.scrollTop(0)
    console.log("scroll added to element")
}
