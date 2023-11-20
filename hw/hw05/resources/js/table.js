{   // code for creating the admin interface
    
    window.addEventListener("load", () => {

        const setTarg = document.getElementById("set-sale");
        
        const delTarg = document.getElementById("del-sale");

        setTarg.addEventListener("click", async () => {
            const inSet = document.getElementById("sale-input").value;

            const result = await fetch("/api/sale", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "message": inSet })
            });
            document.getElementById("sale-input").value = "";
        })

        delTarg.addEventListener("click", async () => {
            const result = await fetch("/api/sale", {
                method: "DELETE",
                headers: {},
                body: JSON.stringify(),
            });
        })

    })
}

{   // Code for Deleting a row of the table
    
    window.addEventListener("load", async () => {

        let deleteButtons = document.querySelectorAll("button.delete");
        let tableRows = document.querySelectorAll("tr");

        let i = 0;
        // looping through table rows
        for (i; i < deleteButtons.length; i++) {
            let thisButton = deleteButtons.item(i);

            // adding event listeners to every button
            thisButton.addEventListener("click", async () => {
                let targetRowNum = thisButton.className.split("R")[1];
                let currRow = document.getElementById("tRow" + targetRowNum);
                let delTarg = {};

                if (currRow != null) {
                    delTarg = { 'id': targetRowNum };
                }

                const result = await fetch("/api/contact", {
                    method: "DELETE",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(delTarg)
                });

                if (result.status != 400 && result.status != 404) {
                    currRow.parentNode.removeChild(currRow);
                }
            })
        }
    })
}

{   // Code for counting down the time until the date on every row
    
    let dateList = document.querySelectorAll("td.countDown");
    window.setInterval(updateTime, 1000);

    function updateTime() {
        let liveTime = Date.now();          // the current real-life time
        /* console.log("liveTime:");
        console.log(liveTime); */

        for (let i = 0; i < dateList.length; i++) {
            
            // console.log("For loop i = " + i);
            let currDate = dateList.item(i).innerHTML.split(" ")[0];      // the dateList Element's time
            /* console.log("currDate:");
            console.log(currDate); */
            if (currDate.indexOf("PAST") >= 0) {            // don't do anything if the date has passed
                continue;
            }

            let currDatified = Date.parse(currDate);        // currDate's date in milliseconds
            /* console.log("currDatified:");
            console.log(currDatified); */

            let timeUntil = (currDatified - liveTime);      // time until the currDate happens
            /* console.log("timeUntil:");
            console.log(timeUntil); */

            if (timeUntil < 0) {
                dateList.item(i).innerHTML = `${currDate} - PAST`;  // template literal for the PAST case
            }
            else {
                /* let tUntilDate = new Date(timeUntil);
                console.log("tUntilDate:");
                console.log(tUntilDate); */
                let untilD = Math.floor(timeUntil / 86400000);                          // days until
                /* console.log("untilD:");
                console.log(untilD); */
                timeUntil -= (untilD * 86400000);
                /* console.log("timeUntil after days:");
                console.log(timeUntil); */

                let untilH = Math.floor((timeUntil % 86400000) / 3600000);                          // hours until
                /* console.log("untilH:");
                console.log(untilH); */
                timeUntil -= (untilH * 3600000);
                /* console.log("timeUntil after hours:");
                console.log(timeUntil); */
                
                let untilM = Math.floor(((timeUntil % 86400000) % 3600000) / 60000);                // minutes until
                /* console.log("untilM:");
                console.log(untilM); */
                timeUntil -= (untilM * 60000);
                /* console.log("timeUntil after minutes:");
                console.log(timeUntil); */
                
                let untilS = Math.floor((((timeUntil % 86400000) % 3600000) % 60000) / 1000);       // seconds until
                /* console.log("untilS:");
                console.log(untilS);
                console.log("timeUntil after seconds:");
                console.log(timeUntil); */
                
                dateList.item(i).innerHTML = `${currDate} - ${untilD} days, ${untilH} hours, ${untilM} minutes, ${untilS} seconds left`;
                // ^ template literal for case where date has not happened yet
            }
        }
    }
}