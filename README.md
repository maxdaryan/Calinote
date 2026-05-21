# CaliNote 🖋️

**CaliNote** is a high-performance, locally-encrypted notes application designed with a modern macOS-inspired aesthetic. It combines the speed and security of a **Rust** backend with a polished **Python (CustomTkinter)** GUI, ensuring your thoughts remain private, secure, and accessible only to you.

---

> [!WARNING]
> **Project Status: Under Active Development**
> CaliNote is currently a functional prototype. Please be aware that:
> - **Settings Screen:** Currently a UI placeholder. These options are not yet functional.
> - Core features are being stabilized.
> - Always remember your master password; there is no recovery mechanism for your encrypted notes.

---

## 🚀 Key Features

- **Zero-Knowledge Privacy:** No cloud, no tracking, no telemetry. Your notes never leave your machine.
- **Military-Grade Encryption:** Every note is individually encrypted using **AES-256-GCM**.
- **Hardened Key Derivation:** Uses **Argon2id** (the winner of the Password Hashing Competition) to derive encryption keys from your master password.
- **Modern Interface:** A premium dark interface built with **CustomTkinter**, featuring smooth animations, rounded corners, and SF Pro typography.
- **Binary Portability:** Notes are stored in a custom `.cali` format, including magic bytes, salts, and nonces for robust identification and decryption.

## 🛠️ Technical Architecture

CaliNote uses a decoupled architecture for maximum security and performance:

- **Backend (Rust):**
  - Handles all cryptographic operations.
  - Manages secure file I/O.
  - Provides a JSON-based CLI interface for the frontend.
- **Frontend (Python):**
  - Modern GUI built with `CustomTkinter`.
  - Implements a subprocess bridge to communicate with the Rust core.
  - Dynamic grid layout for note visualization.
- **Storage Layer:**
  - File Format: `[MAGIC (4B)][SALT (16B)][NONCE (12B)][CIPHERTEXT+TAG]`
  - Plaintext Payload: `[TITLE][NULL_BYTE][BODY]`

## ⚙️ Installation & Usage

### Prerequisites
- **Rust & Cargo** (latest stable)
- **Python 3.10+**
- **CustomTkinter** (`pip install customtkinter`)

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/maxdaryan/Calinote.git
   cd Calinote
   ```
2. **Install dependencies:**
   ```bash
   pip install customtkinter
   ```
3. **Build and Run:**
   The included `Makefile` handles the Rust compilation and Python execution:
   ```bash
   make run
   ```
4. **Usage:**
   - On first launch, set a master password.
   - Use the **+ New Note** button to create encrypted entries.
   - Click any card to edit or the **Delete** button to remove it.

## 🏗️ Implementation Roadmap

Our current focus is transitioning from a functional prototype to a polished productivity tool:

- [x] **UI Overhaul:** Migrated to CustomTkinter for a modern, sleek aesthetic with animations.
- [ ] **Functional Settings:** Implementing the persistence for appearance modes and auto-save.
- [ ] **Rich Text Support:** Implementing Markdown or RTF support for formatted notes.
- [ ] **Search & Filter:** Real-time search across note titles and content (decrypted in-memory).
- [ ] **Note Categories:** Folder support and tagging system for better organization.
- [ ] **Cross-Platform Packaging:** Native installers for macOS (.app), Windows (.exe), and Linux.

## 🧹 Maintenance
To remove build artifacts and local test notes:
```bash
make clean
```

---
*CaliNote: Your thoughts, secured.*
