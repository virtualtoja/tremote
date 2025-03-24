import tkinter as tk
from tkinter import ttk

import subprocess
import threading
import queue

class TerminalTab(ttk.Frame):
    def __init__(self, parent, name):
        super().__init__(parent)
        
        self.process = subprocess.Popen(
            ["python", "l_serv.py", str(name)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        self.text = tk.Text(self, wrap="word", bg="black", fg="white", insertbackground="white")
        self.text.pack(expand=True, fill="both")
        
        self.entry = tk.Entry(self, bg="black", fg="white", insertbackground="white")
        self.entry.pack(fill="x")
        
        self.entry.bind("<Return>", self.execute_command)
        self.text.insert("end", f"Terminal {name} started\n")
        self.text.config(state="disabled")
        
        self.queue = queue.Queue()
        self.output_thread = threading.Thread(target=self.read_output, daemon=True)
        self.output_thread.start()
        self.after(100, self.process_queue)
    
    def execute_command(self, event):
        command = self.entry.get() + "\n"
        self.entry.delete(0, "end")
        
        if self.process.stdin:
            self.process.stdin.write(command)
            self.process.stdin.flush()

        if command.startswith("quit") or command.startswith("disconnect"):
            self.text.config(state="normal")
            self.text.insert("end", "Terminal session end.")
            self.text.config(state="disabled")
            self.text.see("end")

            return

        self.text.config(state="normal")
        self.text.insert("end", f"> {command}")
        self.text.config(state="disabled")
        self.text.see("end")
    
    def read_output(self):
        while True:
            if self.process.stdout:
                output = self.process.stdout.readline()
                if output:
                    self.queue.put(output)
    
    def process_queue(self):
        while not self.queue.empty():
            output = self.queue.get()
            self.text.config(state="normal")
            self.text.insert("end", output)
            self.text.config(state="disabled")
            self.text.see("end")
        self.after(100, self.process_queue)

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TRemote server multiclient v1.1")
        self.geometry("800x600")
        
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(side="top", fill="x")
        
        self.add_tab_button = ttk.Button(self.toolbar, text="Start new server", command=self.add_tab)
        self.add_tab_button.pack(side="left")
        
        self.remove_tab_button = ttk.Button(self.toolbar, text="Close server", command=self.remove_tab)
        self.remove_tab_button.pack(side="left")
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.base_port = 4445
        self.tab_count = 0
        self.add_tab()
    
    def add_tab(self):
        new_tab = TerminalTab(self.notebook, self.base_port)
        self.notebook.add(new_tab, text=f"Server {self.base_port}")
        self.base_port += 1
    
    def remove_tab(self):
        current_tab = self.notebook.index("current")
        #self.notebook.tabs()[current_tab].execute_command("quit")
        if current_tab >= 0:
            self.notebook.forget(current_tab)
            self.tab_count -= 1
            self.base_port -= 1

if __name__ == "__main__":
    app = TerminalApp()
    app.mainloop()
