window.onload = resizeAllGridItems();
window.addEventListener("resize", resizeAllGridItems);

/* Masonry Grid */
function resizeGridItem(item) {
    const grid = document.getElementsByClassName('image-grid')[0];
    const rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
    const rowSpan = Math.ceil((item.querySelector('.item-content').getBoundingClientRect().height+rowGap)/(rowHeight+rowGap));

    item.style.gridRowEnd = "span "+rowSpan;
}


function resizeAllGridItems(){
    allItems = document.getElementsByClassName("grid-item");
    for(x=0; x<allItems.length; x++){
       resizeGridItem(allItems[x]);
    }
 }


function resizeInstance(instance){
        item = instance.elements[0];
    resizeGridItem(item);
}


function waitForImages() {
    allItems = document.getElementsByClassName("item");
    for(x=0; x<allItems.length; x++){
    imagesLoaded( allItems[x], resizeInstance);
    }
}

waitForImages();