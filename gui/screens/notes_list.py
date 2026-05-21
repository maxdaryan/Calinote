import customtkinter as ctk
from tkinter import messagebox
from theme import *
from bridge import list_notes, delete_note
import os

class NotesListScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_DEEP)
        self.app = app
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=SIDEBAR_W, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        ctk.CTkLabel(
            self.sidebar, text="CaliNote", font=FONT_TITLE,
            text_color=ACCENT
        ).pack(pady=40)

        # Nav items
        self.nav_btn = ctk.CTkButton(
            self.sidebar, text="  All Notes", font=FONT_BUTTON,
            fg_color=BG_HOVER, text_color=FG_BRIGHT,
            anchor="w", height=45, corner_radius=8,
            command=self.refresh
        )
        self.nav_btn.pack(fill="x", padx=15, pady=5)

        self.settings_btn = ctk.CTkButton(
            self.sidebar, text="  Settings", font=FONT_BUTTON,
            fg_color="transparent", text_color=FG_DIM,
            hover_color=BG_HOVER, anchor="w", height=45, corner_radius=8,
            command=self.app.show_settings
        )
        self.settings_btn.pack(fill="x", padx=15, pady=5)

        # Bottom sidebar action
        self.new_btn = ctk.CTkButton(
            self.sidebar, text="+  New Note", font=FONT_BUTTON,
            fg_color=ACCENT, text_color=BG_DEEP,
            hover_color="#e5c100", corner_radius=RADIUS,
            height=50, command=self.app.create_new_note
        )
        self.new_btn.pack(side="bottom", fill="x", padx=20, pady=30)
        
        # Main area
        self.main_container = ctk.CTkFrame(self, fg_color=BG_DEEP, corner_radius=0)
        self.main_container.pack(side="right", expand=True, fill="both")
        
        # Header
        header = ctk.CTkFrame(self.main_container, fg_color="transparent", height=80)
        header.pack(fill="x", padx=PAD, pady=(PAD, 0))
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="All CaliNotes", font=FONT_SUBTITLE, text_color=FG_BRIGHT).pack(side="left")
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            header, placeholder_text="Search notes...",
            font=FONT_SMALL, fg_color=BG_CARD, border_color=BORDER,
            width=250, height=35, corner_radius=10
        )
        self.search_entry.pack(side="right", pady=20)

        # Grid area for notes using CTKScrollableFrame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_container, fg_color="transparent",
            label_text=None
        )
        self.scrollable_frame.pack(expand=True, fill="both", padx=PAD, pady=PAD)
        
        # Configure grid columns
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.refresh()

    def refresh(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        res = list_notes(self.app.notes_dir)
        if not res.get("ok"):
            ctk.CTkLabel(self.scrollable_frame, text=f"Error: {res.get('error')}", text_color=DANGER).pack()
            return
            
        notes = res.get("notes", [])
        if not notes:
            ctk.CTkLabel(
                self.scrollable_frame, text="No notes yet. Start by creating one!",
                font=FONT_BODY, text_color=FG_DIM
            ).pack(pady=100)
            return
            
        for i, note in enumerate(notes):
            row = i // 3
            col = i % 3
            self.render_note_card(note, row, col)

    def render_note_card(self, note, row, col):
        card = ctk.CTkFrame(
            self.scrollable_frame, fg_color=BG_CARD,
            corner_radius=RADIUS, height=200
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Clickable area
        title_btn = ctk.CTkButton(
            card, text=note["filename"], font=FONT_BODY,
            fg_color="transparent", text_color=FG_BRIGHT,
            hover_color=BG_HOVER, anchor="nw",
            command=lambda n=note: self.app.open_note(n)
        )
        title_btn.pack(fill="both", expand=True, padx=15, pady=(15, 0))

        # Bottom info in card
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", side="bottom", padx=15, pady=15)
        
        ctk.CTkLabel(
            info_frame, text="CaliNote File", font=FONT_SMALL,
            text_color=FG_DIM
        ).pack(side="left")

        del_btn = ctk.CTkButton(
            info_frame, text="Delete", font=FONT_SMALL,
            fg_color="transparent", text_color=FG_DIM,
            hover_color=DANGER, width=60, height=25,
            command=lambda n=note: self.on_delete(n)
        )
        del_btn.pack(side="right")

    def on_delete(self, note):
        if messagebox.askyesno("Delete", f"Delete {note['filename']} permanently?"):
            res = delete_note(note["path"])
            if res.get("ok"):
                self.refresh()
            else:
                messagebox.showerror("Error", res.get("error"))
