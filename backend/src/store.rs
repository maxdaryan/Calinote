use std::fs;
use std::path::Path;
use serde::{Deserialize, Serialize};

use crate::crypto::{derive_key, encrypt, decrypt, random_salt};

/// Magic bytes at the start of every .cali file.
const MAGIC: &[u8; 4] = b"CALI";

/// .cali file binary layout:
///   [0..4]   = magic "CALI"
///   [4..20]  = 16-byte Argon2 salt
///   [20..32] = 12-byte AES-GCM nonce
///   [32..]   = ciphertext (AES-GCM encrypted payload, includes 16-byte GCM tag)
///
/// The plaintext payload is: `title\0body`

#[derive(Serialize, Deserialize, Debug)]
pub struct NoteInfo {
    pub filename: String,
    pub path: String,
}

/// Save an encrypted note to `path`.
pub fn save_note(path: &Path, title: &str, body: &str, password: &str) -> Result<(), String> {
    let plaintext = format!("{}\x00{}", title, body);
    let salt = random_salt();
    let key = derive_key(password, &salt);
    let (nonce, ciphertext) = encrypt(plaintext.as_bytes(), &key);

    let mut blob: Vec<u8> = Vec::with_capacity(4 + 16 + 12 + ciphertext.len());
    blob.extend_from_slice(MAGIC);
    blob.extend_from_slice(&salt);
    blob.extend_from_slice(&nonce);
    blob.extend_from_slice(&ciphertext);

    fs::write(path, &blob).map_err(|e| format!("File write error: {e}"))
}

/// Load and decrypt a note from `path`.
/// Returns (title, body) or an error.
pub fn load_note(path: &Path, password: &str) -> Result<(String, String), String> {
    let blob = fs::read(path).map_err(|e| format!("File read error: {e}"))?;

    if blob.len() < 4 + 16 + 12 + 16 {
        return Err("File too short — not a valid .ghost file.".into());
    }
    if &blob[0..4] != MAGIC {
        return Err("Not a .ghost file (bad magic bytes).".into());
    }

    let salt: [u8; 16] = blob[4..20].try_into().unwrap();
    let nonce: [u8; 12] = blob[20..32].try_into().unwrap();
    let ciphertext = &blob[32..];

    let key = derive_key(password, &salt);
    let plaintext_bytes = decrypt(ciphertext, &key, &nonce)?;
    let plaintext = String::from_utf8(plaintext_bytes)
        .map_err(|_| "Decrypted content is not valid UTF-8.".to_string())?;

    let mut parts = plaintext.splitn(2, '\x00');
    let title = parts.next().unwrap_or("").to_string();
    let body  = parts.next().unwrap_or("").to_string();

    Ok((title, body))
}

/// List all .cali files in `dir`. Does NOT decrypt anything.
pub fn list_notes(dir: &Path) -> Result<Vec<NoteInfo>, String> {
    if !dir.exists() {
        fs::create_dir_all(dir).map_err(|e| format!("Cannot create notes dir: {e}"))?;
    }

    let entries = fs::read_dir(dir).map_err(|e| format!("Cannot read notes dir: {e}"))?;
    let mut notes: Vec<NoteInfo> = entries
        .filter_map(|e| e.ok())
        .filter(|e| {
            e.path()
                .extension()
                .map(|ext| ext == "cali")
                .unwrap_or(false)
        })
        .map(|e| {
            let path = e.path();
            let filename = path
                .file_stem()
                .unwrap_or_default()
                .to_string_lossy()
                .to_string();
            NoteInfo {
                filename,
                path: path.to_string_lossy().to_string(),
            }
        })
        .collect();

    notes.sort_by(|a, b| a.filename.cmp(&b.filename));
    Ok(notes)
}

/// Delete a .ghost file.
pub fn delete_note(path: &Path) -> Result<(), String> {
    fs::remove_file(path).map_err(|e| format!("Delete error: {e}"))
}
