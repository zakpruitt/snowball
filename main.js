const { app, BrowserWindow, Menu } = require('electron');
const { PythonShell } = require('python-shell');


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
    //mainWindow.webContents.openDevTools();
    // create menus
    // let menu = Menu.buildFromTemplate(
    // [
    //     {
    //         label: 'File',
    //         submenu: [
    //             {
    //                 label: 'Quit',
    //                 click: () => {
    //                     app.quit();
    //                 }
    //             },
    //             {
    //                 label: 'Open',
    //                 click: () => {
    //                     mainWindow.loadFile("src/templates/index.html");
    //                 }
    //             }
    //         ]
    //     }
    // ]);
    // Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {  
    createWindow();
});

app.on('window-all-closed', () => {
    console.log("done");
    app.quit();
});