import customtkinter as ctk
from theme import *

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_DEEP)
        self.app = app
        
        # Sidebar (shared style)
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=SIDEBAR_W, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        ctk.CTkLabel(
            self.sidebar, text="CaliNote", font=FONT_TITLE,
            text_color=ACCENT
        ).pack(pady=40)

        self.nav_btn = ctk.CTkButton(
            self.sidebar, text="  All Notes", font=FONT_BUTTON,
            fg_color="transparent", text_color=FG_DIM,
            hover_color=BG_HOVER, anchor="w", height=45, corner_radius=8,
            command=lambda: self.app.show_notes_list(self.app.password)
        )
        self.nav_btn.pack(fill="x", padx=15, pady=5)

        self.settings_btn = ctk.CTkButton(
            self.sidebar, text="  Settings", font=FONT_BUTTON,
            fg_color=BG_HOVER, text_color=FG_BRIGHT,
            anchor="w", height=45, corner_radius=8
        )
        self.settings_btn.pack(fill="x", padx=15, pady=5)
        
        # Main area
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(side="right", expand=True, fill="both", padx=PAD, pady=PAD)
        
        ctk.CTkLabel(container, text="Settings", font=FONT_TITLE, text_color=FG_BRIGHT).pack(anchor="nw", pady=(0, 30))
        
        # Settings Groups
        self.create_setting_item(container, "Appearance", "Switch between Light and Dark mode", self.toggle_appearance)
        self.create_setting_item(container, "Accent Color", "Change the primary accent color", None)
        self.create_setting_item(container, "Auto-Save", "Automatically save notes every 30 seconds", None, is_toggle=True)
        self.create_setting_item(container, "Encryption", "Change your master vault password", None)

    def create_setting_item(self, parent, title, desc, command, is_toggle=False):
        item = ctk.CTkFrame(parent, fg_color=BG_CARD, height=80, corner_radius=12)
        item.pack(fill="x", pady=10)
        item.pack_propagate(False)
        
        text_frame = ctk.CTkFrame(item, fg_color="transparent")
        text_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(text_frame, text=title, font=FONT_BODY, text_color=FG_BRIGHT).pack(anchor="nw")
        ctk.CTkLabel(text_frame, text=desc, font=FONT_SMALL, text_color=FG_DIM).pack(anchor="nw")
        
        if is_toggle:
            toggle = ctk.CTkSwitch(item, text="", progress_color=ACCENT2)
            toggle.pack(side="right", padx=20)
        else:
            btn = ctk.CTkButton(
                item, text="Configure", font=FONT_SMALL,
                fg_color=BG_HOVER, text_color=FG_BRIGHT,
                width=100, height=32, corner_radius=8,
                command=command
            )
            btn.pack(side="right", padx=20)

    def toggle_appearance(self):
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
