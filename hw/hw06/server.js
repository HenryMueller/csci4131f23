const data = require("./data");

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

// getting the main page
app.get(['/', '/main'], async (req, res) => {
    res.render("mainpage.pug");
});

// getting the contact page
app.get('/contact', async (req, res) => {
    res.render("contactform.pug");
});

// adding the new contact to the array of dictionaries
app.post('/contact', async (req, res) => {
    let statusCode = await data.addContact(req.body);

    if (statusCode == 201) {
        res.status(statusCode).render("contactform.pug");
    }
    else {
        res.status(statusCode).render("400.pug");
    }
});

// getting the testimonies file
app.get('/testimonies', async (req, res) => {
    res.render("testimonies.pug");
});

// getting the contact log (auth needed)
app.get('/admin/contactlog', auth, async (req, res) => {
    let contacts = await data.getContacts();
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.render("contactlog.pug", { contacts });
});

// deleting a contact from contacts (auth needed)
app.delete('/api/contact', auth, async (req, res) => {
    let contacts = await data.getContacts();

    res.set({ "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0" });
    
    for (let contact of contacts) {
        if (contact["id"] == req.body["id"]) {
            const packet = await data.deleteContact(contact["id"]);

            if (packet["affectedRows"] == 1) {
                res.status(200).send("contact deleted");
            }
            else {
                res.status(400).send("contact not found");
            }
        }
    }
});

// getting the current sale if there is one
app.get('/api/sale', async (req, res) => {
    const recents = await data.getRecentSales();

    res.status(200).send(recents[0]);
});

// make a new sale (auth needed)
app.post('/api/sale', auth, async (req, res) => {
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });

    if ((typeof req.body["message"]) != (typeof "str")) {
        res.status(400).send("sale is not a string");
    }
    else {
        const packet = await data.addSale(req.body["message"]);     // the packet returned by the sql req

        if (packet["affectedRows"] != 1) {
            res.status(400).send("there was a problem adding the sale");
        }
        else {
            res.status(200).send("sale posted");
        }
    }
});

// end all active sales (auth needed)
app.delete('/api/sale', auth, async (req, res) => {
    const packet = await data.endSale();
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.status(200).send("deleted sale")
});

// get 3 most recent sales from database (auth needed)
app.get('/admin/salelog', auth, async (req, res) => {
    const recents = await data.getRecentSales();
    res.set({
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"
    });
    res.status(200).send(recents);
});

// fallthrough function, returns 404 page
app.use((req, res, next) => {
    res.status(404).render("404.pug")
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`)
});