from django.test import TestCase
from .models import Cliopatria

class CliopatriaModelTest(TestCase):
    def setUp(self):
        Cliopatria.objects.create(
            name="Test Polity",
            wikipedia_name="Test_Polity",
            seshat_id="SeshatID_123",
            area=100.0,
            start_year=1000,
            end_year=1100,
            polity_start_year=1000,
            polity_end_year=1100,
            colour="blue",
            components="Test Component",
            member_of="Test Member"
        )

    def test_cliopatria_creation(self):
        polity = Cliopatria.objects.get(name="Test Polity")
        self.assertEqual(polity.wikipedia_name, "Test_Polity")
        self.assertEqual(polity.seshat_id, "SeshatID_123")
        self.assertEqual(polity.area, 100.0)
        self.assertEqual(polity.start_year, 1000)
        self.assertEqual(polity.end_year, 1100)
        self.assertEqual(polity.colour, "blue")
        self.assertEqual(polity.components, "Test Component")
        self.assertEqual(polity.member_of, "Test Member")