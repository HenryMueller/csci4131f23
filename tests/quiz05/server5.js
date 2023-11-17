const express = require('express')
const app = express()
const port = 2345

app.use((req, res, next) => {
    next();
    console.log("ALPHA");
})

app.get('/logtest', (req , res) => {
  console.log('BETA')
})

app. listen (port , () => {
  console.log(`Example app listening on port ${port}`)
})