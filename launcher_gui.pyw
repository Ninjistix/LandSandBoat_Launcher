import os
import json
import subprocess
import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ----------------------- Paths -----------------------
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))      # server\tools
SERVER_ROOT = os.path.dirname(TOOLS_DIR)                    # server root

CONFIG_PATH = os.path.join(TOOLS_DIR, "launcher_config.json")
LOG_PATH = os.path.join(TOOLS_DIR, "launcher_gui_log.txt")
ERROR_LOG_PATH = os.path.join(TOOLS_DIR, "launcher_gui_error.txt")

# ----------------------- Server EXEs -----------------------
SERVER_EXES = {
    "Connect": os.path.join(SERVER_ROOT, "xi_connect.exe"),
    "Map":     os.path.join(SERVER_ROOT, "xi_map.exe"),
    "Search":  os.path.join(SERVER_ROOT, "xi_search.exe"),
    "World":   os.path.join(SERVER_ROOT, "xi_world.exe"),
}

# ----------------------- App state -----------------------
process_handles = {}
auto_restart_vars = {}
manual_stopped = {}
gui_rows = {}
auto_restart_flags_loaded = {}
root = None

# ----------------------- Logging -----------------------
def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_log(msg):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{_now()}] {msg}\n")
    except Exception as e:
        write_error(f"Logging failed: {e}")

def write_error(msg):
    try:
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{_now()}] {msg}\n")
    except Exception:
        try:
            messagebox.showerror("Launcher Error (logging failed)", str(msg))
        except Exception:
            pass

# ----------------------- Config -----------------------
def load_config():
    cfg = {}
    try:
        if os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                write_log("Loaded config from launcher_config.json")
    except Exception as e:
        write_error(f"Failed to load config: {e}")
    return cfg

def save_config():
    try:
        cfg = {"auto_restart": {}}
        for name, var in auto_restart_vars.items():
            cfg["auto_restart"][name] = bool(var.get())
        if root:
            cfg["window_geometry"] = root.geometry()
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        write_log("Saved config to launcher_config.json")
    except Exception as e:
        write_error(f"Failed to save config: {e}")

# ----------------------- Process helpers -----------------------
def is_running_by_name(exe_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def start_process(name, path):
    exe = os.path.basename(path)
    if not os.path.isfile(path):
        messagebox.showerror("Executable not found", f"{path} does not exist.")
        write_error(f"Start failed: {path} not found")
        return
    if is_running_by_name(exe):
        write_log(f"{name} already running (detected by process name).")
        return
    try:
        # Start in server root for DLLs/resources
        p = subprocess.Popen(
            ["cmd", "/c", "start", "", path],
            cwd=SERVER_ROOT,
            shell=True
        )
        process_handles[name] = p
        manual_stopped[name] = False
        write_log(f"Started {name} ({exe}) with PID {p.pid}")
    except Exception as e:
        write_error(f"Failed to start {name}: {e}")
        messagebox.showerror("Start Error", f"{name}: {e}")

def stop_process(name, path):
    exe = os.path.basename(path)
    manual_stopped[name] = True
    stopped_any = False
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == exe.lower():
                write_log(f"Stopping {name} (PID {proc.pid})")
                try:
                    proc.terminate()
                    proc.wait(timeout=4)
                    write_log(f"Terminated {name} PID {proc.pid}")
                except Exception:
                    try:
                        proc.kill()
                        write_log(f"Killed {name} PID {proc.pid}")
                    except Exception as ee:
                        write_error(f"Failed to kill {name} PID {proc.pid}: {ee}")
                stopped_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not stopped_any:
        write_log(f"Stop requested for {name} but no running process found.")

def restart_process(name, path):
    manual_stopped[name] = False
    stop_process(name, path)
    start_process(name, path)
    write_log(f"Restart requested for {name}")

# ----------------------- UI update & auto-restart -----------------------
def update_status_loop():
    for name, widgets in gui_rows.items():
        path = SERVER_EXES[name]
        exe = os.path.basename(path)
        running = is_running_by_name(exe)
        widgets["status"].config(text="Running" if running else "Stopped",
                                 foreground="green" if running else "red")
        if auto_restart_vars[name].get() and not running and not manual_stopped.get(name, False):
            write_log(f"Auto-Restart triggered for {name}")
            start_process(name, path)
    root.after(1000, update_status_loop)

# ----------------------- GUI -----------------------
def build_gui():
    global root, gui_rows
    root = tk.Tk()
    root.title("LandSandBoat Server Launcher")

    cfg = load_config()
    geometry = cfg.get("window_geometry", "760x320+100+100")
    root.geometry(geometry)

    frm = ttk.Frame(root, padding=12)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Server", width=20).grid(row=0, column=0, sticky="w")
    ttk.Label(frm, text="Status", width=20).grid(row=0, column=1, sticky="w")
    ttk.Label(frm, text="Auto-Restart", width=12).grid(row=0, column=2, sticky="w")

    gui_rows = {}
    row = 1
    for name, exe_path in SERVER_EXES.items():
        ttk.Label(frm, text=name).grid(row=row, column=0, sticky="w")
        lbl_status = ttk.Label(frm, text="Checking...", foreground="orange")
        lbl_status.grid(row=row, column=1, sticky="w")

        val = auto_restart_flags_loaded.get(name, False)
        var = tk.BooleanVar(value=val)
        auto_restart_vars[name] = var
        ttk.Checkbutton(frm, variable=var, command=save_config).grid(row=row, column=2)

        ttk.Button(frm, text="Start",
                   command=lambda n=name, p=exe_path: start_process(n, p)).grid(row=row, column=3, padx=6)
        ttk.Button(frm, text="Stop",
                   command=lambda n=name, p=exe_path: stop_process(n, p)).grid(row=row, column=4, padx=6)
        ttk.Button(frm, text="Restart",
                   command=lambda n=name, p=exe_path: restart_process(n, p)).grid(row=row, column=5, padx=6)

        gui_rows[name] = {"status": lbl_status}
        manual_stopped[name] = False
        row += 1

    btn_frame = ttk.Frame(root, padding=(12, 6))
    btn_frame.pack(fill="x")

    ttk.Button(btn_frame, text="Start ALL",
               command=lambda: [start_process(n, p) for n, p in SERVER_EXES.items()]).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Stop ALL",
               command=lambda: [stop_process(n, p) for n, p in SERVER_EXES.items()]).pack(side="left", padx=6)

    info_txt = f"Config: {CONFIG_PATH}    Log: {LOG_PATH}    Error Log: {ERROR_LOG_PATH}"
    ttk.Label(root, text=info_txt, font=("Segoe UI", 8)).pack(side="bottom", pady=6)

    # Save window geometry when resized/moved
    def on_configure(event):
        save_config()
    root.bind("<Configure>", on_configure)

    root.after(500, update_status_loop)
    return root

# ----------------------- Safe startup -----------------------
def safe_start():
    try:
        try:
            _ = psutil.cpu_count()
        except Exception as e:
            messagebox.showerror("Missing dependency",
                                 "psutil not installed. Run:\n\npip install psutil")
            write_error(f"psutil import failed: {e}")
            return

        global auto_restart_flags_loaded
        cfg = load_config()
        auto_restart_flags_loaded = cfg.get("auto_restart", {})

        app = build_gui()
        save_config()
        app.mainloop()
    except Exception as e:
        write_error(f"Unexpected launcher error: {e}")
        messagebox.showerror("Launcher Error", str(e))

if __name__ == "__main__":
    safe_start()
