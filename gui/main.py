import customtkinter as ctk
from app import CaliNoteApp

def main():
    print("Initializing CaliNote...")
    
    # Set appearance mode and color theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue") # We will override most colors
    
    root = ctk.CTk()
    print("Setting up CaliNoteApp...")
    app = CaliNoteApp(root)
    print("Entering mainloop...")
    root.mainloop()

if __name__ == "__main__":
    main()
