// In the space below, write a simple expressjs server file. The server should respond to PUT requests to the path "/compute" with an HTML page (and appropriate status and headers).

// This request should expect URL-parameters with names "a" and "b". These should have numbers and be provided in standard format (See the example) 
// If either of a or b are not given in the url, or contain non-numerical values you should give them a default value of 1.2
// This page should contains at a minimum html, body, and a header (h1, h2, h3, etc.)
// The returned page's header should contain the sum of a and b. 
// For example, if we did a PUT request: http://localhost:4131/compute?a=10.5&b=4 then the response should be an HTML page with a heading containing "14.5". Whereas a PUT request http://localhost:4131/compute would return an html page with a header containing "2.4".

const express = require('express');
const app = express();
const port = 3456;

app.use(express.urlencoded({ extended: true }));

app.put('/compute', (req, res) => {
    const a = parseFloat(req.query.a) || 1.2;
    const b = parseFloat(req.query.b) || 1.2;
    const sum = a + b;

    res.setHeader('Content-Type', 'text/html');
    res.status(200);

    res.send(`
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
        </head>
        
        <body>
            <h1>${sum}</h1>
        </body>
    </html>`);
});

app.use((req, res, next) => {
    res.status(404).send("Impossible");
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});