/**
 * Secure Storage Implementation
 * Provides encrypted storage for sensitive data using Web Crypto API
 * Falls back to sessionStorage for browsers without Web Crypto API
 */

interface StorageItem {
  value: string;
  expires: number;
  encrypted: boolean;
}

class SecureStorage {
  private readonly storageKey = 'Vidalytics_SecureStorage';
  private readonly cryptoKey: CryptoKey | null = null;
  private readonly useEncryption: boolean;

  constructor() {
    this.useEncryption = this.isWebCryptoAvailable();
    if (this.useEncryption) {
      this.initializeCrypto();
    }
  }

  private isWebCryptoAvailable(): boolean {
    return typeof window !== 'undefined' && 
           'crypto' in window && 
           'subtle' in window.crypto &&
           'getRandomValues' in window.crypto;
  }

  private async initializeCrypto(): Promise<void> {
    try {
      // Generate a key for AES-GCM encryption
      const keyMaterial = await window.crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode('Vidalytics-Secure-Storage-Key-2024'),
        { name: 'PBKDF2' },
        false,
        ['deriveBits', 'deriveKey']
      );

      this.cryptoKey = await window.crypto.subtle.deriveKey(
        {
          name: 'PBKDF2',
          salt: new TextEncoder().encode('Vidalytics-Salt'),
          iterations: 100000,
          hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-GCM', length: 256 },
        false,
        ['encrypt', 'decrypt']
      );
    } catch (error) {
      console.warn('Failed to initialize crypto, falling back to sessionStorage:', error);
      this.useEncryption = false;
    }
  }

  private async encrypt(data: string): Promise<string> {
    if (!this.cryptoKey || !this.useEncryption) {
      return data;
    }

    try {
      const iv = window.crypto.getRandomValues(new Uint8Array(12));
      const encodedData = new TextEncoder().encode(data);
      
      const encrypted = await window.crypto.subtle.encrypt(
        { name: 'AES-GCM', iv },
        this.cryptoKey,
        encodedData
      );

      const encryptedArray = new Uint8Array(encrypted);
      const combined = new Uint8Array(iv.length + encryptedArray.length);
      combined.set(iv);
      combined.set(encryptedArray, iv.length);

      return btoa(String.fromCharCode(...combined));
    } catch (error) {
      console.warn('Encryption failed, storing unencrypted:', error);
      return data;
    }
  }

  private async decrypt(encryptedData: string): Promise<string> {
    if (!this.cryptoKey || !this.useEncryption) {
      return encryptedData;
    }

    try {
      const combined = new Uint8Array(
        atob(encryptedData).split('').map(char => char.charCodeAt(0))
      );
      
      const iv = combined.slice(0, 12);
      const encrypted = combined.slice(12);

      const decrypted = await window.crypto.subtle.decrypt(
        { name: 'AES-GCM', iv },
        this.cryptoKey,
        encrypted
      );

      return new TextDecoder().decode(decrypted);
    } catch (error) {
      console.warn('Decryption failed, returning encrypted data:', error);
      return encryptedData;
    }
  }

  async setItem(key: string, value: string, expiresInMinutes: number = 60): Promise<void> {
    try {
      const expires = Date.now() + (expiresInMinutes * 60 * 1000);
      const item: StorageItem = {
        value: await this.encrypt(value),
        expires,
        encrypted: this.useEncryption
      };

      const storage = this.getStorage();
      const allData = this.getAllData();
      allData[key] = item;
      
      storage.setItem(this.storageKey, JSON.stringify(allData));
    } catch (error) {
      console.error('Failed to set secure storage item:', error);
      // Fallback to regular sessionStorage
      sessionStorage.setItem(key, value);
    }
  }

  async getItem(key: string): Promise<string | null> {
    try {
      const storage = this.getStorage();
      const allData = this.getAllData();
      const item = allData[key];

      if (!item) {
        return null;
      }

      // Check expiration
      if (Date.now() > item.expires) {
        this.removeItem(key);
        return null;
      }

      return await this.decrypt(item.value);
    } catch (error) {
      console.error('Failed to get secure storage item:', error);
      // Fallback to regular sessionStorage
      return sessionStorage.getItem(key);
    }
  }

  removeItem(key: string): void {
    try {
      const storage = this.getStorage();
      const allData = this.getAllData();
      delete allData[key];
      storage.setItem(this.storageKey, JSON.stringify(allData));
    } catch (error) {
      console.error('Failed to remove secure storage item:', error);
      // Fallback to regular sessionStorage
      sessionStorage.removeItem(key);
    }
  }

  clear(): void {
    try {
      const storage = this.getStorage();
      storage.removeItem(this.storageKey);
    } catch (error) {
      console.error('Failed to clear secure storage:', error);
      // Fallback to regular sessionStorage
      sessionStorage.clear();
    }
  }

  hasItem(key: string): boolean {
    try {
      const allData = this.getAllData();
      const item = allData[key];
      return item !== undefined && Date.now() <= item.expires;
    } catch (error) {
      console.error('Failed to check secure storage item:', error);
      return sessionStorage.getItem(key) !== null;
    }
  }

  private getStorage(): Storage {
    // Use sessionStorage for better security (cleared when browser closes)
    return sessionStorage;
  }

  private getAllData(): Record<string, StorageItem> {
    try {
      const storage = this.getStorage();
      const data = storage.getItem(this.storageKey);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Failed to parse secure storage data:', error);
      return {};
    }
  }
}

// Create singleton instance
export const secureStorage = new SecureStorage();

// Utility functions for common use cases
export const secureTokenStorage = {
  async setToken(token: string, expiresInMinutes: number = 60): Promise<void> {
    await secureStorage.setItem('auth_token', token, expiresInMinutes);
  },

  async getToken(): Promise<string | null> {
    return await secureStorage.getItem('auth_token');
  },

  clearToken(): void {
    secureStorage.removeItem('auth_token');
  },

  async setUserData(userData: any): Promise<void> {
    await secureStorage.setItem('user_data', JSON.stringify(userData), 480); // 8 hours
  },

  async getUserData(): Promise<any | null> {
    const data = await secureStorage.getItem('user_data');
    return data ? JSON.parse(data) : null;
  },

  clearUserData(): void {
    secureStorage.removeItem('user_data');
  },

  clearAll(): void {
    secureStorage.clear();
  }
};

export default secureStorage;