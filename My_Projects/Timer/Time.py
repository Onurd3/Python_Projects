from __future__ import annotations

import sys
import time
import ctypes
import datetime as dt
import tkinter as tk
from typing import Optional


WINDOW_TITLE = "⏰ Alarm"
WINDOW_SIZE = "900x200"
ALARM_MESSAGE = (
    "ALARM! Time reached 🔔"
)


def bring_to_front(root: tk.Tk) -> None:
    """Best-effort: keep the window on top and try to grab focus (Windows-focused)."""
    try:
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()

        # Windows-specific: attempt to restore console and set foreground to Tk window
        try:
            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            console_hwnd = kernel32.GetConsoleWindow()
            if console_hwnd:
                # 9 == SW_RESTORE
                user32.ShowWindow(console_hwnd, 9)
            user32.SetForegroundWindow(root.winfo_id())
        except Exception:
            # Non-Windows or restricted environments will land here.
            pass
    except Exception:
        pass


def alarm_popup(message: str = ALARM_MESSAGE) -> None:
    """Create and run the alarm popup window."""
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)

    bring_to_front(root)

    label = tk.Label(root, text=message, font=("Arial", 18), fg="red")
    label.pack(expand=True)

    close_btn = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 14))
    close_btn.pack(pady=20)

    root.mainloop()


def parse_alarm_time(text: str) -> Optional[dt.time]:
    """Parse HH:MM 24-hour time into a time object; return None if invalid."""
    try:
        return dt.datetime.strptime(text.strip(), "%H:%M").time()
    except ValueError:
        return None


def wait_until(alarm_time: dt.time) -> None:
    """Block until the system time matches the given alarm time (minute precision)."""
    print(f"Alarm set for: {alarm_time.strftime('%H:%M')}")
    while True:
        now = dt.datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            return
        time.sleep(1)


def main() -> int:
    try:
        prompt = "Alarm time (HH:MM): "
        text = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nCanceled.")
        return 1

    alarm_time = parse_alarm_time(text)
    if alarm_time is None:
        print("Invalid time format. Example: 14:30")
        return 2

    wait_until(alarm_time)
    alarm_popup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
