// this package behaves just like the mysql one, but uses async await instead of callbacks.
const mysql = require(`mysql-await`); // npm install mysql-await

// first -- I want a connection pool: https://www.npmjs.com/package/mysql#pooling-connections
// this is used a bit differently, but I think it's just better -- especially if server is doing heavy work.
var connPool = mysql.createPool({
    connectionLimit: 5, // it's a shared resource, let's not go nuts.
    host: "cse-mysql-classes-01.cse.umn.edu", // this will work WHEN USING SSH, else use '127.0.0.1' or 'localhost'
    user: "C4131F23U149", // username
    database: "C4131F23U149", // name of database
    password: "22251", // we really shouldn't be saving this here long-term -- and I probably shouldn't be sharing it with you...
    port: "3306"
});

/* uncomment if database/tables were destroyed
let sale = { "active": false };

let testContacts = [
    {   // id = 1
        "user": "test",                 // user,
        "id": 1,                        // id
        "email": "testemail@example.com",  // email, 
        "appointment": "2012-5-26",              // email sent day, 
        "qtype": "Question",               // service, 
        "ssn": "Yes"                     // and SSN included
    },
    {
        "user": "Joe Schmo",
        "email": "JoSchmoo@google.com",
        "appointment": "2077-4-1",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Alice Johnson",
        "email": "alice.j@example.com",
        "appointment": "2021-8-15",
        "qtype": "Concern",
        "ssn": "Yes"
    },
    {
        "user": "Bob Smith",
        "email": "bob.smith@example.com",
        "appointment": "2019-3-10",
        "qtype": "Other",
        "ssn": "No"
    },
    {
        "user": "Eva Brown",
        "email": "eva.brown@example.com",
        "appointment": "2020-12-5",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Michael Davis",
        "email": "michael.d@example.com",
        "appointment": "2018-6-20",
        "qtype": "Question",
        "ssn": "No"
    },
    {
        "user": "John Doe",
        "email": "john.doe@example.com",
        "appointment": "2015-11-20",
        "qtype": "Question",
        "ssn": "Yes"
    },
    {
        "user": "Jane Smith",
        "email": "jane.smith@example.com",
        "appointment": "2019-02-14",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Chris Johnson",
        "email": "chris.j@example.com",
        "appointment": "2020-07-30",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Emily White",
        "email": "emily.w@example.com",
        "appointment": "2017-05-12",
        "qtype": "Question",
        "ssn": "No"
    },
    {
        "user": "Daniel Brown",
        "email": "daniel.b@example.com",
        "appointment": "2018-09-08",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Sophia Clark",
        "email": "sophia.c@example.com",
        "appointment": "2016-03-25",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Liam Johnson",
        "email": "liam.j@example.com",
        "appointment": "2023-11-08",
        "qtype": "Question",
        "ssn": "Yes"
    },
    {
        "user": "Olivia Wilson",
        "email": "olivia.w@example.com",
        "appointment": "2023-11-12",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Noah Anderson",
        "email": "noah.a@example.com",
        "appointment": "2023-11-18",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Emma Davis",
        "email": "emma.d@example.com",
        "appointment": "2023-11-23",
        "qtype": "Question",
        "ssn": "No"
    },
    {
        "user": "Liam Smith",
        "email": "liam.s@example.com",
        "appointment": "2023-11-29",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Ava Johnson",
        "email": "ava.j@example.com",
        "appointment": "2023-12-02",
        "qtype": "Question",
        "ssn": "Yes"
    },
    {
        "user": "Ethan White",
        "email": "ethan.w@example.com",
        "appointment": "2023-12-07",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Sophia Martin",
        "email": "sophia.m@example.com",
        "appointment": "2023-12-12",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Mia Brown",
        "email": "mia.b@example.com",
        "appointment": "2023-12-17",
        "qtype": "Question",
        "ssn": "No"
    },
    {
        "user": "James Davis",
        "email": "james.d@example.com",
        "appointment": "2023-12-22",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {
        "user": "Isabella Martinez",
        "email": "isabella.m@example.com",
        "appointment": "2023-12-28",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Liam Harris",
        "email": "liam.h@example.com",
        "appointment": "2023-12-03",
        "qtype": "Question",
        "ssn": "Yes"
    },
    {
        "user": "Olivia Robinson",
        "email": "olivia.r@example.com",
        "appointment": "2023-12-08",
        "qtype": "Comment",
        "ssn": "No"
    },
    {
        "user": "Noah Johnson",
        "email": "noah.j@example.com",
        "appointment": "2023-12-13",
        "qtype": "Comment",
        "ssn": "Yes"
    },
    {   // id = 27
        "user": "Emma Wilson",
        "email": "emma.w@example.com",
        "appointment": "2023-12-18",
        "qtype": "Question",
        "ssn": "No"
    }
];
*/

// later you can use connPool.awaitQuery(query, data) -- it will return a promise for the query results.

/**
 * Adds a row to the contacts table, filling the row with the contact data that is error-checked
 * @param contact the contact object. Contains: Name, ID, Email, Date, Type, and SSN.
 * @return a html status code signifying successful addition to list or failure
 */
async function addContact(newQuery) {
    // you CAN change the parameters for this function. please do not change the parameters for any other function in this file.
    try {
                                                // this was:
        if (typeof newQuery !== 'object' ||     // if (typeof newQuery === 'object' &&
            Array.isArray(newQuery) ||          //     !Array.isArray(newQuery) &&
            newQuery === null)                  //     newQuery !== null)
        {   // if data is not an object, is an array, or is null, it's wrong.
            console.log("first if, returning 400");
            return 400;
        }

        const user = newQuery["user"];
        const email = newQuery["email"];
        const appointment = newQuery["appointment"];
        const qtype = newQuery["qtype"];
        
        let ssn = newQuery["ssn"] ?? "No";
        if (ssn == "No") {
            ssn = false;
        }
        else if (ssn == "Yes" || ssn == "on") {
            ssn = true;
        }
        else {
            console.log("ssn not true or false, return 400");
            return 400;
        }

        if (user == "" || email == "" || appointment == "" || qtype == "") {
            console.log("element is empty, return 400");
            return 400;
        }

        if (user.length > 50 || email.length > 50 || appointment.length > 10 || qtype.length > 8) {
            console.log("element is too long");
            return 400;
        }

        if (newQuery["submit"] != 'Submit') {
            console.log("Innapropriate use of submit")
            return 400;
        }

        const contact = {
            "user": user,
            "email": email,
            "appointment": appointment,
            "qtype": qtype,
            "ssn": ssn
        };

        let retval = await connPool.awaitQuery("INSERT INTO contacts (user, email, appointment, qtype, ssn) VALUES (?, ?, ?, ?, ?)",
            [contact.user, contact.email, contact.appointment, contact.qtype, contact.ssn]);

        if (retval["affectedRows"] != 1) {
            console.log("problem adding the contact")
            return 400;
        }
        
        return 201;
    }
    catch {
        return 400;
    }
}

/**
 * Deletes the specified row from the database for error purposes, we are interested
 * in the "affectedRows" attribute, as it should be 1 if it's a row that is in the 
 * database, 0 if it is not.
 * @param {*} id the id associated with the row to be deleted
 * @returns a packet containing information on the result of the sql command
 */
async function deleteContact(id){
    return await connPool.awaitQuery("DELETE FROM contacts WHERE id=?", [id]);
}

/**
 * Gets all the contacts from the database and formats each row as a json
 * @returns every row from the database as json within an array
 */
async function getContacts() {
    const data = await connPool.awaitQuery("SELECT * FROM contacts");
    let contacts = [];
    
    for (let contact of data) {
        let curDate = contact.appointment;
        let year = String(curDate.getFullYear());
        let month = String(curDate.getMonth() + 1).padStart(2, '0');
        let day = String(curDate.getDate()).padStart(2, '0');

        let appt = `${year}-${month}-${day}`;   // getting only the date

        contacts.push({
            "user": contact.user,
            "id": contact.id,
            "email": contact.email,
            "appointment": appt,
            "qtype": contact.qtype,
            "ssn": ((contact.ssn == 1) ? "Yes" : "No")   // transforming yes/no to true/false
        });
    }

    return contacts;
}

/**
 * Adds a sale to the database and sets its start time as the current time, with the end time as NULL.
 * @param {*} message The text for the sale, i.e. "Black Friday Sale!"
 * @returns a packet that holds information about whether the command was successful
 */
async function addSale(message) {
    endSale();
    
    return await connPool.awaitQuery("INSERT INTO sales (sale) VALUES (?)", message);
}

/**
 * Ends all active sales by setting each of their 'ends' column values to the current time
 * @returns a packet that holds information about whether the command was successful
 */
async function endSale() {  // misleading, should be sales
    const retval = await connPool.awaitQuery("UPDATE sales SET ends = IFNULL(ends, CURRENT_TIMESTAMP)");
    // console.log(retval);
    return retval;
}

/**
 * Gets the 3 most recent sales from the database
 * @returns an array of the three most recent sales as objects, with 'message' and 'active' fields.
 */
async function getRecentSales() {
    const ordered = await connPool.awaitQuery("SELECT sale, begins, ends FROM sales ORDER BY begins DESC LIMIT 0, 3");
    let recents = [];

    for (let item of ordered) {
        recents.push({
            "message": item.sale,
            "active": ((item.ends == null) ? 1 : 0)
        });
    }

    return recents;
}

/* 
// uncomment if 'truncate table contacts' was used
// adding all the testContacts
for (let i = 0; i < 27; i++) {
    addContact(testContacts[i]);
}
*/

module.exports = {addContact, getContacts, deleteContact, addSale, endSale, getRecentSales}