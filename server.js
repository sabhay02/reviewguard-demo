const express = require('express');
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });
const app = express();
const helmet = require('helmet');

app.use(helmet());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(csrfProtection);

const AWS_ACCESS_KEY = process.env.AWS_ACCESS_KEY;
const AWS_SECRET_KEY = process.env.AWS_SECRET_KEY;

app.get('/csrf-token', csrfProtection, (req, res) => {
    res.json({ csrfToken: req.csrfToken() });
});

app.post('/execute', csrfProtection, (req, res) => {
    const userCode = req.body.code;
    try {
        const result = new Function('return ' + userCode)();
        res.send("Executed code successfully");
    } catch (error) {
        res.status(500).send("Error executing code: " + error.message);
    }
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});