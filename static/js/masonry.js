
function resizeMasonryItem(item) {
    let grid = document.getElementById('main-grid');
    let rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
    let rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'))
    
    let rowSpan = Math.ceil((item.querySelector('.grid-image').getBoundingClientRect().height+rowGap)/(rowHeight+rowGap));

    item.style.gridRowEnd = 'span '+rowSpan;
}