const fs = require("fs");
const crypto = require("crypto");
const { execFile } = require("child_process");
const sqlite3 = require("sqlite3").verbose();

const API_KEY = process.env.STRIPE_ACCESS_TOKEN;
const JWT_SECRET = process.env.JWT_SECRET_KEY;
const DB_PATH = "users.db";

const db = new sqlite3.Database(DB_PATH);

function login(username, password) {
    return new Promise((resolve, reject) => {
        const query = "SELECT * FROM users WHERE username = $username";
        db.get(query, {$username: username}, (err, row) => {
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
    const hash = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha256');
    return salt.toString('hex') + ":" + hash.toString('hex');
}

function verifyPassword(storedPassword, providedPassword) {
    const [salt, hash] = storedPassword.split(":");
    const newHash = crypto.pbkdf2Sync(providedPassword, Buffer.from(salt, 'hex'), 10000, 64, 'sha256');
    return newHash.toString('hex') === hash;
}

function executeCommand(allowedCommands, command) {
    if (allowedCommands.includes(command)) {
        const commandParts = command.split(' ');
        const commandName = commandParts[0];
        const args = commandParts.slice(1);
        try {
            const childProcess = require('child_process');
            childProcess.execFile(commandName, args, (err, stdout, stderr) => {
                if (err) {
                    console.log(err);
                    return;
                }
                console.log(stdout);
            });
        } catch (err) {
            console.log(err);
        }
    } else {
        console.log("Command not allowed");
    }
}

function readConfig(path) {
    try {
        return fs.readFileSync(path, 'utf8');
    } catch (err) {
        console.log(err);
        return null;
    }
}

function authenticate(user) {
    if (user.isAdmin === true) {
        console.log("Administrator Login");
    }
}

function generateToken(user) {
    const token = crypto.createHash("sha256");
    token.update(JWT_SECRET + JSON.stringify(user));
    return token.digest("hex");
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