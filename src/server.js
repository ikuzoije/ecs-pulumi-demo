'use strict';
const express = require('express');

// Constants
const PORT = process.env.PORT || 8080;
const HOST = '0.0.0.0';

// Environment Variables
const APP_NAME = process.env.APP_NAME || 'Default App';
const APP_VERSION = process.env.APP_VERSION || '1.0.0';

// App
const app = express();
app.get('/', (req, res) => {
  res.send(`App Name: ${APP_NAME}, Version: ${APP_VERSION}`);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);