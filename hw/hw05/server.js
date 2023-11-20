const express = require('express')
const app = express()
const port = 4131

app.set("views", "template")
app.set("view engine", "pug")

app.use(express.urlencoded({ extended: true }))
app.use(express.json())



app.use((req, res, next) => {
    res.status(404).send("Sorry, can't find that!")
})

app.listen(port, () => {
    console.log(`App listening on port ${port}`)
})