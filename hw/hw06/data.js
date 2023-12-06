// this package behaves just like the mysql one, but uses async await instead of callbacks.
const mysql = require(`mysql-await`); // npm install mysql-await

// first -- I want a connection pool: https://www.npmjs.com/package/mysql#pooling-connections
// this is used a bit differently, but I think it's just better -- especially if server is doing heavy work.
var connPool = mysql.createPool({
  connectionLimit: 5, // it's a shared resource, let's not go nuts.
  host: "127.0.0.1",// this will work
  user: "your username",
  database: "your database",
  password: "your password", // we really shouldn't be saving this here long-term -- and I probably shouldn't be sharing it with you...
});

// later you can use connPool.awaitQuery(query, data) -- it will return a promise for the query results.

async function addContact(data){
    // you CAN change the parameters for this function. please do not change the parameters for any other function in this file.

}

async function deleteContact(id){

}

async function getContacts() {

    
}

async function addSale(message) {
    
}

async function endSale() {

}

async function getRecentSales() {

}

module.exports = {addContact, getContacts, deleteContact, addSale, endSale, getRecentSales}