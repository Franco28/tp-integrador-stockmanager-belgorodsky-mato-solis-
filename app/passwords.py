"""Funciones para guardar y comprobar contraseñas."""
import hashlib
import hmac
import secrets

N, R, P = 1 << 14, 8, 1


def crear_hash(password: str) -> str:
    """Guarda la contraseña como un hash, no como texto."""
    if len(password) < 12:
        raise ValueError("La contraseña debe tener al menos 12 caracteres")
    salt = secrets.token_bytes(16)
    key = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=N, r=R, p=P, dklen=32)
    return f"scrypt${N}${R}${P}${salt.hex()}${key.hex()}"


def verificar_hash(password: str, valor: str) -> bool:
    """Compara la contraseña ingresada con el hash guardado."""
    try:
        metodo, n, r, p, salt_hex, hash_hex = valor.split("$")
        if (metodo, int(n), int(r), int(p)) != ("scrypt", N, R, P):
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        if len(salt) != 16 or len(expected) != 32:
            return False
        actual = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=N, r=R, p=P, dklen=32)
        return hmac.compare_digest(actual, expected)
    except (ValueError, AttributeError, TypeError, OverflowError):
        return False
