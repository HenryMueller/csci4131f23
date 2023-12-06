const express = require('express');
const app = express();
const port = 4131;

app.set("views", "templates");
app.set("view engine", "pug");

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use("/resources", express.static("resources"));

const basicAuth = require('express-basic-auth');

const auth = basicAuth({
    users: { "admin": "password" },
    challenge: true,
    realm: "User Visible Realm"
});

let sale = { "active": false };

let next_id = 28;
let contacts = [
    {
        "name": "test",                 // name,
        "id": 1,                        // id,
        "email": "testemail@example.com",  // email, 
        "date": "2012-5-26",              // email sent day, 
        "type": "Question",               // service, 
        "ssn": "Yes"                     // and SSN included
    },
    {
        "name": "Joe Schmo",
        "id": 2,
        "email": "JoSchmoo@google.com",
        "date": "2077-4-1",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Alice Johnson",
        "id": 3,
        "email": "alice.j@example.com",
        "date": "2021-8-15",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Bob Smith",
        "id": 4,
        "email": "bob.smith@example.com",
        "date": "2019-3-10",
        "type": "Question",
        "ssn": "No"
    },
    {
        "name": "Eva Brown",
        "id": 5,
        "email": "eva.brown@example.com",
        "date": "2020-12-5",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Michael Davis",
        "id": 6,
        "email": "michael.d@example.com",
        "date": "2018-6-20",
        "type": "Question",
        "ssn": "No"
    },
    {
        "name": "John Doe",
        "id": 7,
        "email": "john.doe@example.com",
        "date": "2015-11-20",
        "type": "Question",
        "ssn": "Yes"
    },
    {
        "name": "Jane Smith",
        "id": 8,
        "email": "jane.smith@example.com",
        "date": "2019-02-14",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Chris Johnson",
        "id": 9,
        "email": "chris.j@example.com",
        "date": "2020-07-30",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Emily White",
        "id": 10,
        "email": "emily.w@example.com",
        "date": "2017-05-12",
        "type": "Question",
        "ssn": "No"
    },
    {
        "name": "Daniel Brown",
        "id": 11,
        "email": "daniel.b@example.com",
        "date": "2018-09-08",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Sophia Clark",
        "id": 12,
        "email": "sophia.c@example.com",
        "date": "2016-03-25",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Liam Johnson",
        "id": 13,
        "email": "liam.j@example.com",
        "date": "2023-11-08",
        "type": "Question",
        "ssn": "Yes"
    },
    {
        "name": "Olivia Wilson",
        "id": 14,
        "email": "olivia.w@example.com",
        "date": "2023-11-12",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Noah Anderson",
        "id": 15,
        "email": "noah.a@example.com",
        "date": "2023-11-18",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Emma Davis",
        "id": 16,
        "email": "emma.d@example.com",
        "date": "2023-11-23",
        "type": "Question",
        "ssn": "No"
    },
    {
        "name": "Liam Smith",
        "id": 17,
        "email": "liam.s@example.com",
        "date": "2023-11-29",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Ava Johnson",
        "id": 18,
        "email": "ava.j@example.com",
        "date": "2023-12-02",
        "type": "Question",
        "ssn": "Yes"
    },
    {
        "name": "Ethan White",
        "id": 19,
        "email": "ethan.w@example.com",
        "date": "2023-12-07",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Sophia Martin",
        "id": 20,
        "email": "sophia.m@example.com",
        "date": "2023-12-12",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Mia Brown",
        "id": 21,
        "email": "mia.b@example.com",
        "date": "2023-12-17",
        "type": "Question",
        "ssn": "No"
    },
    {
        "name": "James Davis",
        "id": 22,
        "email": "james.d@example.com",
        "date": "2023-12-22",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Isabella Martinez",
        "id": 23,
        "email": "isabella.m@example.com",
        "date": "2023-12-28",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Liam Harris",
        "id": 24,
        "email": "liam.h@example.com",
        "date": "2023-12-03",
        "type": "Question",
        "ssn": "Yes"
    },
    {
        "name": "Olivia Robinson",
        "id": 25,
        "email": "olivia.r@example.com",
        "date": "2023-12-08",
        "type": "Comment",
        "ssn": "No"
    },
    {
        "name": "Noah Johnson",
        "id": 26,
        "email": "noah.j@example.com",
        "date": "2023-12-13",
        "type": "Comment",
        "ssn": "Yes"
    },
    {
        "name": "Emma Wilson",
        "id": 27,
        "email": "emma.w@example.com",
        "date": "2023-12-18",
        "type": "Question",
        "ssn": "No"
    }
];

function extractQueries(newQuery) {
    try {
        console.log(newQuery);

        if (typeof newQuery === 'object' &&
            !Array.isArray(newQuery) &&
            newQuery !== null)
        {
            return 400;
        }

        const name = newQuery["name"];
        const email = newQuery["email"];
        const date = newQuery["date"];
        const type = newQuery["drop"];
        const ssn = newQuery["option1"] ?? "No";

        if (name == "" || email == "" || date == "" || type == "") {
            return 400;
        }

        contacts.push({
            "name": name,
            "id": next_id,
            "email": email,
            "date": date,
            "type": type,
            "ssn": ssn
        });

        next_id += 1;
        
        return 201;
    }
    catch {
        return 400;
    }
}

// getting the main page
app.get(['/', '/main'], (req, res) => {
    res.render("mainpage.pug");
});

// getting the contact page
app.get('/contact', (req, res) => {
    res.render("contactform.pug");
});

// adding the new contact to the array of dictionaries
app.post('/contact', (req, res) => {
    let statusCode = extractQueries(req.body);
    if (statusCode == 201) {
        res.status(statusCode).render("contactform.pug");
    }
    else {
        res.status(statusCode).render("400.pug");
    }
});

// getting the testimonies file
app.get('/testimonies', (req, res) => {
    res.render("testimonies.pug");
});

// getting the contact log (auth needed)
app.get('/admin/contactlog', auth, (req, res) => {
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.render("contactlog.pug", { contacts });
    res.send();
});

// deleting a contact from contacts (auth needed)
app.delete('/api/contact', auth, (req, res) => {
    console.log(req.body);
    for (let i = 0; i < contacts.length; i++) {
        let contact = contacts[i];
        if (contact["id"] == req.body["id"]) {
            contacts.splice(i, 1);
            res.set({
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
            });
            res.status(200).send("contact deleted");
        }
    }    
});

// getting the current sale if there is one (auth needed)
app.get('/api/sale', (req, res) => {
    res.status(200).send(sale);
});

// make a new sale (auth needed)
app.post('/api/sale', auth, (req, res) => {
    sale = { "active": true, "message": req.body["message"] };
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.status(200).send("sale posted");
});

app.delete('/api/sale', auth, (req, res) => {
    sale = { "active": false }
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.status(200).send("deleted sale")
});

// fallthrough function, returns 404 page
app.use((req, res, next) => {
    res.status(404).render("404.pug")
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`)
});