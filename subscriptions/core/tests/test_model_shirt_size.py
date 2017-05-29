from django.core.exceptions import ValidationError
from django.test import TestCase
from subscriptions.core.models import ShirtSize
from unittest import skip

class ShirtSizeModelTest(TestCase):
    def setUp(self):
        self.shirt_size = ShirtSize(
            shirt_size='P',
            file_shirt_size='Camiseta P',
        )

    def test_create_shirt_size(self):
        self.shirt_size.save()
        self.assertTrue(ShirtSize.objects.exists())

    @skip('Validation not implemented')
    def test_invalid_shirt_size(self):
        shirt_size = ShirtSize(
            shirt_size='invalid_shirt_size',
            file_shirt_size='Camiseta P',
        )
        with self.assertRaises(ValidationError):
            shirt_size.save()
        self.assertFalse(ShirtSize.objects.exists())

    def test_str(self):
        self.assertEqual('P', str(self.shirt_size))