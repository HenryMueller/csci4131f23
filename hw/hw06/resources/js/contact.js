let drop = document.getElementById("drop");
let checkbox = document.getElementById("option1");
let dynamElem = document.getElementById("dynam-elem");
let finalAmount = 1;

drop.addEventListener("change", updatePrice);
checkbox.addEventListener("change", updatePrice);

/* 
    updatePrice() checks to see if the checkbox is checked and finds what option from the dropdown
    is selected. A selected checkbox reduces price by half, and appends a message onto the current 
    one. Otherwise, a Question is $400, Comment is $200, Concern is $600, and Other is $1200.
*/
function updatePrice() {
    let selectedOption = drop.options[drop.selectedIndex].value;

    dynamElem.innerText = "$";
    if (checkbox.checked) {
        finalAmount = 0.5;
    }
    else {
        finalAmount = 1;
    }

    if (selectedOption == "question") {
        finalAmount *= 400;
        dynamElem.innerText += finalAmount + ", what questions could you possibly have?";
    }
    else if (selectedOption == "comment") {
        finalAmount *= 200;
        dynamElem.innerText += finalAmount + ". Honestly, we just don't care.";
    }
    else if (selectedOption == "concern") {
        finalAmount *= 600;
        dynamElem.innerText += finalAmount + " - really? Just report us.";
    }
    else if (selectedOption == "other") {
        finalAmount *= 1200;
        dynamElem.innerText += finalAmount + "... read the title of the page.";
    }

    if (checkbox.checked) {
        dynamElem.innerText += " But we 'preciate your business!";
    }
}
