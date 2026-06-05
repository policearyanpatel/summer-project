
import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import json, os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TaskManagerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Pro")
        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1400x800")

        self.tasks = []
        self.load_tasks()
        self.build_ui()
        self.refresh_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json","r",encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except:
                self.tasks=[]

    def save_tasks(self):
        with open("tasks.json","w",encoding="utf-8") as f:
            json.dump(self.tasks,f,indent=4)

    def build_ui(self):
        self.root.configure(fg_color="#F5F5F5")

        ctk.CTkLabel(self.root,text="TASK MANAGER PRO",
                     font=("Segoe UI",32,"bold")).pack(pady=10)

        top=ctk.CTkFrame(self.root,fg_color="#F5F5F5")
        top.pack(fill="both",expand=True,padx=10,pady=10)

        self.left=ctk.CTkFrame(top)
        self.left.pack(side="left",fill="y",padx=10)

        self.total=ctk.CTkLabel(self.left,text="Total Tasks: 0")
        self.total.pack(pady=10)
        self.completed=ctk.CTkLabel(self.left,text="Completed: 0")
        self.completed.pack(pady=10)
        self.pending=ctk.CTkLabel(self.left,text="Pending: 0")
        self.pending.pack(pady=10)
        self.productivity=ctk.CTkLabel(self.left,text="Productivity: 0%")
        self.productivity.pack(pady=10)
        self.achievement=ctk.CTkLabel(self.left,text="Achievement: Beginner",wraplength=200)
        self.achievement.pack(pady=10)

        self.center=ctk.CTkFrame(top)
        self.center.pack(side="left",fill="both",expand=True,padx=10)

        self.search=ctk.CTkEntry(self.center,placeholder_text="Search Task")
        self.search.pack(fill="x",padx=10,pady=10)

        ctk.CTkButton(self.center,text="Search",command=self.search_tasks).pack(pady=5)

        self.box=ctk.CTkTextbox(self.center)
        self.box.pack(fill="both",expand=True,padx=10,pady=10)

        self.right=ctk.CTkFrame(top)
        self.right.pack(side="right",fill="y",padx=10)

        ctk.CTkButton(self.right,text="Add Task",command=self.add_task_window).pack(fill="x",pady=5,padx=10)
        ctk.CTkButton(self.right,text="Update Task",command=self.update_task_window).pack(fill="x",pady=5,padx=10)
        ctk.CTkButton(self.right,text="Delete Task",command=self.delete_task).pack(fill="x",pady=5,padx=10)
        ctk.CTkButton(self.right,text="Show Overdue",command=self.show_overdue).pack(fill="x",pady=5,padx=10)
        ctk.CTkButton(self.right,text="Export Report",command=self.export_report).pack(fill="x",pady=5,padx=10)

    def add_task_window(self):
        w=ctk.CTkToplevel(self.root)
        w.title("Add Task")
        w.geometry("450x600")

        title=ctk.CTkEntry(w,placeholder_text="Task Title")
        title.pack(pady=8)

        category=ctk.CTkOptionMenu(w,values=["Work","Study","Personal","Health","Other"])
        category.pack(pady=8)

        priority=ctk.CTkOptionMenu(w,values=["High","Medium","Low"])
        priority.pack(pady=8)

        status=ctk.CTkOptionMenu(w,values=["Pending","In Progress","Completed"])
        status.pack(pady=8)

        due=ctk.CTkEntry(w,placeholder_text="Due Date DD-MM-YYYY")
        due.pack(pady=8)

        notes=ctk.CTkTextbox(w,height=120)
        notes.pack(pady=8)

        def save():
            task={
                "id":f"T{len(self.tasks)+1:03}",
                "title":title.get(),
                "category":category.get(),
                "priority":priority.get(),
                "status":status.get(),
                "due_date":due.get(),
                "notes":notes.get("1.0","end").strip(),
                "created":datetime.now().strftime("%d-%m-%Y %H:%M")
            }
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_tasks()
            w.destroy()

        ctk.CTkButton(w,text="Save",command=save).pack(pady=10)

    def update_task_window(self):
        tid=ctk.CTkInputDialog(text="Enter Task ID",title="Update").get_input()
        if not tid: return
        for task in self.tasks:
            if task["id"]==tid:
                new=ctk.CTkInputDialog(text="New Title",title="Update").get_input()
                if new:
                    task["title"]=new
                    task["updated"]=datetime.now().strftime("%d-%m-%Y %H:%M")
                    self.save_tasks()
                    self.refresh_tasks()
                return
        messagebox.showerror("Error","Task not found")

    def delete_task(self):
        tid=ctk.CTkInputDialog(text="Enter Task ID",title="Delete").get_input()
        if not tid: return
        self.tasks=[t for t in self.tasks if t["id"]!=tid]
        self.save_tasks()
        self.refresh_tasks()

    def refresh_tasks(self):
        self.box.delete("1.0","end")
        completed=0

        for t in self.tasks:
            if t["status"]=="Completed":
                completed+=1

            self.box.insert("end",
                f"{t['id']} | {t['title']}\n"
                f"Category: {t['category']}\n"
                f"Priority: {t['priority']}\n"
                f"Status: {t['status']}\n"
                f"Due: {t['due_date']}\n"
                f"{'-'*40}\n"
            )

        total=len(self.tasks)
        pending=total-completed
        prod=int((completed/total)*100) if total else 0

        self.total.configure(text=f"Total Tasks: {total}")
        self.completed.configure(text=f"Completed: {completed}")
        self.pending.configure(text=f"Pending: {pending}")
        self.productivity.configure(text=f"Productivity: {prod}%")

        if completed >= 10:
            ach="Task Master"
        elif completed >= 5:
            ach="Productive Performer"
        elif completed >= 1:
            ach="First Task Completed"
        else:
            ach="Beginner"

        self.achievement.configure(text=f"Achievement: {ach}")

    def search_tasks(self):
        q=self.search.get().lower()
        self.box.delete("1.0","end")
        for t in self.tasks:
            if q in t["title"].lower() or q in t["id"].lower():
                self.box.insert("end",f"{t['id']} | {t['title']}\n")

    def show_overdue(self):
        today=datetime.now()
        self.box.delete("1.0","end")
        for t in self.tasks:
            try:
                d=datetime.strptime(t["due_date"],"%d-%m-%Y")
                if d < today and t["status"]!="Completed":
                    self.box.insert("end",f"OVERDUE: {t['id']} {t['title']}\n")
            except:
                pass

    def export_report(self):
        path=filedialog.asksaveasfilename(defaultextension=".txt")
        if not path: return
        with open(path,"w",encoding="utf-8") as f:
            for t in self.tasks:
                f.write(str(t)+"\n")
        messagebox.showinfo("Success","Report Exported")

root=ctk.CTk()
app=TaskManagerPro(root)
root.mainloop()
