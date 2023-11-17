/*
    In the space below, write a simple expressjs server file. The server should respond to POST requests generated from the following HTML form:

    <form action="/qsix" method="post">
        <input type="text" required name="username">
        <input type="password" name=password">
        <input type="submit">
    </form>

    If the data sent is username "admin" and password "password" respond with "OK".
    If the data sent is any other username and password response with "no".
    If the data sent does not include a password, respond with "try again".
*/
const e = require('express');
const express = require('express');
const app = express();
const port = 4567;

app.use(express.urlencoded({ extended: true }));

app.post('/qsix', (req, res) => {
    const { name, pass } = req.body;
    if (name && pass) {
        if (user == 'admin' && pass == 'password') {
            res.send('OK');
        }
        else {
            res.send('no');
        }
    }
    else {
        res.send('need user and pass fields');
    }
})

app.use((req, res, next) => {
    res.status(404).send("Impossible");
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});