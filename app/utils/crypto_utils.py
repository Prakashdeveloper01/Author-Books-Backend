


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from app.config import CONFIG_SETTINGS
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from hashlib import sha256

_backend = default_backend()
_encryption_iv = CONFIG_SETTINGS.MAIN_ENCRYPTION_IV  # Initialization vector used for encryption
_encryption_key = CONFIG_SETTINGS.MAIN_ENCRYPTION_KEY  # Key used for encryption
_cipher = Cipher(algorithms.AES(_encryption_key.encode()), modes.CTR(_encryption_iv.encode()), backend=_backend)

def encrypt(data: str | None) -> str:
    """
    Encrypts the provided data using AES encryption algorithm.

    Args:
        data (str): The data to be encrypted.

    Returns
    -------
        str: The encrypted data encoded in Base64.
    """
    data = str(data)
    encryptor = _cipher.encryptor()
    encryption = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(encryption).decode("utf-8")


def decrypt(encrypted_data_str: str) -> str:
    """
    Decrypts the provided encrypted data.

    Args:
        encrypted_data_str (str): The encrypted data encoded in Base64.

    Returns
    -------
        str: The decrypted data.
    """
    encrypted_data = base64.b64decode(encrypted_data_str.encode("utf-8"))
    decryptor = _cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data.decode("utf-8")

def hash_password(password: str) -> str:
    """Hash password."""
    salt = base64.urlsafe_b64encode(sha256(password.encode()).digest())[:16]
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    key = kdf.derive(password.encode())
    return base64.b64encode(salt + key).decode()


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    decoded = base64.b64decode(hashed_password)
    salt = decoded[:16]
    key = decoded[16:]
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    derived_key = kdf.derive(plain_password.encode())
    return derived_key == key
