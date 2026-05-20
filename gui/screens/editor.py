import tkinter as tk
from tkinter import messagebox
from theme import *
from bridge import save_note, load_note
import os

class EditorScreen(tk.Frame):
    def __init__(self, parent, app, note_info=None):
        super().__init__(parent, bg=BG_DEEP)
        self.app = app
        self.note_info = note_info
        
        # Header
        header = tk.Frame(self, bg=BG_DEEP)
        header.pack(fill="x", padx=PAD, pady=PAD)
        
        back_btn = tk.Button(
            header, text="← Back", font=FONT_BUTTON,
            bg=BG_CARD, fg=FG_BRIGHT, relief="flat",
            command=lambda: self.app.show_notes_list(self.app.password),
            cursor="hand2"
        )
        back_btn.pack(side="left")
        
        save_btn = tk.Button(
            header, text="Save Note", font=FONT_BUTTON,
            bg=ACCENT2, fg=BG_DEEP, relief="flat",
            command=self.on_save, cursor="hand2"
        )
        save_btn.pack(side="right")
        
        # Editor
        self.title_entry = tk.Entry(
            self, font=FONT_TITLE, bg=BG_DEEP, fg=ACCENT,
            insertbackground=FG_BRIGHT, relief="flat"
        )
        self.title_entry.pack(fill="x", padx=PAD, pady=(0, PAD))
        self.title_entry.insert(0, "Untitled Note")
        
        self.text_area = tk.Text(
            self, font=FONT_NOTE, bg=BG_CARD, fg=FG_BRIGHT,
            insertbackground=FG_BRIGHT, relief="flat",
            padx=20, pady=20, wrap="word"
        )
        self.text_area.pack(expand=True, fill="both", padx=PAD, pady=(0, PAD))
        
        if self.note_info:
            self.load_note_data()

    def load_note_data(self):
        res = load_note(self.note_info["path"], self.app.password)
        if res.get("ok"):
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, res["title"])
            self.text_area.insert("1.0", res["body"])
        else:
            messagebox.showerror("Error", res.get("error"))
            self.app.show_notes_list(self.app.password)

    def on_save(self):
        title = self.title_entry.get().strip()
        body = self.text_area.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Title cannot be empty.")
            return
            
        filename = title.lower().replace(" ", "_") + ".cali"
        path = os.path.join(self.app.notes_dir, filename)
        
        res = save_note(path, title, body, self.app.password)
        if res.get("ok"):
            messagebox.showinfo("Success", "Note saved successfully.")
            self.app.show_notes_list(self.app.password)
        else:
            messagebox.showerror("Error", res.get("error"))
