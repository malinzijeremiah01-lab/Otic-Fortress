def has_role(claims: dict, role: str) -> bool:
    return role in claims.get("roles", [])
