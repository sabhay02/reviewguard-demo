const express = require('express');
const app = express();

// Hardcoded AWS Key (Gitleaks should catch this secret)
const AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

app.get('/execute', (req, res) => {
    // Dangerous eval injection (Semgrep should catch this vulnerability)
    const userCode = req.query.code;
    eval(userCode);
    
    res.send("Executed code successfully");
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});

//testing again 
