import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import os
import threading
import time

class PersonalManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Management App")
        self.root.geometry("800x600")
        
        # Data storage
        self.data_file = "personal_data.json"
        self.tasks = []
        self.expenses = []
        self.load_data()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tasks_tab()
        self.create_expenses_tab()
        self.create_reminders_tab()
        
        # Start reminder checker
        self.start_reminder_checker()
        
        # Save data on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_tasks_tab(self):
        # Tasks tab
        self.tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_frame, text="Tasks")
        
        # Task input section
        input_frame = ttk.LabelFrame(self.tasks_frame, text="Add New Task", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, sticky='w', padx=5)
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, sticky='w', padx=5)
        self.priority_combo = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], width=10)
        self.priority_combo.grid(row=0, column=3, padx=5)
        self.priority_combo.set("Medium")
        
        ttk.Label(input_frame, text="Due Date:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.due_date_entry = ttk.Entry(input_frame, width=15)
        self.due_date_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(row=1, column=3, padx=5, pady=5)
        
        # Tasks list
        list_frame = ttk.LabelFrame(self.tasks_frame, text="Tasks", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for tasks
        columns = ("Task", "Priority", "Due Date", "Status", "Created")
        self.tasks_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tasks_tree.heading(col, text=col)
            self.tasks_tree.column(col, width=150)
        
        # Scrollbar for tasks
        tasks_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=tasks_scrollbar.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        tasks_scrollbar.pack(side='right', fill='y')
        
        # Task control buttons
        task_buttons_frame = ttk.Frame(self.tasks_frame)
        task_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(task_buttons_frame, text="Mark Complete", command=self.mark_complete).pack(side='left', padx=5)
        ttk.Button(task_buttons_frame, text="Delete Task", command=self.delete_task).pack(side='left', padx=5)
        ttk.Button(task_buttons_frame, text="Edit Task", command=self.edit_task).pack(side='left', padx=5)
        
        self.refresh_tasks_list()
    
    def create_expenses_tab(self):
        # Expenses tab
        self.expenses_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.expenses_frame, text="Expenses")
        
        # Expense input section
        expense_input_frame = ttk.LabelFrame(self.expenses_frame, text="Add New Expense", padding=10)
        expense_input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(expense_input_frame, text="Description:").grid(row=0, column=0, sticky='w', padx=5)
        self.expense_desc_entry = ttk.Entry(expense_input_frame, width=30)
        self.expense_desc_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(expense_input_frame, text="Amount:").grid(row=0, column=2, sticky='w', padx=5)
        self.expense_amount_entry = ttk.Entry(expense_input_frame, width=15)
        self.expense_amount_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(expense_input_frame, text="Category:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.expense_category_combo = ttk.Combobox(expense_input_frame, 
                                                  values=["Food", "Transportation", "Entertainment", "Bills", "Shopping", "Health", "Other"],
                                                  width=20)
        self.expense_category_combo.grid(row=1, column=1, padx=5, pady=5)
        self.expense_category_combo.set("Other")
        
        ttk.Button(expense_input_frame, text="Add Expense", command=self.add_expense).grid(row=1, column=3, padx=5, pady=5)
        
        # Expenses list
        expense_list_frame = ttk.LabelFrame(self.expenses_frame, text="Expenses", padding=10)
        expense_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for expenses
        expense_columns = ("Description", "Amount", "Category", "Date")
        self.expenses_tree = ttk.Treeview(expense_list_frame, columns=expense_columns, show="headings", height=10)
        
        for col in expense_columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=150)
        
        # Scrollbar for expenses
        expenses_scrollbar = ttk.Scrollbar(expense_list_frame, orient='vertical', command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=expenses_scrollbar.set)
        
        self.expenses_tree.pack(side='left', fill='both', expand=True)
        expenses_scrollbar.pack(side='right', fill='y')
        
        # Expense control buttons and summary
        expense_control_frame = ttk.Frame(self.expenses_frame)
        expense_control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(expense_control_frame, text="Delete Expense", command=self.delete_expense).pack(side='left', padx=5)
        ttk.Button(expense_control_frame, text="Show Summary", command=self.show_expense_summary).pack(side='left', padx=5)
        
        self.refresh_expenses_list()
    
    def create_reminders_tab(self):
        # Reminders tab
        self.reminders_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reminders_frame, text="Reminders")
        
        # Reminder settings
        settings_frame = ttk.LabelFrame(self.reminders_frame, text="Reminder Settings", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=5)
        
        self.reminder_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Reminders", variable=self.reminder_enabled).pack(anchor='w')
        
        ttk.Label(settings_frame, text="Check for due tasks every:").pack(anchor='w', pady=(10,0))
        self.reminder_interval = tk.IntVar(value=30)
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(anchor='w', pady=5)
        ttk.Entry(interval_frame, textvariable=self.reminder_interval, width=10).pack(side='left')
        ttk.Label(interval_frame, text="minutes").pack(side='left', padx=(5,0))
        
        # Upcoming tasks display
        upcoming_frame = ttk.LabelFrame(self.reminders_frame, text="Upcoming Tasks (Next 7 Days)", padding=10)
        upcoming_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Upcoming tasks list
        upcoming_columns = ("Task", "Priority", "Due Date", "Days Left")
        self.upcoming_tree = ttk.Treeview(upcoming_frame, columns=upcoming_columns, show="headings", height=10)
        
        for col in upcoming_columns:
            self.upcoming_tree.heading(col, text=col)
            self.upcoming_tree.column(col, width=150)
        
        upcoming_scrollbar = ttk.Scrollbar(upcoming_frame, orient='vertical', command=self.upcoming_tree.yview)
        self.upcoming_tree.configure(yscrollcommand=upcoming_scrollbar.set)
        
        self.upcoming_tree.pack(side='left', fill='both', expand=True)
        upcoming_scrollbar.pack(side='right', fill='y')
        
        ttk.Button(self.reminders_frame, text="Refresh Upcoming Tasks", 
                  command=self.refresh_upcoming_tasks).pack(pady=10)
        
        self.refresh_upcoming_tasks()
    
    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_combo.get()
        due_date = self.due_date_entry.get().strip()
        
        if not task:
            messagebox.showwarning("Warning", "Please enter a task description")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter date in YYYY-MM-DD format")
            return
        
        new_task = {
            "id": len(self.tasks) + 1,
            "task": task,
            "priority": priority,
            "due_date": due_date,
            "status": "Pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(new_task)
        self.save_data()
        self.refresh_tasks_list()
        self.refresh_upcoming_tasks()
        
        # Clear entries
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        messagebox.showinfo("Success", "Task added successfully!")
    
    def add_expense(self):
        description = self.expense_desc_entry.get().strip()
        amount_str = self.expense_amount_entry.get().strip()
        category = self.expense_category_combo.get()
        
        if not description or not amount_str:
            messagebox.showwarning("Warning", "Please enter description and amount")
            return
        
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid amount")
            return
        
        new_expense = {
            "id": len(self.expenses) + 1,
            "description": description,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.expenses.append(new_expense)
        self.save_data()
        self.refresh_expenses_list()
        
        # Clear entries
        self.expense_desc_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Expense of ${amount:.2f} added successfully!")
    
    def mark_complete(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = self.tasks_tree.item(selected[0])
        task_text = item['values'][0]
        
        for task in self.tasks:
            if task['task'] == task_text and task['status'] == 'Pending':
                task['status'] = 'Completed'
                break
        
        self.save_data()
        self.refresh_tasks_list()
        self.refresh_upcoming_tasks()
        messagebox.showinfo("Success", "Task marked as completed!")
    
    def delete_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            item = self.tasks_tree.item(selected[0])
            task_text = item['values'][0]
            
            self.tasks = [task for task in self.tasks if task['task'] != task_text]
            self.save_data()
            self.refresh_tasks_list()
            self.refresh_upcoming_tasks()
            messagebox.showinfo("Success", "Task deleted successfully!")
    
    def edit_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = self.tasks_tree.item(selected[0])
        task_text = item['values'][0]
        
        for task in self.tasks:
            if task['task'] == task_text:
                new_task = simpledialog.askstring("Edit Task", "Edit task description:", initialvalue=task['task'])
                if new_task:
                    task['task'] = new_task
                    self.save_data()
                    self.refresh_tasks_list()
                    self.refresh_upcoming_tasks()
                    messagebox.showinfo("Success", "Task updated successfully!")
                break
    
    def delete_expense(self):
        selected = self.expenses_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            item = self.expenses_tree.item(selected[0])
            expense_desc = item['values'][0]
            
            self.expenses = [expense for expense in self.expenses if expense['description'] != expense_desc]
            self.save_data()
            self.refresh_expenses_list()
            messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def show_expense_summary(self):
        if not self.expenses:
            messagebox.showinfo("Summary", "No expenses recorded yet.")
            return
        
        total = sum(expense['amount'] for expense in self.expenses)
        
        # Category breakdown
        categories = {}
        for expense in self.expenses:
            cat = expense['category']
            categories[cat] = categories.get(cat, 0) + expense['amount']
        
        summary = f"Total Expenses: ${total:.2f}\n\nBreakdown by Category:\n"
        for cat, amount in sorted(categories.items()):
            summary += f"• {cat}: ${amount:.2f}\n"
        
        messagebox.showinfo("Expense Summary", summary)
    
    def refresh_tasks_list(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        for task in self.tasks:
            self.tasks_tree.insert("", "end", values=(
                task['task'], task['priority'], task['due_date'], 
                task['status'], task['created']
            ))
    
    def refresh_expenses_list(self):
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        for expense in self.expenses:
            self.expenses_tree.insert("", "end", values=(
                expense['description'], f"${expense['amount']:.2f}", 
                expense['category'], expense['date']
            ))
    
    def refresh_upcoming_tasks(self):
        for item in self.upcoming_tree.get_children():
            self.upcoming_tree.delete(item)
        
        today = datetime.now()
        week_later = today + timedelta(days=7)
        
        upcoming_tasks = []
        for task in self.tasks:
            if task['status'] == 'Pending':
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
                    if today <= due_date <= week_later:
                        days_left = (due_date - today).days
                        upcoming_tasks.append((task, days_left))
                except ValueError:
                    continue
        
        # Sort by days left
        upcoming_tasks.sort(key=lambda x: x[1])
        
        for task, days_left in upcoming_tasks:
            days_text = f"{days_left} days" if days_left != 1 else "1 day"
            if days_left == 0:
                days_text = "Today!"
            elif days_left < 0:
                days_text = "Overdue!"
            
            self.upcoming_tree.insert("", "end", values=(
                task['task'], task['priority'], task['due_date'], days_text
            ))
    
    def start_reminder_checker(self):
        def check_reminders():
            while True:
                if self.reminder_enabled.get():
                    self.check_due_tasks()
                time.sleep(self.reminder_interval.get() * 60)  # Convert minutes to seconds
        
        reminder_thread = threading.Thread(target=check_reminders, daemon=True)
        reminder_thread.start()
    
    def check_due_tasks(self):
        today = datetime.now().date()
        due_today = []
        overdue = []
        
        for task in self.tasks:
            if task['status'] == 'Pending':
                try:
                    due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                    if due_date == today:
                        due_today.append(task['task'])
                    elif due_date < today:
                        overdue.append(task['task'])
                except ValueError:
                    continue
        
        if due_today or overdue:
            message = ""
            if due_today:
                message += f"Tasks due TODAY:\n• " + "\n• ".join(due_today) + "\n\n"
            if overdue:
                message += f"OVERDUE tasks:\n• " + "\n• ".join(overdue)
            
            # Show reminder in a separate thread to avoid blocking
            self.root.after(0, lambda: messagebox.showinfo("Task Reminder", message))
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.expenses = data.get('expenses', [])
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                self.expenses = []
    
    def save_data(self):
        data = {
            'tasks': self.tasks,
            'expenses': self.expenses
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def on_closing(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalManagerApp(root)
    root.mainloop()