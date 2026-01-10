#!/usr/bin/env python3
"""
Secure API Key Manager for I Am Ironman
Handles secure storage and retrieval of API keys locally
"""

import os
import json
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from datetime import datetime


class SecureAPIManager:
    """Securely manage API keys with encryption"""

    def __init__(self):
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        self.key_file = self.data_dir / 'api_key.encrypted'
        self.master_key_file = self.data_dir / '.master_key'

    def _get_or_create_master_key(self):
        """Get existing or create new master encryption key"""
        if self.master_key_file.exists():
            with open(self.master_key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new master key
            key = Fernet.generate_key()
            # Store master key securely (file permissions should restrict access)
            with open(self.master_key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions (Unix only)
            try:
                os.chmod(str(self.master_key_file), 0o600)
            except:
                pass  # Windows doesn't support Unix permissions
            return key

    def _encrypt_api_key(self, api_key: str) -> bytes:
        """Encrypt API key using Fernet (symmetric encryption)"""
        master_key = self._get_or_create_master_key()
        cipher_suite = Fernet(master_key)
        encrypted = cipher_suite.encrypt(api_key.encode())
        return encrypted

    def _decrypt_api_key(self, encrypted_key: bytes) -> str:
        """Decrypt API key"""
        master_key = self._get_or_create_master_key()
        cipher_suite = Fernet(master_key)
        try:
            decrypted = cipher_suite.decrypt(encrypted_key).decode()
            return decrypted
        except Exception as e:
            print(f"❌ Error decrypting API key: {e}")
            return None

    def save_api_key(self, api_key: str, provider: str = 'google') -> bool:
        """
        Save API key securely
        Args:
            api_key: The API key to store
            provider: Name of the API provider (google, openai, etc.)
        """
        try:
            # Encrypt the API key
            encrypted_key = self._encrypt_api_key(api_key)

            # Create metadata
            metadata = {
                'provider': provider,
                'created_at': datetime.now().isoformat(),
                'encrypted': True,
                'key_length': len(api_key)
            }

            # Save encrypted key and metadata
            with open(self.key_file, 'wb') as f:
                f.write(encrypted_key)

            # Save metadata separately
            with open(self.data_dir / f'{provider}_meta.json', 'w') as f:
                json.dump(metadata, f, indent=2)

            # Set restrictive permissions
            try:
                os.chmod(str(self.key_file), 0o600)
                os.chmod(str(self.data_dir / f'{provider}_meta.json'), 0o600)
            except:
                pass

            print(f"✅ API key for {provider} saved securely")
            return True
        except Exception as e:
            print(f"❌ Error saving API key: {e}")
            return False

    def get_api_key(self, provider: str = 'google') -> str:
        """
        Retrieve and decrypt API key
        Returns None if key not found or decryption fails
        """
        try:
            if not self.key_file.exists():
                return None

            with open(self.key_file, 'rb') as f:
                encrypted_key = f.read()

            decrypted_key = self._decrypt_api_key(encrypted_key)
            return decrypted_key
        except Exception as e:
            print(f"❌ Error retrieving API key: {e}")
            return None

    def has_api_key(self, provider: str = 'google') -> bool:
        """Check if API key exists"""
        return self.key_file.exists()

    def delete_api_key(self, provider: str = 'google') -> bool:
        """Delete stored API key"""
        try:
            if self.key_file.exists():
                self.key_file.unlink()
            meta_file = self.data_dir / f'{provider}_meta.json'
            if meta_file.exists():
                meta_file.unlink()
            print(f"✅ API key for {provider} deleted")
            return True
        except Exception as e:
            print(f"❌ Error deleting API key: {e}")
            return False

    def prompt_for_api_key(self) -> str:
        """
        Securely prompt user for API key (input is hidden)
        """
        print("\n" + "="*60)
        print("🔐 API Key Setup")
        print("="*60)
        print("Your API key will be encrypted and stored locally.")
        print("It will NOT be saved to GitHub or shared.\n")

        while True:
            api_key = getpass.getpass("Enter your Google API key: ")
            if not api_key:
                print("❌ API key cannot be empty")
                continue
            if len(api_key) < 10:
                print("❌ API key seems too short")
                continue
            # Confirm
            confirm = input("Confirm? (y/n): ").lower()
            if confirm == 'y':
                return api_key
            else:
                print("Re-enter your key\n")


def setup_api_key():
    """Interactive API key setup for first run"""
    manager = SecureAPIManager()

    if manager.has_api_key():
        choice = input("API key already exists. Replace? (y/n): ").lower()
        if choice != 'y':
            return manager

    api_key = manager.prompt_for_api_key()
    manager.save_api_key(api_key, 'google')
    print(f"\n✅ Setup complete!\nYour API key has been securely stored.")
    print("="*60 + "\n")
    return manager


if __name__ == '__main__':
    # Test the API manager
    manager = SecureAPIManager()
    print("Secure API Manager Module")
    print("For use in main.py - not meant to run directly")
