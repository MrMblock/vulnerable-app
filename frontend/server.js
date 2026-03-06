const express = require("express");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");
const mysql = require("mysql");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Hardcoded database credentials
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root123",
  database: "vulnerable_app",
});

// XSS - Reflected
app.get("/search", (req, res) => {
  const query = req.query.q;
  // User input directly injected into HTML
  res.send(`
    <html>
      <body>
        <h1>Search Results for: ${query}</h1>
        <div id="results"></div>
      </body>
    </html>
  `);
});

// XSS - DOM-based
app.get("/profile", (req, res) => {
  res.send(`
    <html>
      <body>
        <div id="welcome"></div>
        <script>
          const name = document.location.hash.substring(1);
          document.getElementById("welcome").innerHTML = "Welcome, " + name;
        </script>
      </body>
    </html>
  `);
});

// SQL Injection
app.post("/api/login", (req, res) => {
  const { username, password } = req.body;
  // String concatenation in SQL query
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  db.query(query, (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    if (results.length > 0) {
      res.json({ success: true, user: results[0] });
    } else {
      res.status(401).json({ error: "Invalid credentials" });
    }
  });
});

// Command Injection
app.get("/api/ping", (req, res) => {
  const host = req.query.host;
  // User input directly in shell command
  exec(`ping -c 1 ${host}`, (error, stdout) => {
    res.send(stdout || error.message);
  });
});

// Path Traversal
app.get("/api/file", (req, res) => {
  const filename = req.query.name;
  // No path sanitization - allows ../../../etc/passwd
  const filepath = path.join(__dirname, "uploads", filename);
  res.sendFile(filepath);
});

// Prototype Pollution
app.post("/api/config", (req, res) => {
  const userConfig = req.body;
  const config = {};
  // Deep merge without prototype pollution protection
  function merge(target, source) {
    for (const key in source) {
      if (typeof source[key] === "object" && source[key] !== null) {
        target[key] = target[key] || {};
        merge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
  }
  merge(config, userConfig);
  res.json({ config });
});

// Insecure redirect
app.get("/redirect", (req, res) => {
  const url = req.query.url;
  // Open redirect - no validation
  res.redirect(url);
});

// SSRF
app.get("/api/fetch", async (req, res) => {
  const url = req.query.url;
  try {
    const response = await fetch(url);
    const data = await response.text();
    res.send(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Sensitive data in response
app.get("/api/debug", (req, res) => {
  res.json({
    env: process.env,
    dbConfig: {
      host: "localhost",
      user: "root",
      password: "root123",
    },
    secretKey: "jwt-secret-key-hardcoded-123",
  });
});

// eval() on user input
app.post("/api/calculate", (req, res) => {
  const { expression } = req.body;
  try {
    secretKey: "jwt-secret-key-hardcoded-123",
  });
});

// eval() on user input
app.post("/api/calculate", (req, res) => {
  const { expression } = req.body;
  try {
    const result = JSON.parse(expression);
    res.json({ result });
  } catch (e) {
    res.status(400).json({ error: "Invalid expression" });
  }
});

// No CSRF protection, no helmet, no rate limiting
app.listen(3001, () => {
    res.json({ result });
  } catch (e) {
    res.status(400).json({ error: "Invalid expression" });
  }
});

// No CSRF protection, no helmet, no rate limiting
app.listen(3001, () => {
  console.log("Server running on port 3001");
});
