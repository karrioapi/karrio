/**
 * OAuth Encryption Utilities
 *
 * Provides AES-GCM encryption/decryption for secure OAuth credential storage.
 * Uses Web Crypto API for browser-compatible cryptographic operations.
 */

export interface EncryptedData {
  ciphertext: string;
  iv: string;
  key: string;
}

export const OAUTH_STORAGE_KEY = "karrio_oauth_result";

// Functional helper: convert ArrayBuffer/Uint8Array to base64
const toBase64 = (buffer: ArrayBuffer | Uint8Array): string =>
  btoa(
    Array.from(buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer))
      .map((byte) => String.fromCharCode(byte))
      .join("")
  );

// Functional helper: convert base64 string to Uint8Array
const fromBase64 = (base64: string): Uint8Array =>
  Uint8Array.from(atob(base64), (char) => char.charCodeAt(0));

/**
 * Encrypts data using AES-GCM with Web Crypto API.
 * Generates a random 256-bit key and 96-bit IV for each encryption.
 */
export const encryptData = async (data: string): Promise<EncryptedData> => {
  const key = await crypto.subtle.generateKey(
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );

  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encodedData = new TextEncoder().encode(data);

  const [encryptedBuffer, exportedKey] = await Promise.all([
    crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, encodedData),
    crypto.subtle.exportKey("raw", key),
  ]);

  return {
    ciphertext: toBase64(encryptedBuffer),
    iv: toBase64(iv),
    key: toBase64(exportedKey),
  };
};

/**
 * Decrypts data that was encrypted with encryptData.
 * Imports the key and uses AES-GCM decryption.
 */
export const decryptData = async (encrypted: EncryptedData): Promise<string> => {
  const ciphertext = new Uint8Array(fromBase64(encrypted.ciphertext));
  const iv = new Uint8Array(fromBase64(encrypted.iv));
  const keyData = new Uint8Array(fromBase64(encrypted.key));

  const key = await crypto.subtle.importKey(
    "raw",
    keyData,
    { name: "AES-GCM", length: 256 },
    false,
    ["decrypt"]
  );

  const decryptedBuffer = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv },
    key,
    ciphertext
  );

  return new TextDecoder().decode(decryptedBuffer);
};

/**
 * Stores encrypted OAuth result in localStorage.
 * Uses localStorage instead of sessionStorage because popup windows
 * have separate sessionStorage contexts from their opener.
 * Returns true on success, false on failure.
 */
export const storeEncryptedOAuthResult = async (result: unknown): Promise<boolean> => {
  try {
    console.log("[OAuth] Storing encrypted result...");
    const encrypted = await encryptData(JSON.stringify(result));
    localStorage.setItem(OAUTH_STORAGE_KEY, JSON.stringify(encrypted));
    console.log("[OAuth] Result stored successfully");
    return true;
  } catch (e) {
    console.error("[OAuth] Failed to encrypt/store OAuth result:", e);
    return false;
  }
};

/**
 * Retrieves and decrypts OAuth result from localStorage.
 * Automatically clears the stored data after retrieval.
 * Returns null if no data found or decryption fails.
 */
export const retrieveEncryptedOAuthResult = async <T = unknown>(): Promise<T | null> => {
  try {
    const storedData = localStorage.getItem(OAUTH_STORAGE_KEY);
    if (!storedData) return null;

    console.log("[OAuth] Found stored data, decrypting...");

    // Clear immediately after reading for security
    localStorage.removeItem(OAUTH_STORAGE_KEY);

    const encrypted: EncryptedData = JSON.parse(storedData);
    const decrypted = await decryptData(encrypted);
    const result = JSON.parse(decrypted) as T;
    console.log("[OAuth] Decryption successful");
    return result;
  } catch (e) {
    console.error("[OAuth] Failed to retrieve/decrypt OAuth result:", e);
    localStorage.removeItem(OAUTH_STORAGE_KEY);
    return null;
  }
};
