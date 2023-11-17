let url = "http://myCoolServer.com/expenses";
let response = await fetch(url);
let total = 0;
async function getExpenseSum() {
    let journal = await response.json();
    for (let day in journal.res) {
        total += day["amount"];
    }
    return total;
}

function sum1(a, b) {
    setTimeout(() => {
        return a + b
    }, 100);
}

async function sum2(a, b) {
    return a + b;
}