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
    mainWindow.setResizable(false);

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
    PythonShell.end(function (err,code,signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
    });
    app.quit();
});