import os
import re

import tempfile


file_path = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))


def read_file(filename: str) -> list:
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def test_read_file():
    # create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
        temp_filename = temp_file.name
        # Write some lines to the temporary file
        temp_file.write("line1\nline2\nline3\n")

    try:
        # call the read_file function
        result = read_file(temp_filename)
        # Verify the result
        assert result == ["line1", "line2", "line3"]
    finally:
        # clean up the temporary file
        os.remove(temp_filename)


def is_valid_email(email: str) -> bool:
    # regular expression for validating an email
    regex = r'^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,64}\.[A-Za-z]{2,24}$'

    # check if the email matches the regex
    if not re.match(regex, email):
        return False

    # split the email into local part and domain part
    local_part, domain_part = email.rsplit('@', 1)

    # check the lengths of the local part and domain part

    if len(local_part) > 64 or len(local_part) < 1:
        return False

    if len(domain_part) > 64 or len(domain_part) < 1:
        return False

    # split the domain into the main part and the top-level domain
    _, tld = domain_part.rsplit('.', 1)

    # check the length of the top-level domain
    if len(tld) < 2 or len(tld) > 24:
        return False

    # check the length of the full email
    if len(email) < 6 or len(email) > 128:
        return False

    # check for disposable domains
    disposable_domains = os.path.join(file_path, "tests", "disposable_email_blocklist.conf")
    if domain_part in disposable_domains:
        return False

    return True


class TestValidateEmailFormat(object):
    def test_email_input_format(self):
        assert is_valid_email("test@example.com") == True
        assert is_valid_email("test.user@domain.co") == True
        assert is_valid_email("test123@sub.domain.org") == True

    def test_email_for_at_the_rate_of_sign(self):
        assert is_valid_email("testexample.com") == False
        assert is_valid_email("test@@example.com") == False

    def test_the_local_part_of_email(self):
        assert is_valid_email("a" * 64 + "@domain.co") == True
        assert is_valid_email("a" * 65 + "@domain.co") == False

    def test_the_domain_part_of_email(self):
        assert is_valid_email("test" + "@" + "x" * 1 + ".com") == True
        assert is_valid_email("test" + "@" + "x" * 60 + ".com") == True

        assert is_valid_email("test" + "@" + "x" * 61 + ".com") == False

    def test_the_tld_of_the_domain_part_of_the_email(self):
        assert is_valid_email("test@tvs.co") == True
        assert is_valid_email("test@tvs." + "c" * 24) == True

        assert is_valid_email("test@tvs.c") == False
        assert is_valid_email("test@tvs." + "c" * 25) == False

    def test_character_length_of_the_email(self):
        assert is_valid_email("t@x.co") == True
        assert is_valid_email("t" * 64 + "@" + "x" * 60 + ".co") == True

        assert is_valid_email("t@x.c") == False
        assert is_valid_email("t" * 124 + "@x.co") == False

    def test_email_does_not_not_contain_disposable_domain(self):
        assert is_valid_email("test@example.com") == True
        assert is_valid_email("test@analyticalwe.us") == True
