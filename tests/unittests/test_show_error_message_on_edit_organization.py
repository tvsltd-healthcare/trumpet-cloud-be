import pytest

from typing import Dict, List

error_message_mappings = {
    "organization_name": {
        0: 'valid',
        1: 'Enter organization name',
        2: 'Organization name must be less than 255 characters'
    },
    "organization_address": {
        0: 'valid',
        1: 'Enter organization address',
        2: 'Organization address must be less than 255 characters'
    },
    "organization_phone_no": {
        0: 'valid',
        1: 'Enter organization phone no',
        2: 'Please enter a valid organization phone no'
    },
    "file": {
        0: 'valid',
        1: 'Upload not more than 5 files',
        2: 'Each file should be less than 5 mb',
        3: 'Upload only .doc, .pdf, .jpg, .png files',
    }
}


def show_organization_error_message(data: Dict[str, int]) -> List[str]:
    """
    function id: 105
    Generates a list of error messages based on the input data.

    Args:
        data (Dict[str, int]): A dictionary where:
            - Keys are field names (strings).
            - Values are predefined integers representing error codes.

    Returns:
        List[str]: A list of error messages corresponding to the error codes in the input dictionary.
        An empty list indicates that there are no error messages.
    """

    messages = []

    for field, error_code in data.items():
        # Check if the field exists in the error_message_mappings
        if field in error_message_mappings:
            # Get the corresponding error message based on the error code
            error_message = error_message_mappings[field].get(error_code, 'Unknown error')
            # If the error message is not 'valid', add it to the messages list
            if error_message != 'valid':
                messages.append(error_message)

    return messages
    

class TestShowErrorMessages(object):
    def test_organization_name(self):
        assert "Enter organization name" in show_organization_error_message({'organization_name': 1})
        assert "Organization name must be less than 255 characters" in show_organization_error_message({'organization_name': 2})
        
        assert "Enter organization name" not in show_organization_error_message({'organization_name': 0})
        assert "Organization name must be less than 255 characters" not in show_organization_error_message({'organization_name': 0})
        
    def test_organization_address(self):
        assert "Enter organization address" in show_organization_error_message({'organization_address': 1})
        assert "Organization address must be less than 255 characters" in show_organization_error_message({'organization_address': 2})
        
        assert "Enter organization address" not in show_organization_error_message({'organization_address': 0})
        assert "Organization address must be less than 255 characters" not in show_organization_error_message({'organization_address': 0})

    def test_organization_phone_no(self):
        assert "Enter organization phone no" in show_organization_error_message({'organization_phone_no': 1})
        assert "Please enter a valid organization phone no" in show_organization_error_message({'organization_phone_no': 2})
        
        assert "Enter organization phone no" not in show_organization_error_message({'organization_phone_no': 0})
        assert "Please enter a valid organization phone no" not in show_organization_error_message({'organization_phone_no': 0})
    
    def test_file_too_many_uploads(self):
        assert "Upload not more than 5 files" in show_organization_error_message({'file': 1})
        assert "Upload not more than 5 files" not in show_organization_error_message({'file': 0})

    def test_file_size_limit_exceeded(self):
        assert "Each file should be less than 5 mb" in show_organization_error_message({'file': 2})
        assert "Each file should be less than 5 mb" not in show_organization_error_message({'file': 0})

    def test_file_invalid_format(self):
        assert "Upload only .doc, .pdf, .jpg, .png files" in show_organization_error_message({'file': 3})
        assert "Upload only .doc, .pdf, .jpg, .png files" not in show_organization_error_message({'file': 0})

    def test_unknown_file_error_code(self):
        assert "Unknown error" in show_organization_error_message({'file': 99})
        assert "Unknown error" not in show_organization_error_message({'file': 0})

    def test_unknown_error_code(self):
        # Test for unknown error code for a known field
        assert "Unknown error" in show_organization_error_message({'organization_name': 99})
        assert "Unknown error" not in show_organization_error_message({'organization_name': 0})
