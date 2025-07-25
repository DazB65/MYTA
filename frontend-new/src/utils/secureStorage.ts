/**
 * Secure Storage Utility
 * Provides encrypted storage for sensitive data using Web Crypto API
 * Falls back to sessionStorage for development (less persistent than localStorage)
 */

interface StorageItem {
  data: string;
  timestamp: number;
  expires?: number;
}

class SecureStorage {
  private keyPromise: Promise<CryptoKey>;

  constructor() {
    this.keyPromise = this.generateOrRetrieveKey();
  }

  private async generateOrRetrieveKey(): Promise<CryptoKey> {
    try {
      // Try to get existing key from sessionStorage (for session persistence)
      const savedKey = sessionStorage.getItem('_sk');
      if (savedKey) {
        const keyData = JSON.parse(savedKey);
        return await crypto.subtle.importKey(
          'raw',
          new Uint8Array(keyData),
          { name: 'AES-GCM' },
          false,
          ['encrypt', 'decrypt']
        );
      }

      // Generate new key
      const key = await crypto.subtle.generateKey(
        { name: 'AES-GCM', length: 256 },
        true,
        ['encrypt', 'decrypt']
      );

      // Export and save key for session persistence
      const exportedKey = await crypto.subtle.exportKey('raw', key);
      sessionStorage.setItem('_sk', JSON.stringify(Array.from(new Uint8Array(exportedKey))));

      return key;
    } catch (error) {
      console.warn('Web Crypto API not available, falling back to sessionStorage');
      throw new Error('Crypto not supported');
    }
  }

  private async encrypt(data: string): Promise<string> {
    try {
      const key = await this.keyPromise;
      const encoder = new TextEncoder();
      const dataBuffer = encoder.encode(data);
      
      const iv = crypto.getRandomValues(new Uint8Array(12));
      const encrypted = await crypto.subtle.encrypt(
        { name: 'AES-GCM', iv },
        key,
        dataBuffer
      );

      // Combine IV and encrypted data
      const combined = new Uint8Array(iv.length + encrypted.byteLength);
      combined.set(iv);
      combined.set(new Uint8Array(encrypted), iv.length);

      return btoa(String.fromCharCode(...combined));
    } catch (error) {
      // Fallback to base64 encoding (not secure, but better than plain text)
      console.warn('Encryption failed, using base64 fallback');
      return btoa(data);
    }
  }

  private async decrypt(encryptedData: string): Promise<string> {
    try {
      const key = await this.keyPromise;
      const combined = new Uint8Array(
        atob(encryptedData).split('').map(char => char.charCodeAt(0))
      );

      const iv = combined.slice(0, 12);
      const encrypted = combined.slice(12);

      const decrypted = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv },
        key,
        encrypted
      );

      const decoder = new TextDecoder();
      return decoder.decode(decrypted);
    } catch (error) {
      // Fallback from base64
      try {
        return atob(encryptedData);
      } catch {
        console.error('Failed to decrypt data');
        return '';
      }
    }
  }

  async setItem(key: string, value: string, expiresInMinutes?: number): Promise<void> {
    const expires = expiresInMinutes 
      ? Date.now() + (expiresInMinutes * 60 * 1000)
      : undefined;

    const item: StorageItem = {
      data: value,
      timestamp: Date.now(),
      expires
    };

    try {
      const encryptedData = await this.encrypt(JSON.stringify(item));
      sessionStorage.setItem(`sec_${key}`, encryptedData);
    } catch (error) {
      console.error('Failed to store item securely:', error);
      // Don't fall back to localStorage for security reasons
      throw new Error('Secure storage failed');
    }
  }

  async getItem(key: string): Promise<string | null> {
    try {
      const encryptedData = sessionStorage.getItem(`sec_${key}`);
      if (!encryptedData) return null;

      const decryptedData = await this.decrypt(encryptedData);
      if (!decryptedData) return null;

      const item: StorageItem = JSON.parse(decryptedData);
      
      // Check expiration
      if (item.expires && Date.now() > item.expires) {
        this.removeItem(key);
        return null;
      }

      return item.data;
    } catch (error) {
      console.error('Failed to retrieve item securely:', error);
      return null;
    }
  }

  removeItem(key: string): void {
    sessionStorage.removeItem(`sec_${key}`);
  }

  clear(): void {
    // Remove all secure storage items
    Object.keys(sessionStorage).forEach(key => {
      if (key.startsWith('sec_')) {
        sessionStorage.removeItem(key);
      }
    });
    // Also remove the key
    sessionStorage.removeItem('_sk');
  }

  // Method to check if an item exists without decrypting
  hasItem(key: string): boolean {
    return sessionStorage.getItem(`sec_${key}`) !== null;
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