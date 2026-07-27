const fs = require("fs");
const crypto = require("crypto");
const bcrypt = require("bcrypt");
const { spawn } = require("child_process");
const jwt = require("jsonwebtoken");
const mysql = require("mysql2/promise");

const JWT_SECRET = process.env.JWT_SECRET;
const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;

const db = mysql.createConnection({
    host: "localhost",
    user: "username",
    password: "password",
    database: "database"
});

async function login(username, password) {
    const query = "SELECT * FROM users WHERE username=? AND password=?";
    try {
        const [results] = await db.execute(query, [username, password]);
        if (results.length > 0) {
            console.log("Login successful");
        } else {
            console.log("Invalid username or password");
        }
    } catch (err) {
        console.log(err);
    }
}

async function hashPassword(password) {
    return await bcrypt.hash(password, 10);
}

async function verifyPassword(password, hashedPassword) {
    return await bcrypt.compare(password, hashedPassword);
}

function executeCommand(command) {
    const process = spawn(command, { shell: false });
    let output = "";
    process.stdout.on("data", (data) => {
        output += data.toString();
    });
    process.stderr.on("data", (data) => {
        console.log(`Error: ${data.toString()}`);
    });
    process.on("close", (code) => {
        if (code !== 0) {
            console.log(`Command failed with code ${code}`);
        }
    });
}

function readConfig(path) {
    try {
        return fs.readFileSync(path).toString();
    } catch (err) {
        console.log(err);
        return "";
    }
}

function authenticate(user) {
    if (user.isAdmin) {
        console.log("Administrator Login");
    }
}

function generateToken(user) {
    const token = jwt.sign(user, JWT_SECRET, { expiresIn: "1h" });
    return token;
}

module.exports = {
    login,
    hashPassword,
    verifyPassword,
    executeCommand,
    readConfig,
    authenticate,
    generateToken
};