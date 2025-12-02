# LandSandBoat Server Launcher

A simple **Python Tkinter GUI** to manage the LandSandBoat private server executables.  

This launcher provides easy control over starting, stopping, restarting, and monitoring the server processes.

---

## Features

- **Detects server executables automatically** in the same folder:
  - `xi_connect.exe`
  - `xi_map.exe`
  - `xi_search.exe`
  - `xi_world.exe`
- **Start / Stop / Restart** each executable individually
- **Start ALL / Stop ALL** with a single click
- **Auto-Restart option** per executable if it crashes
- **Process status monitoring** (Running / Stopped)
- **Persistent settings** saved in `launcher_config.json`
- **Logs** all actions and errors to:
  - `launcher_gui_log.txt`  
  - `launcher_gui_error.txt`  

---

## Setup & Usage

1. **Place the launcher files in your server folder**  

Make sure both `launcher_gui.py` and `setup.bat` are in the **root folder of your server**, next to the `.exe` files:

```

DIR\server
│ xi_connect.exe
│ xi_map.exe
│ xi_search.exe
│ xi_world.exe
│ launcher_gui.py
│ setup.bat

```

2. **Run the setup batch file**  

Double-click `setup.bat`. This will:

- Install Python dependencies automatically (e.g., `psutil`)  
- Launch the Python GUI (`launcher_gui.pyw`) after setup  

3. **Using the launcher**  

- Start the server by clicking **Start** for individual executables or **Start ALL**  
- Stop the server by clicking **Stop** for individual executables or **Stop ALL**  
- Toggle **Auto-Restart** for any executable to automatically relaunch it if it crashes  
- Monitor each executable's status directly in the GUI

---

## Screenshot


![Launcher Screenshot](https://github.com/user-attachments/assets/3004a369-be19-4adb-817d-c35097f3436a)

*Example of the LandSandBoat Server Launcher interface.* 

---

## Notes

- The launcher does **not auto-start executables** on launch; you must manually start them  
- Settings (Auto-Restart) are saved automatically in `launcher_config.json`  
- Logs are written in the same folder as the launcher for debugging and monitoring

---

## Requirements

- **Python 3.8+**  
- **psutil** (`pip install psutil` or `py -3 -m pip install psutil`)  
- Tkinter (usually included with Python)

---

## License

This project is licensed under the **MIT License**.  
Use, modify, and distribute freely.
```
