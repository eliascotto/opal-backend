import uuid
from slugify import slugify
from secrets import token_urlsafe


def generate_uuid():
    """
    Generate a valid uuid4
    """
    return uuid.uuid4()


def create_url(string):
    """
    Implement 3 alphadigit using blake2b(digest_size=3).hexdigest()
    in order to avoid duplicated articles per user
    """
    return slugify(string, max_length=100)


def compare_raw_str(rawstrA, rawstrB):
    """
    Compare two strings stripping with casefold compare
    """
    return rawstrA.strip().casefold() == rawstrB.strip().casefold()


def generate_rand_id():
    """
    Return a base64 url safe id of 12 char
    """
    return token_urlsafe(9)
