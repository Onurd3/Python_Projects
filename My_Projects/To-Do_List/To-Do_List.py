import tkinter as tk
from tkinter import messagebox

# ---- Data ----
tasks = []  # in-memory task list

# ---- Logic ----
def refresh():
    """Sync the visible listbox with the in-memory list."""
    listbox.delete(0, tk.END)
    for t in tasks:
        listbox.insert(tk.END, t)

def add_task():
    text = entry.get().strip()
    if not text:
        messagebox.showwarning("Warning", "Type a task first.")
        return
    tasks.append(text)
    entry.delete(0, tk.END)
    refresh()

def delete_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a task to delete.")
        return
    idx = sel[0]
    tasks.pop(idx)
    refresh()

def complete_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a task to complete.")
        return
    idx = sel[0]
    # mark as completed if not already
    if not tasks[idx].startswith("[x] "):
        tasks[idx] = "[x] " + tasks[idx]
        refresh()

def save_tasks():
    try:
        with open("tasks.txt", "w", encoding="utf-8") as f:
            for t in tasks:
                f.write(t + "\n")
        messagebox.showinfo("Saved", "Tasks saved to tasks.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")

def load_tasks():
    try:
        with open("tasks.txt", "r", encoding="utf-8") as f:
            for line in f:
                tasks.append(line.strip())
        refresh()
    except FileNotFoundError:
        pass  # first run: file doesn't exist yet

# ---- UI (simple/minimal) ----
root = tk.Tk()
root.title("To-Do List")
root.geometry("360x460")

top = tk.Frame(root)
top.pack(pady=8)

entry = tk.Entry(top, width=28)
entry.grid(row=0, column=0, padx=4)
tk.Button(top, text="Add", width=8, command=add_task).grid(row=0, column=1)

listbox = tk.Listbox(root, width=44, height=18)
listbox.pack(pady=8)

buttons = tk.Frame(root)
buttons.pack(pady=4)

tk.Button(buttons, text="Delete",   width=10, command=delete_task).grid(row=0, column=0, padx=3)
tk.Button(buttons, text="Complete", width=10, command=complete_task).grid(row=0, column=1, padx=3)
tk.Button(buttons, text="Save",     width=10, command=save_tasks).grid(row=0, column=2, padx=3)

load_tasks()
root.mainloop()
