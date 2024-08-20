// const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');

// const app = express();
// const port = 5001;

// // Middleware to parse JSON bodies
// app.use(bodyParser.json());

// // Define the predict endpoint
// app.post('/predict', (req, res) => {
//     const { url } = req.body;
//     if (!url) {
//         return res.status(400).json({ error: 'No URL provided' });
//     }

//     // Spawn a new child process to run the Python script
//     const pythonProcess = spawn('python3', ['predict.py']);

//     // Send JSON data to the Python script via stdin
//     pythonProcess.stdin.write(JSON.stringify({ url }));
//     pythonProcess.stdin.end();

//     // Collect data from the Python script's stdout
//     let result = '';
//     pythonProcess.stdout.on('data', (data) => {
//         result += data.toString();
//     });

//     pythonProcess.stdout.on('end', () => {
//         console.log(`Python script output: ${result}`); // Log output for debugging
//         try {
//             // Parse and send back the result
//             const prediction = JSON.parse(result);
//             res.json(prediction);
//         } catch (error) {
//             console.error(`Parsing error: ${error.message}`); // Log parsing errors
//             res.status(500).json({ error: 'Error parsing prediction output' });
//         }
//     });

//     pythonProcess.stderr.on('data', (data) => {
//         console.error(`stderr: ${data}`);
//     });
// });

// app.listen(port, () => {
//     console.log(`Server is running on port ${port}`);
// });

const express = require('express');
const cors = require('cors');

const app = express();
const port = 5001;

app.use(cors());
app.use(bodyParser.json())

app.post('/predict', (req, res) => {
    const { url } = req.body;
    if (!url) {
        return res.status(400).json({ error: 'No URL provided' });
    }

    // Spawn a new child process to run the Python script
    const pythonProcess = spawn('python3', ['server.py', url]);

    // Send JSON data to the Python script via stdin
    pythonProcess.stdin.write(JSON.stringify({ url }));
    pythonProcess.stdin.end();

    // Collect data from the Python script's stdout
    let result = '';
    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
    });

    pythonProcess.stdout.on('end', () => {
        console.log(`Python script output: ${result}`); // Log output for debugging
        try {
            // Parse and send back the result
            const prediction = JSON.parse(result);
            res.json(prediction);
        } catch (error) {
            console.error(`Parsing error: ${error.message}`); // Log parsing errors
            res.status(500).json({ error: 'Error parsing prediction output' });
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://0.0.0.0:${port}`);
});
