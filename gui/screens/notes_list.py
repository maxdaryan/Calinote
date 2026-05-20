import tkinter as tk
from tkinter import messagebox
from theme import *
from bridge import list_notes, delete_note
import os

class NotesListScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DEEP)
        self.app = app
        
        # Sidebar
        sidebar = tk.Frame(self, bg=BG_SIDEBAR, width=SIDEBAR_W)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar, text="CaliNote", font=FONT_TITLE,
            fg=ACCENT, bg=BG_SIDEBAR, pady=20
        ).pack()

        # Folders/Lists section
        folder_item = tk.Frame(sidebar, bg=BG_HOVER, padx=20, pady=8)
        folder_item.pack(fill="x", pady=(20, 0))
        tk.Label(folder_item, text="All CaliNotes", font=FONT_BODY, fg=FG_BRIGHT, bg=BG_HOVER).pack(side="left")

        # Bottom sidebar action
        new_btn = tk.Button(
            sidebar, text="+ New Note", font=FONT_BUTTON,
            bg=BG_SIDEBAR, fg=ACCENT, relief="flat",
            activebackground=BG_HOVER, activeforeground=ACCENT,
            command=self.app.create_new_note, cursor="hand2",
            bd=0, highlightthickness=0
        )
        new_btn.pack(side="bottom", fill="x", pady=20)
        
        # Main area with header
        main_container = tk.Frame(self, bg=BG_DEEP)
        main_container.pack(side="right", expand=True, fill="both")
        
        header = tk.Frame(main_container, bg=BG_DEEP, height=60)
        header.pack(fill="x", padx=PAD, pady=PAD)
        header.pack_propagate(False)
        
        tk.Label(header, text="All CaliNotes", font=FONT_TITLE, fg=FG_BRIGHT, bg=BG_DEEP).pack(side="left")
        
        # Search bar placeholder style
        search_frame = tk.Frame(header, bg=BG_CARD, padx=10, pady=5)
        search_frame.pack(side="right")
        tk.Label(search_frame, text="🔍 Search", font=FONT_SMALL, fg=FG_DIM, bg=BG_CARD).pack()

        # Grid area for notes
        self.canvas = tk.Canvas(main_container, bg=BG_DEEP, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_DEEP)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Ensure the scrollable frame is at least as wide as the canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.pack(side="left", expand=True, fill="both", padx=PAD)
        self.scrollbar.pack(side="right", fill="y")
        
        self.refresh()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def refresh(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        res = list_notes(self.app.notes_dir)
        print(f"DEBUG: list_notes result: {res}")
        if not res.get("ok"):

            tk.Label(self.scrollable_frame, text=f"Error: {res.get('error')}", fg=DANGER, bg=BG_DEEP).pack()
            return
            
        notes = res.get("notes", [])
        if not notes:
            tk.Label(
                self.scrollable_frame, text="No notes yet. Click + New Note to start.",
                font=FONT_BODY, fg=FG_DIM, bg=BG_DEEP
            ).pack(pady=100)
            return
            
        # Display as a grid of cards
        cols = 3
        for i, note in enumerate(notes):
            row = i // cols
            col = i % cols
            self.render_note_card(note, row, col)

    def render_note_card(self, note, row, col):
        card = tk.Frame(self.scrollable_frame, bg=BG_CARD, padx=15, pady=15, width=220, height=180)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False)
        
        # Make the card clickable
        card.bind("<Button-1>", lambda e, n=note: self.app.open_note(n))
        
        title_lbl = tk.Label(
            card, text=note["filename"], font=FONT_BODY,
            fg=FG_BRIGHT, bg=BG_CARD, wraplength=180, justify="left"
        )
        title_lbl.pack(anchor="nw")
        title_lbl.bind("<Button-1>", lambda e, n=note: self.app.open_note(n))

        # Date/Subtitle style
        tk.Label(
            card, text="CaliNote File", font=FONT_SMALL,
            fg=FG_DIM, bg=BG_CARD
        ).pack(anchor="nw", pady=(5, 0))

        # Delete button hidden in card
        del_btn = tk.Button(
            card, text="×", font=("Arial", 14),
            bg=BG_CARD, fg=FG_DIM, relief="flat",
            activebackground=DANGER, activeforeground=FG_BRIGHT,
            command=lambda n=note: self.on_delete(n),
            cursor="hand2", bd=0
        )
        del_btn.place(relx=1.0, rely=0.0, anchor="ne", x=5, y=-5)

    def on_delete(self, note):
        if messagebox.askyesno("Delete", f"Delete {note['filename']} permanently?"):
            res = delete_note(note["path"])
            if res.get("ok"):
                self.refresh()
            else:
                messagebox.showerror("Error", res.get("error"))
