from urllib.parse import urlunsplit


def create_url(schema, username="", password="", host=None, port=None):
    netloc = ""
    if username or password:
        netloc = f"{username}:{password}"
    if host:
        netloc += ("@" if netloc else "") + host
    if port:
        netloc += ":" + str(port)
    return urlunsplit((schema, netloc, "", "", ""))
