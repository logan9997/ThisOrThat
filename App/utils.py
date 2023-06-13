from password_strength import PasswordPolicy
from .config import (
    VALID_IMAGE_EXTENSIONS, MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH, MIN_SPECIAL_CHARS, MIN_UPPERCASE_CHARS
)

def is_image_file_extension_valid(image_path:str) -> bool:
    '''
    Check if the an images contains an any valid file extension.
    Valid image extensions saved in config.py
    '''
    for extension in VALID_IMAGE_EXTENSIONS:
        if image_path[-len(extension):] == extension:
            return True
    return False


def get_field_length_error(error:str) -> str:
    '''
    Return which field is has too many characters from form.errors
    '''

    if type(error) != str:
        error = str(error)

    if str(MAX_USERNAME_LENGTH) in error:
        return f'Username is too long ({MAX_USERNAME_LENGTH} Chars)'
    
    if str(MAX_PASSWORD_LENGTH) in error:
        return f'Password is too long ({MAX_PASSWORD_LENGTH} Chars)'
    return ''


def is_password_strong_enough(password:str) -> bool:
    '''
    Returns True is password passes all requirements,
    otherwise returns False
    '''
    policy = PasswordPolicy.from_names(
        length=MIN_PASSWORD_LENGTH,
        uppercase=MIN_UPPERCASE_CHARS,
        special=MIN_SPECIAL_CHARS
    )

    test_result = policy.test(password)

    if test_result == []:
        return True
    return False


def insert_spaces_in_tag_string(tag_string:str) -> str:
    '''
    Adds spaces after each comman in tag_string for readability on the UI
    '''
    tag_string = ''.join([
        char if char != ',' else f'{char} ' for char in tag_string
    ])
    return tag_string