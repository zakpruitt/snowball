const { app, BrowserWindow } = require('electron');


function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
    });
    mainWindow.loadFile("src/templates/index.html");
}

app.whenReady().then(() => {
    createWindow();
});