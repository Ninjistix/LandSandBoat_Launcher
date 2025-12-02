# LandSandBoat Server Launcher

A simple **Python Tkinter GUI** to manage the LandSandBoat private server executables.

This launcher provides easy control over starting, stopping, restarting, and monitoring the server processes, with improvements for better organization and usability.

---

## Features

- **Auto-detect server executables** located in the server root folder:
  - `xi_connect.exe`
  - `xi_map.exe`
  - `xi_search.exe`
  - `xi_world.exe`
- **Start / Stop / Restart** each executable individually
- **Start ALL / Stop ALL** with a single click
- **Auto-Restart option** for each executable if it crashes (configurable)
- **Process status monitoring** (Running / Stopped)
- **Persistent GUI window size/position** saved across sessions
- **Logs** all actions and errors to:
  - `tools/launcher_gui_log.txt`  
  - `tools/launcher_gui_error.txt`
- **Configuration** stored in `tools/launcher_config.json`

---

## Folder Structure & Setup

1. **Place the launcher files inside the `tools` folder** within your server directory:

```
your_server_directory/
│
├── xi_connect.exe
├── xi_map.exe
├── xi_search.exe
├── xi_world.exe
│
└── tools/
    ├── launcher_gui.pyw
    └── requirements.txt  (add `psutil` at the bottom if not present)

```

2. **Install dependencies**

- **Option A:** If you prefer not to modify `requirements.txt`:
  
  - Manually install `psutil` by running:

  ```
  pip install psutil
  ```

- **Option B:** Or, install all dependencies listed in `requirements.txt` with:

  ```
  pip install -r tools/requirements.txt
  ```

*Note:* If `psutil` is not already in `requirements.txt`, ensure you add it there for easier setup in future.

3. **Run the launcher**

- Launch the GUI with:

```
pythonw tools/launcher_gui.pyw
```

---

## How It Works & Changes

### Path Handling
- The script dynamically determines its location (`TOOLS_DIR`) and the server root directory (`SERVER_ROOT`).
- Executable paths are constructed relative to the server root, allowing flexible placement of the launcher inside the `tools` folder.

### Window Geometry Persistence
- The GUI window size and position are saved automatically in `launcher_config.json` upon resize or move, and restored on startup.

### Process Launching
- Server processes are started using `cmd /c start` within the server root directory, ensuring proper DLL/resource loading.

### Logging & Error Handling
- All logs include timestamps.
- Errors during logging or process management are captured and logged for easier debugging.

### User Interface
- The GUI layout is similar but now supports the new folder structure.
- Status indicators, auto-restart toggles, and control buttons are maintained.

---

## Dependencies

- Python 3.8+
- Install dependencies with:

```bash
pip install -r tools/requirements.txt
```

*(or install `psutil` manually with `pip install psutil`)*

---

## Screenshots

*(Screenshot of the GUI window)*

> *A screenshot showing the main launcher window with server statuses, control buttons, and auto-restart toggles.*

*<img width="721" height="352" alt="image" src="https://github.com/user-attachments/assets/8b343b89-3c9a-46bb-b12b-20e244cddfa9" />*

---

## License

This project is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for details.
