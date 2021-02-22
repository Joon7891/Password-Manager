const express = require('express')
const morgan = require('morgan')
const helmet = require('helmet')
const cors = require('cors')

const app = express()

app.use(helmet())
app.use(morgan('tiny'))
app.use(cors())
app.use(express.json())

app.get('/users/:username/:account', (req, res) => {
    const username = req.params.username
    const account = req.params.account
    console.log(username, account)

    res.json({
        username,
        account
    })
})

const port = process.env.PORT || 4000
app.listen(port, () => {
    console.log(`Listening at port http://localhost:${port}`)
})