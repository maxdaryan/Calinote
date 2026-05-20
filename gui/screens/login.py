import tkinter as tk
from theme import *

class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DEEP)
        self.app = app
        
        container = tk.Frame(self, bg=BG_DEEP)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            container, text="CALINOTE",
            font=FONT_TITLE, fg=ACCENT, bg=BG_DEEP
        ).pack(pady=(0, 40))
        
        self.pass_entry = tk.Entry(
            container, show="*", font=FONT_BODY,
            bg=BG_CARD, fg=FG_BRIGHT, insertbackground=FG_BRIGHT,
            relief="flat", width=30
        )
        self.pass_entry.pack(ipady=10, pady=10)
        self.pass_entry.bind("<Return>", lambda e: self.on_unlock())
        self.pass_entry.focus_set()
        
        unlock_btn = tk.Button(
            container, text="UNLOCK", font=FONT_BUTTON,
            bg=ACCENT, fg=FG_BRIGHT, activebackground=ACCENT,
            activeforeground=FG_BRIGHT, relief="flat",
            command=self.on_unlock, cursor="hand2",
            padx=20, pady=10
        )
        unlock_btn.pack(pady=20)
        
        self.error_label = tk.Label(
            container, text="", font=FONT_SMALL,
            fg=DANGER, bg=BG_DEEP
        )
        self.error_label.pack()

    def on_unlock(self):
        password = self.pass_entry.get()
        if not password:
            self.error_label.config(text="Please enter a password.")
            return
        
        self.app.show_notes_list(password)
