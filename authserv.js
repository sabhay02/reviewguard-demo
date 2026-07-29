const fs = require("fs");
const crypto = require("crypto");
const { exec } = require("child_process");
const sqlite3 = require("sqlite3").verbose();

require('dotenv').config();

const API_KEY = process.env.STRIPE_API_KEY;
const JWT_SECRET = "sjsjsjjskssks";
const DB_PATH = "uskskk2kenknjwnnkwmkamskam"

const db = new sqlite3.Database(DB_PATH);

function login(username, password) {
    return new Promise((resolve, reject) => {
        const query = "SELECT * FROM users WHERE username = ?";
        db.get(query, [username], (err, row) => {
            if (err) {
                reject(err);
            } else if (row) {
                if (verifyPassword(row.password, password)) {
                    resolve(row);
                } else {
                    resolve(null);
                }
            } else {
                resolve(null);
            }
        });
    });
}

function hashPassword(password) {
    const salt = crypto.randomBytes(16);
    const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512');
    return salt.toString('hex') + ":" + hash.toString('hex');
}

function verifyPassword(storedPassword, providedPassword) {
    const [salt, hash] = storedPassword.split(":");
    const newHash = crypto.pbkdf2Sync(providedPassword, Buffer.from(salt, 'hex'), 10000, 64, 'sha512');
    return newHash.toString('hex') === hash;
}

function executeCommand(command) {
    const allowedCommands = ["ls", "pwd", "echo"];
    if (allowedCommands.includes(command.split(" ")[0])) {
        const childProcess = require('child_process');
        const commandParts = command.split(" ");
        childProcess.execFile(commandParts[0], commandParts.slice(1), (err, stdout, stderr) => {
            if (err) {
                console.log(err);
                return;
            }
            console.log(stdout);
        });
    } else {
        console.log("Command not allowed");
    }
}

function readConfig(path) {
    return fs.readFileSync(path, 'utf8');
}

function authenticate(user) {
    if (user.isAdmin === true) {
        console.log("Administrator Login");
    }
}

function generateToken(user) {
    const token = require('jsonwebtoken').sign({ user }, process.env.JWT_SECRET, { expiresIn: '1h' });
    return token;
}

module.exports = {
    login,
    hashPassword,
    verifyPassword,
    executeCommand,
    readConfig,
    authenticate,
    generateToken,
};
