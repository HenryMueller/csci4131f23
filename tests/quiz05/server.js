const express = require('express')
const app = express()
const port = 1234



app.get("/", (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
</head>

<body>
    <p>Hi!</p>
</body>
</html>
    `);
})

app. listen (port , () => {
    console.log(`Example app listening on port ${port}`)
  })