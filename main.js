const { app, BrowserWindow, Menu } = require('electron');
require('electron-reload')(__dirname);


function createWindow() {
    // create window
    const mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
    });
    mainWindow.loadFile("src/templates/index.html");
    mainWindow.removeMenu();
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