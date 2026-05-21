import customtkinter as ctk
from theme import *

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_DEEP)
        self.app = app
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.6, anchor="center") # Start slightly lower
        
        ctk.CTkLabel(
            self.container, text="CALINOTE",
            font=FONT_TITLE, text_color=ACCENT
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            self.container, text="Your thoughts, secured.",
            font=FONT_BODY, text_color=FG_DIM
        ).pack(pady=(0, 40))
        
        self.pass_entry = ctk.CTkEntry(
            self.container, show="*", font=FONT_BODY,
            fg_color=BG_CARD, border_color=BORDER,
            text_color=FG_BRIGHT, placeholder_text="Enter Password",
            width=320, height=50, corner_radius=RADIUS
        )
        self.pass_entry.pack(pady=10)
        self.pass_entry.bind("<Return>", lambda e: self.on_unlock())
        self.pass_entry.focus_set()
        
        self.unlock_btn = ctk.CTkButton(
            self.container, text="Unlock Vault", font=FONT_BUTTON,
            fg_color=ACCENT, text_color=BG_DEEP,
            hover_color="#e5c100", corner_radius=RADIUS,
            height=50, width=320,
            command=self.on_unlock
        )
        self.unlock_btn.pack(pady=20)
        
        self.error_label = ctk.CTkLabel(
            self.container, text="", font=FONT_SMALL,
            text_color=DANGER
        )
        self.error_label.pack()

        # Start animation
        self.animate_in()

    def animate_in(self, target_rely=0.5, current_rely=0.6):
        if current_rely > target_rely:
            current_rely -= 0.005
            self.container.place(relx=0.5, rely=current_rely, anchor="center")
            self.after(10, lambda: self.animate_in(target_rely, current_rely))

    def on_unlock(self):
        password = self.pass_entry.get()
        if not password:
            self.error_label.configure(text="Please enter a password.")
            return
        
        self.app.show_notes_list(password)
