import re

def normalize_owner(owner: str) -> str:
    o = owner.strip().lower()
    o = re.sub(r"\s+", "-", o)
    return o
