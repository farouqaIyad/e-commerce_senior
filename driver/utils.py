from django.core.exceptions import ValidationError


def validate_lat(value):
    if value < -90.00 or value > 90.00:
        raise ValidationError("Rating must be between -90 and 90.")


def validate_long(value):
    if value < -180.00 or value > 180.00:
        raise ValidationError("Rating must be between -180 and 180.")
