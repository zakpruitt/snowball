const { app, BrowserWindow, Menu, globalShortcut } = require('electron');
const { PythonShell } = require('python-shell');
var kill = require('tree-kill');


PythonShell.run(__dirname + '/src/main.py', null, function (err, results) {
    if (err) throw err;
    console.log('results: %j', results);
});

function createWindow() {
    // create window
    const mainWindow = new BrowserWindow({
        width: 1500,
        height: 1000,
    });
    mainWindow.loadURL('http://127.0.0.1:5000');
    mainWindow.removeMenu();
    mainWindow.webContents.openDevTools();
    //mainWindow.setResizable(false);

    globalShortcut.register('f5', function () {
        console.log('Refreshing Electron page...');
        mainWindow.reload();
    })
}

app.whenReady().then(() => {
    createWindow();
});

app.on('window-all-closed', () => {
    console.log("done");
    app.quit();
});