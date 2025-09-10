"""
Sprint 25.4 — PII encryption helper R2 (protocol v2)
DEMO-ONLY: stream XOR with SHA256-derived keystream; replace with libsodium in later sprint.
"""
import os, base64, hashlib

def _keystream(key: bytes, nonce: bytes, nbytes: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < nbytes:
        h = hashlib.sha256(key + nonce + counter.to_bytes(4,'big')).digest()
        out.extend(h)
        counter += 1
    return bytes(out[:nbytes])

def encrypt_pii(plaintext: str, key: str) -> str:
    if plaintext is None: plaintext = ""
    nonce = os.urandom(12)
    pt = plaintext.encode('utf-8')
    ks = _keystream(key.encode('utf-8'), nonce, len(pt))
    ct = bytes([a ^ b for a,b in zip(pt, ks)])
    blob = nonce + ct
    return base64.urlsafe_b64encode(blob).decode('ascii')

def decrypt_pii(token: str, key: str) -> str:
    raw = base64.urlsafe_b64decode(token.encode('ascii'))
    nonce, ct = raw[:12], raw[12:]
    ks = _keystream(key.encode('utf-8'), nonce, len(ct))
    pt = bytes([a ^ b for a,b in zip(ct, ks)])
    return pt.decode('utf-8', errors='replace')
