document.addEventListener("DOMContentLoaded", () => {
    // HTMX: Handle 404 responses to trigger grid resize
    document.body.addEventListener("htmx:responseError", (event) => {
        if (event.detail.xhr.status === 404) {
            resizeAllGridItems(); // Reorganize the grid
        }
    });

    // Recalculate the grid after new content is swapped in
    document.body.addEventListener("htmx:afterSwap", () => {
        resizeAllGridItems();
    });

    // Initial grid setup
    window.onload = resizeAllGridItems();
    window.addEventListener("resize", resizeAllGridItems);
});

/* Masonry Grid */
function resizeGridItem(item) {
    const grid = document.getElementsByClassName('image-grid')[0];
    const rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    // Retrieves the computed 'grid-auto-rows' value from the CSS and converts it to an integer.
    // This represents the default row height defined in the CSS grid.

    const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
    // Retrieves the computed 'grid-row-gap' value from the CSS and converts it to an integer.
    // This represents the vertical spacing between rows in the grid.

    const rowSpan = Math.ceil((item.querySelector('.item-content').getBoundingClientRect().height+rowGap)/(rowHeight+rowGap));
    // Calculates how many rows this particular item should span.
    // It measures the item's content height, adds a row gap, and divides by the total row height (row height + row gap),
    // rounding up with Math.ceil because the item must occupy full rows.

    item.style.gridRowEnd = "span "+rowSpan;
    // Dynamically sets the CSS property to make the item span the calculated number of rows.
}

function resizeAllGridItems(){
    allItems = document.getElementsByClassName("grid-item");
    for(x=0; x<allItems.length; x++){
       resizeGridItem(allItems[x]);
    }
 }

function resizeInstance(instance){
        item = instance.elements[0];
        // Retrieves the first element from the instance's elements array (the item that needs resizing).
    resizeGridItem(item);
}

function waitForImages() {
    allItems = document.getElementsByClassName("item");
    for(x=0; x<allItems.length; x++){
    imagesLoaded( allItems[x], resizeInstance);
    // Uses the imagesLoaded library to call 'resizeInstance' once the images in the given item are fully loaded.
    }
}

waitForImages();