# CaliNote 🖋️

**CaliNote** is a high-performance, locally-encrypted notes application designed with a macOS-inspired aesthetic. It combines the speed and security of a **Rust** backend with the flexibility of a **Python (Tkinter)** GUI, ensuring your thoughts remain private, secure, and accessible only to you.

---

> [!WARNING]
> **Project Status: Under Active Development**
> CaliNote is currently a functional prototype. Please be aware that:
> - The **UI is currently a bit cluttered** as we refine the layout and typography.
> - Core features are being stabilized.
> - Always remember your master password; there is no recovery mechanism for your encrypted notes.

---

## 🚀 Key Features

- **Zero-Knowledge Privacy:** No cloud, no tracking, no telemetry. Your notes never leave your machine.
- **Military-Grade Encryption:** Every note is individually encrypted using **AES-256-GCM**.
- **Hardened Key Derivation:** Uses **Argon2id** (the winner of the Password Hashing Competition) to derive encryption keys from your master password.
- **Native Experience:** A custom-themed dark interface inspired by macOS, featuring a grid-based organization system.
- **Binary Portability:** Notes are stored in a custom `.cali` format, including magic bytes, salts, and nonces for robust identification and decryption.

## 🛠️ Technical Architecture

CaliNote uses a decoupled architecture for maximum security and performance:

- **Backend (Rust):**
  - Handles all cryptographic operations.
  - Manages secure file I/O.
  - Provides a JSON-based CLI interface for the frontend.
- **Frontend (Python):**
  - Responsive GUI built with `Tkinter`.
  - Implements a subprocess bridge to communicate with the Rust core.
  - Dynamic grid layout for note visualization.
- **Storage Layer:**
  - File Format: `[MAGIC (4B)][SALT (16B)][NONCE (12B)][CIPHERTEXT+TAG]`
  - Plaintext Payload: `[TITLE][NULL_BYTE][BODY]`

## ⚙️ Installation & Usage

### Prerequisites
- **Rust & Cargo** (latest stable)
- **Python 3.10+**
- **Tkinter** (included in most Python distributions)

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/maxdaryan/Calinote.git
   cd Calinote
   ```
2. **Build and Run:**
   The included `Makefile` handles the Rust compilation and Python execution:
   ```bash
   make run
   ```
3. **Usage:**
   - On first launch, set a master password.
   - Use the **+ New Note** button to create encrypted entries.
   - Click any card to edit or the **×** to delete.

## 🏗️ Implementation Roadmap

Our current "Implementation Plan" focuses on transitioning from a functional prototype to a polished productivity tool:

- [ ] **UI De-cluttering:** Streamlining the grid layout and sidebar for a cleaner, more focused experience.
- [ ] **Rich Text Support:** Implementing Markdown or RTF support for formatted notes.
- [ ] **Search & Filter:** Real-time search across note titles and content (decrypted in-memory).
- [ ] **Note Categories:** Folder support and tagging system for better organization.
- [ ] **Auto-Save:** Improving the bridge to handle background saves without UI interruption.
- [ ] **Cross-Platform Packaging:** Native installers for macOS (.app), Windows (.exe), and Linux.

## 🧹 Maintenance
To remove build artifacts and local test notes:
```bash
make clean
```

---
*CaliNote: Your thoughts, secured.*
