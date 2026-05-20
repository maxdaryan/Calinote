import tkinter as tk
from app import CaliNoteApp

def main():
    print("Initializing Tkinter...")
    root = tk.Tk()
    print("Setting up CaliNoteApp...")
    app = CaliNoteApp(root)
    print("Entering mainloop...")
    root.mainloop()

if __name__ == "__main__":
    main()
