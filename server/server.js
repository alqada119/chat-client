const WebSocket = require('ws');
const dgram = require('dgram');
const express = require('express');
const http = require('http');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const UDP_SERVER_IP = "127.0.0.1";
const UDP_PORT = 8081;
const TCP_PORT = 8082;
const HTTP_PORT = 5000;

// UDP Client for status updates
const udpClient = dgram.createSocket('udp4');

// Create an Express server
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Middleware for file uploads
const upload = multer({ dest: 'uploads/' });

// Store connected clients
let clients = [];

// WebSocket Handling
wss.on('connection', (ws) => {
    console.log("New WebSocket connection");

    clients.push(ws);

    ws.on('message', (message) => {
        console.log(`Received: ${message}`);

        // Broadcast message to all clients
        clients.forEach(client => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });

    ws.on('close', () => {
        console.log("WebSocket connection closed");
        clients = clients.filter(client => client !== ws);
    });
});

// API for status updates (sent over UDP)
app.use(express.json());

app.post('/status', (req, res) => {
    const { status } = req.body;
    const message = `STATUS:${status}`;
    udpClient.send(message, UDP_PORT, UDP_SERVER_IP, (err) => {
        if (err) {
            console.error("Error sending UDP status:", err);
            res.status(500).send("Failed to send status");
        } else {
            console.log(`Sent UDP status: ${message}`);
            res.send("Status sent");
        }
    });
});

// API for file upload
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).send("No file uploaded.");
    }

    console.log(`Received file: ${req.file.filename}`);
    res.send({ message: "File uploaded successfully", filename: req.file.filename });
});

// Start the server
server.listen(HTTP_PORT, () => {
    console.log(`Server running on http://localhost:${HTTP_PORT}`);
});
