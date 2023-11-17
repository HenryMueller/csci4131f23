// In the space below, write a simple expressjs server. The server should 
// respond to GET requests to the path "/api/names" with a JSON list of 
// names(you can choose these arbitrarily, include at least 3), and appropriate
// headers and status code.

const express = require('express');
const app = express();
const port = 2345;

app.use(express.json())

const names = ["Joe", "Barb", "Rich"];

app.get('/api/names', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.status(200);
    res.json({ names });
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
});