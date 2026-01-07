import hashlib

class Hasher:
    @staticmethod
    def compute_hash(content: bytes) -> str:
        """מחזיר SHA256 hash של תוכן הבייטים"""
        sha256 = hashlib.sha256()
        sha256.update(content)
        return sha256.hexdigest()
