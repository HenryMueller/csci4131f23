/*
    This is the main javascript file that will work with the website.
    It  looks at the 'readyState' and if the DOM is not loaded, it adds
    an event listener that fires a function 'domLoaded' that will add an event 
    listener that will fire a change to the css file being used.
*/
{
    let currCssMode = document.getElementById("css");       // the "link" tag in the html files
    let lightMode = "http://localhost:4131/main.css";
    let darkMode = "http://localhost:4131/main.dark.css";
    let cssButton = document.getElementsByClassName("dark-mode")[0];
    let storedCssMode = localStorage.getItem("cssMode");    // a locally stored css mode variable

    if (currCssMode.href == lightMode && storedCssMode == null) {
        localStorage.setItem("cssMode", "light");
    }
    else if (currCssMode.href == darkMode && storedCssMode == null) {
        localStorage.setItem("cssMode", "dark");
    }

    function domLoaded() {                  // adds event listener to the toggle css mode button
        cssButton.addEventListener("click", toggle_style);
    }

    function toggle_style() {               // function that changes the current page's screen mode
        if (currCssMode.href == lightMode) {
            currCssMode.href = darkMode;
            localStorage.setItem("cssMode", "dark");
        }
        else {
            currCssMode.href = lightMode;
            localStorage.setItem("cssMode", "light");
        }
    }

    if (document.readyState === "loading") { // adds event listener for when the DOM
        window.addEventListener("DOMContentLoaded", domLoaded);
    }
    else {
        domLoaded();
    }


    if (storedCssMode == "light" && currCssMode.href == darkMode) {
        currCssMode.href = lightMode;
    }
    else if (storedCssMode == "dark" && currCssMode.href == lightMode) {
        currCssMode.href = darkMode;
    }
}

{
    window.addEventListener("load", () => {
        let newNode = document.getElementById("sale-banner");
        // let bodyElem = document.querySelector("body");
        // bodyElem.insertBefore(newNode, bodyElem.children[1]);
        console.log(document.querySelector("body").children[1]);

        async function update() {
            const result = await fetch("/api/sale");
            const sale = await result.json();
            console.log(sale);

            if (sale["active"]) {
                newNode.setAttribute("class", "sale");
                newNode.innerText = sale["message"];
            }
            else {
                newNode.removeAttribute("class");
                newNode.innerText = "";
            }
        }
        // update every second
        if (newNode != null) {
            setInterval(update, 1000);
        }
    })
}