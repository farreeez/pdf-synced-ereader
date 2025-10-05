import { app, BrowserWindow } from "electron";
import isDev from "electron-is-dev";
import { join } from "path";

// NOTE: When using ESM, Node does not allow directory imports. Import the explicit file.
import {
  enable as enableRemote,
  initialize,
} from "@electron/remote/main/index.js";
initialize();

function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      enableRemoteModule: true,
    },
  });

  // Enable @electron/remote on this window's webContents
  try {
    enableRemote(win.webContents);
  } catch (e) {
    // Non-fatal; continue even if remote couldn't be enabled.
    console.warn("Failed to enable @electron/remote:", e);
  }

  win.loadURL(
    isDev
      ? "http://localhost:3000"
      : `file://${join(__dirname, "../build/index.html")}`
  );
}

app.on("ready", createWindow);

// Quit when all windows are closed.
app.on("window-all-closed", function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
