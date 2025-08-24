import tkinter as tk
from tkinter import messagebox
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("700x420")
        self.root.configure(bg="#B5E5CF")
        self.root.resizable(False, False)

        # Database setup
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")
        
        # Task list (in memory)
        self.tasks = []

        # Build UI
        self.build_ui()

        # Load saved tasks
        self.load_tasks()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        frame = tk.Frame(self.root, bg="#8EE5EE")
        frame.pack(expand=True, fill="both")

        tk.Label(
            frame, text="TO-DO LIST\nEnter Task:", 
            font=("Arial", 14, "bold"), bg="#8EE5EE", fg="#FF6103"
        ).place(x=20, y=30)

        self.task_entry = tk.Entry(frame, font=("Arial", 14), width=42, bg="white")
        self.task_entry.place(x=180, y=30)
        self.task_entry.bind("<Return>", lambda e: self.add_task())  # press Enter to add

        # Buttons
        tk.Button(frame, text="Add", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"),
                  command=self.add_task).place(x=18, y=80)
        tk.Button(frame, text="Remove", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"),
                  command=self.delete_task).place(x=240, y=80)
        tk.Button(frame, text="Delete All", width=15, bg="#D4AC0D", font=("Arial", 14, "bold"),
                  command=self.delete_all).place(x=460, y=80)
        tk.Button(frame, text="Exit / Close", width=52, bg="#D4AC0D", font=("Arial", 14, "bold"),
                  command=self.close).place(x=17, y=330)

        # Listbox + Scrollbar
        self.task_listbox = tk.Listbox(
            frame, width=70, height=9, font="bold",
            selectmode="SINGLE", bg="white", fg="black",
            selectbackground="#FF8C00", selectforeground="black"
        )
        self.task_listbox.place(x=17, y=140)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.place(x=650, y=140, height=180)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

    # --- Functions ---
    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showinfo("Error", "Field is Empty.")
        elif task in self.tasks:
            messagebox.showinfo("Error", "Task already exists!")
        else:
            self.tasks.append(task)
            self.task_entry.delete(0, "end")
            self.update_list()
            with self.conn:
                self.conn.execute("INSERT INTO tasks VALUES (?)", (task,))

    def delete_task(self):
        try:
            selected = self.task_listbox.get(self.task_listbox.curselection())
            self.tasks.remove(selected)
            self.update_list()
            with self.conn:
                self.conn.execute("DELETE FROM tasks WHERE title=?", (selected,))
        except:
            messagebox.showinfo("Error", "No Task Selected. Cannot Delete.")

    def delete_all(self):
        if messagebox.askyesno("Delete All", "Are you sure?"):
            self.tasks.clear()
            self.update_list()
            with self.conn:
                self.conn.execute("DELETE FROM tasks")

    def update_list(self):
        self.task_listbox.delete(0, "end")
        for t in self.tasks:
            self.task_listbox.insert("end", t)

    def load_tasks(self):
        self.tasks.clear()
        for row in self.cursor.execute("SELECT title FROM tasks"):
            self.tasks.append(row[0])
        self.update_list()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.root.destroy()


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
