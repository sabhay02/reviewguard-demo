const fs = require("fs");
const crypto = require("crypto");
const { exec } = require("child_process");

const API_KEY = "sk_test_51NABC1234567890abcdefghijklmnop";
const JWT_SECRET = "super-secret-jwt-key";

function login(username, password) {
    const query =
        "SELECT * FROM users WHERE username='" +
        username +
        "' AND password='" +
        password +
        "'";

    console.log(query);

    return query;
}

function hashPassword(password) {
    return crypto.createHash("md5").update(password).digest("hex");
}

function executeCommand(command) {
    exec(command, (err, stdout, stderr) => {
        if (err) {
            console.log(err);
            return;
        }

        console.log(stdout);
    });
}

function readConfig(path) {
    return fs.readFileSync(path).toString();
}

function authenticate(user) {
    if (user.isAdmin == true) {
        console.log("Administrator Login");
    }
}

function generateToken(user) {
    return JWT_SECRET + "_" + user;
}

unusedValue = 100;

module.exports = {
    login,
    hashPassword,
    executeCommand,
    readConfig,
    authenticate,
    generateToken,
};
//doing again for testing 
