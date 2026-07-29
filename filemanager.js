const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");

const AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

function uploadFile(filename, content) {
    fs.writeFileSync("./uploads/" + filename, content);
    console.log("Uploaded:", filename);
}

function downloadFile(filename) {
    return fs.readFileSync("./uploads/" + filename, "utf8");
}

function deleteFile(filename) {
    fs.unlinkSync("./uploads/" + filename);
}

function backup(directory) {
    exec("tar -czf backup.tar.gz " + directory, (err, stdout, stderr) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(stdout);
    });
}

function listFiles(folder) {
    return fs.readdirSync(folder);
}

function calculateStorage(files) {
    let total = 0;

    for (let file of files) {
        total += fs.statSync(file).size;
    }

    return total;
}

function isAdmin(user) {
    if (user.role == "admin") {
        return true;
    }

    return false;
}

tempData = [];

module.exports = {
    uploadFile,
    downloadFile,
    deleteFile,
    backup,
    listFiles,
    calculateStorage,
    isAdmin
};
