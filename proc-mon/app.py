import ctypes
import time
import psutil


def get_proc_by_name(name: str) -> psutil.Process:
    """Get a vmmem procedure by name"""
    print(f"Searching for process with name '{name}'...")
    # Search process names
    vmmem_proc_list = [proc for proc in psutil.process_iter() if proc.name() == name]
    if len(vmmem_proc_list) == 0:
        print("No process found!")
        return None

    print(f"Process '{name}' found!")
    return vmmem_proc_list[0]


def windows_alert(message: str, title: str) -> None:
    """Generates a Windows OS alert"""
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, message, title, 0)
    return None


PROC_NAME_STR = "vmmem"
CPU_THRESHOLD = 95
SLEEP_SECONDS = 10

# How many CPU cores on the computer?
# To emulate Windows taskmgr.exe behavior you can do: p.cpu_percent() / psutil.cpu_count()
NUM_CORES = psutil.cpu_count()

vmmem = get_proc_by_name(PROC_NAME_STR)
if vmmem:
    while True:
        # percentage since last call, SLEEP_SECONDS ago
        cpu_percent = round(vmmem.cpu_percent() / NUM_CORES)
        if cpu_percent > CPU_THRESHOLD:
            # Alert the user
            message = f"VMMem CPU usage of {cpu_percent}% is greater than {CPU_THRESHOLD}% threshold."
            message += '\n\nRun "wsl --shutdown" and then restart Docker Desktop.'
            title = "VMMem Usage High!"
            windows_alert(message, title)

        time.sleep(SLEEP_SECONDS)

print("All Done")
