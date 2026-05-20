use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm, Key, Nonce,
};
use argon2::Argon2;
use rand::RngCore;

/// Derive a 32-byte AES key from a password + raw 16-byte salt using Argon2id.
pub fn derive_key(password: &str, salt_bytes: &[u8; 16]) -> [u8; 32] {
    let mut key = [0u8; 32];
    Argon2::default()
        .hash_password_into(password.as_bytes(), salt_bytes, &mut key)
        .expect("Argon2 key derivation failed");
    key
}

/// Generate a random 16-byte salt.
pub fn random_salt() -> [u8; 16] {
    let mut salt = [0u8; 16];
    OsRng.fill_bytes(&mut salt);
    salt
}

/// Encrypt `plaintext` with AES-256-GCM using the given key.
/// Returns (nonce [12 bytes], ciphertext+tag).
pub fn encrypt(plaintext: &[u8], key: &[u8; 32]) -> ([u8; 12], Vec<u8>) {
    let cipher = Aes256Gcm::new(Key::<Aes256Gcm>::from_slice(key));
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
    let ciphertext = cipher
        .encrypt(&nonce, plaintext)
        .expect("AES-GCM encryption failed");
    let mut nonce_bytes = [0u8; 12];
    nonce_bytes.copy_from_slice(&nonce);
    (nonce_bytes, ciphertext)
}

/// Decrypt `ciphertext` (with embedded GCM tag) using key + nonce.
/// Returns Err if the password is wrong or the file is corrupt.
pub fn decrypt(ciphertext: &[u8], key: &[u8; 32], nonce_bytes: &[u8; 12]) -> Result<Vec<u8>, String> {
    let cipher = Aes256Gcm::new(Key::<Aes256Gcm>::from_slice(key));
    let nonce = Nonce::from_slice(nonce_bytes);
    cipher
        .decrypt(nonce, ciphertext)
        .map_err(|_| "Decryption failed — wrong password or corrupted file.".to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn roundtrip() {
        let password = "super_secret";
        let salt = random_salt();
        let key = derive_key(password, &salt);
        let plaintext = b"Hello, Ghost Notes!";
        let (nonce, ct) = encrypt(plaintext, &key);
        let decrypted = decrypt(&ct, &key, &nonce).unwrap();
        assert_eq!(decrypted, plaintext);
    }

    #[test]
    fn wrong_password_fails() {
        let salt = random_salt();
        let key_good = derive_key("correct", &salt);
        let key_bad  = derive_key("wrong",   &salt);
        let (nonce, ct) = encrypt(b"secret", &key_good);
        assert!(decrypt(&ct, &key_bad, &nonce).is_err());
    }
}
