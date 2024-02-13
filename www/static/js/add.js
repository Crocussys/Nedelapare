let selectedCircle = null;

function handleCircleClick(circleId) {
    const circles = document.querySelectorAll('.circle');
    circles.forEach((circle, index) => {
    if (index + 1 === circleId) {
        circle.classList.add('selected');
    } else {
        circle.classList.remove('selected');
    }
    });
}

let selectedRectangle = null;

function handleRectangleClick(rectangleId) {
    const rectangles = document.querySelectorAll('.rectangle');
    rectangles.forEach((rectangle, index) => {
    if (index + 1 === rectangleId) {
        rectangle.classList.add('selected');
    } else {
        rectangle.classList.remove('selected');
    }
    });
}

function handleSelectionChange() {
    const selections = document.querySelectorAll('.select-week');
    const additionalFields = document.querySelectorAll('.additionalField');
    selections.forEach((selection, index) => {
        if (selection.value === 'Каждые N недель') {
            additionalFields[index].classList.remove('hidden');
        } else if (selection.value === 'В недели') {
            additionalInputs[index].classList.remove('hidden');
        } else {
            additionalFields[index].classList.add('hidden');
        }
    });
}
