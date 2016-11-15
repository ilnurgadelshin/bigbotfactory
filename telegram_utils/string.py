
def to_utf8(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    elif isinstance(s, str):
        # Must be encoded in UTF-8
        s.decode('utf8')
    return s
