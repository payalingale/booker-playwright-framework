def mask(secret):
    """It returns empty for None or empty secret and return **** for secret less than 8 characters and the last 4 characters"""
    if secret is None or secret == "":
        return "<empty>"
    if len(secret) < 8:
        return "****"
    return "****" + secret[-4:]
