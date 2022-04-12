const { app, BrowserWindow, Menu, globalShortcut } = require('electron');
const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs');

PythonShell.run(__dirname + '/src/main.py', null, function (err, results) {
    if (err) throw err;
    console.log('results: %j', results);
});

function createWindow() {
    // create window
    const mainWindow = new BrowserWindow({
        width: 1600,
        height: 1000,
    });
    mainWindow.loadURL('http://127.0.0.1:5000');
    mainWindow.removeMenu();
    mainWindow.setResizable(false);
    mainWindow.webContents.openDevTools();

    globalShortcut.register('f5', function () {
        console.log('Refreshing Electron page...');
        mainWindow.reload();
    })
}

async function emptyTemp() {
    console.log("Emptying temp folder...");
    const folderPath = "./data/temp/";
    await fs.promises.readdir(folderPath)
    .then((f) => Promise.all(f.map(e => fs.promises.unlink(`${folderPath}${e}`))))
}

app.whenReady().then(() => {
    createWindow();
    emptyTemp();
});

app.on('window-all-closed', () => {
    app.quit();
    console.log("App closed.");
});