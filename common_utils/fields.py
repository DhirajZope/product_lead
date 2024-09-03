from django.db import models
from django.core.exceptions import ValidationError
import re

PHONE_NUMBER_REGEX = re.compile(r'^\+?1?\d{9,15}$')  # Example regex for international format


def validate_phone_number(value):
    """Validate the phone number format."""
    if not PHONE_NUMBER_REGEX.match(value):
        raise ValidationError('Enter a valid phone number.')


class PhoneNumberField(models.CharField):
    """Custom Phone Number Field for Django models."""

    def __init__(self, *args, **kwargs):
        # Set default max_length to 15, which is a common length for international numbers
        kwargs.setdefault('max_length', 15)
        # Add the custom validator
        kwargs.setdefault('validators', [validate_phone_number])
        super().__init__(*args, **kwargs)
