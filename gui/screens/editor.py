import customtkinter as ctk
from tkinter import messagebox
from theme import *
from bridge import save_note, load_note
import os

class EditorScreen(ctk.CTkFrame):
    def __init__(self, parent, app, note_info=None):
        super().__init__(parent, fg_color=BG_DEEP)
        self.app = app
        self.note_info = note_info
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PAD, pady=PAD)
        
        self.back_btn = ctk.CTkButton(
            header, text="←  Back", font=FONT_BUTTON,
            fg_color=BG_CARD, text_color=FG_BRIGHT,
            hover_color=BG_HOVER, width=100, height=40,
            command=lambda: self.app.show_notes_list(self.app.password)
        )
        self.back_btn.pack(side="left")
        
        self.save_btn = ctk.CTkButton(
            header, text="Save Changes", font=FONT_BUTTON,
            fg_color=ACCENT2, text_color=BG_DEEP,
            hover_color="#2da94d", width=140, height=40,
            command=self.on_save
        )
        self.save_btn.pack(side="right")
        
        # Editor Container
        container = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=RADIUS)
        container.pack(expand=True, fill="both", padx=PAD, pady=(0, PAD))

        # Title
        self.title_entry = ctk.CTkEntry(
            container, font=FONT_TITLE, fg_color="transparent",
            text_color=ACCENT, border_width=0,
            placeholder_text="Enter Title...",
            height=60
        )
        self.title_entry.pack(fill="x", padx=20, pady=(20, 10))
        self.title_entry.insert(0, "Untitled Note")
        
        # Separator line
        sep = ctk.CTkFrame(container, fg_color=BORDER, height=1)
        sep.pack(fill="x", padx=20)

        # Body - Standard TK Text inside CTK is often better for performance/features
        # but CTKTextbox exists now.
        self.text_area = ctk.CTkTextbox(
            container, font=FONT_NOTE, fg_color="transparent",
            text_color=FG_BRIGHT,
            padx=20, pady=20, corner_radius=0
        )
        self.text_area.pack(expand=True, fill="both")
        
        if self.note_info:
            self.load_note_data()

    def load_note_data(self):
        res = load_note(self.note_info["path"], self.app.password)
        if res.get("ok"):
            self.title_entry.delete(0, ctk.END)
            self.title_entry.insert(0, res["title"])
            self.text_area.insert("1.0", res["body"])
        else:
            messagebox.showerror("Decryption Failed", "Wrong password or corrupted file. Access denied.")
            # Use after to ensure we don't switch screens while this one is still initializing
            self.after(100, lambda: self.app.show_notes_list(self.app.password))

    def on_save(self):
        title = self.title_entry.get().strip()
        body = self.text_area.get("1.0", ctk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Title cannot be empty.")
            return
            
        filename = title.lower().replace(" ", "_") + ".cali"
        path = os.path.join(self.app.notes_dir, filename)
        
        res = save_note(path, title, body, self.app.password)
        if res.get("ok"):
            # Simple success "animation" - flash button color?
            self.save_btn.configure(text="Saved!", fg_color="#1a7a33")
            self.after(2000, lambda: self.save_btn.configure(text="Save Changes", fg_color=ACCENT2))
        else:
            messagebox.showerror("Error", res.get("error"))
