import sqlite3
import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("650x400")
        self.root.configure(bg="#B5E5CF")
        self.root.resizable(False, False)

        # Database
        self.conn = sqlite3.connect("tasks.db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS tasks (title TEXT)")
        
        # Task list
        self.tasks = []

        # ---- UI ----
        frame = tk.Frame(root, bg="#8EE5EE")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="TO-DO LIST\nEnter Task:", font=("Arial", 14, "bold"),
                 bg="#8EE5EE", fg="#FF6103").place(x=20, y=30)

        self.task_entry = tk.Entry(frame, font=("Arial", 14), width=42)
        self.task_entry.place(x=180, y=30)

        self.add_btn = tk.Button(frame, text="Add", width=15, bg="#D4AC0D",
                                 font=("Arial", 14, "bold"), command=self.add_task)
        self.add_btn.place(x=18, y=80)

        self.del_btn = tk.Button(frame, text="Remove", width=15, bg="#D4AC0D",
                                 font=("Arial", 14, "bold"), command=self.delete_task)
        self.del_btn.place(x=240, y=80)

        self.del_all_btn = tk.Button(frame, text="Delete All", width=15, bg="#D4AC0D",
                                     font=("Arial", 14, "bold"), command=self.delete_all)
        self.del_all_btn.place(x=460, y=80)

        self.exit_btn = tk.Button(frame, text="Exit / Close", width=52, bg="#D4AC0D",
                                  font=("Arial", 14, "bold"), command=self.close)
        self.exit_btn.place(x=17, y=330)

        # Listbox with scrollbar
        self.task_listbox = tk.Listbox(frame, width=70, height=9, font="bold",
                                       selectmode="SINGLE", bg="white", fg="black",
                                       selectbackground="#FF8C00")
        self.task_listbox.place(x=17, y=140)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.place(x=615, y=140, height=210)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Bind Enter key to Add
        self.root.bind("<Return>", lambda e: self.add_task())

        # Load saved tasks
        self.load_tasks()

        # Safe window close
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # ---------------- Functions ----------------
    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showinfo("Error", "Field is Empty.")
            return
        if task in self.tasks:
            messagebox.showinfo("Error", "Task already exists.")
            return
        self.tasks.append(task)
        self.conn.execute("INSERT INTO tasks VALUES (?)", (task,))
        self.conn.commit()
        self.update_list()
        self.task_entry.delete(0, "end")

    def delete_task(self):
        try:
            task = self.task_listbox.get(self.task_listbox.curselection())
            self.tasks.remove(task)
            self.conn.execute("DELETE FROM tasks WHERE title=?", (task,))
            self.conn.commit()
            self.update_list()
        except:
            messagebox.showinfo("Error", "No Task Selected.")

    def delete_all(self):
        if messagebox.askyesno("Delete All", "Are you sure?"):
            self.tasks.clear()
            self.conn.execute("DELETE FROM tasks")
            self.conn.commit()
            self.update_list()

    def update_list(self):
        self.task_listbox.delete(0, "end")
        for t in self.tasks:
            self.task_listbox.insert("end", t)

    def load_tasks(self):
        self.tasks.clear()
        for row in self.conn.execute("SELECT title FROM tasks"):
            self.tasks.append(row[0])
        self.update_list()

    def close(self):
        self.conn.close()
        self.root.destroy()

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
