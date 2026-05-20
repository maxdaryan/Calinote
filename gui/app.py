import tkinter as tk
from theme import *
from screens.login import LoginScreen
from screens.notes_list import NotesListScreen
from screens.editor import EditorScreen

class CaliNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CaliNote")
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.configure(bg=BG_DEEP)
        
        # Application State
        self.password = None
        self.current_screen = None
        self.notes_dir = "notes"
        
        self.show_login()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_login(self):
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self)
        self.current_screen.pack(expand=True, fill="both")

    def show_notes_list(self, password):
        self.password = password
        self.clear_screen()
        self.current_screen = NotesListScreen(self.root, self)
        self.current_screen.pack(expand=True, fill="both")

    def open_note(self, note_info):
        self.clear_screen()
        self.current_screen = EditorScreen(self.root, self, note_info)
        self.current_screen.pack(expand=True, fill="both")

    def create_new_note(self):
        self.clear_screen()
        self.current_screen = EditorScreen(self.root, self, None)
        self.current_screen.pack(expand=True, fill="both")
