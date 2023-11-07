from django.test import SimpleTestCase

from utility.versioning import APIVersion


class TestVersionType(SimpleTestCase):
    def test_valid_version_format(self):
        version_number = "1.2.3"
        version = APIVersion(version_number)
        self.assertEqual(version.header, version_number)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)

    def test_invalid_version_format(self):
        version_number = "1.2"
        with self.assertRaises(ValueError) as ex:
            APIVersion(version_number)

        self.assertIn("This version has wrong format,", str(ex.exception))

    def test_is_valid_version(self):
        version = APIVersion("1.9.3")

        self.assertTrue(version.is_valid("1.9.3"))
        self.assertTrue(version.is_valid("1.9.2"))
        self.assertTrue(version.is_valid("0.10.4"))
        self.assertTrue(version.is_valid("1.8.5"))

        self.assertFalse(version.is_valid("1.9.4"))
        self.assertFalse(version.is_valid("2.0.0"))
        self.assertFalse(version.is_valid("2.8.4"))

    def test_is_child_version(self):
        version = APIVersion("1.9.0")

        self.assertTrue(version.is_child("1.8.8"))
        self.assertTrue(version.is_child("1.10.1"))

        self.assertFalse(version.is_child("0.10.10"))
        self.assertFalse(version.is_child("2.8.0"))

    def test_comparison_operators(self):
        version = APIVersion("1.2.4")
        self.assertTrue(APIVersion("1.2.5") == "1.2.5")
        self.assertFalse(version == "1.2.5")

        self.assertFalse(APIVersion("1.2.5") != "1.2.5")
        self.assertTrue(version != "1.3.4")

        self.assertTrue(version > "0.1.3")
        self.assertTrue(version > "1.1.4")
        self.assertFalse(version > "1.2.3")

        self.assertTrue(version > "0.3.5")
        self.assertTrue(version > "1.1.5")
        self.assertTrue(version > "0.16.5")
        self.assertTrue(version > "1.1.23")

        self.assertTrue(version >= "1.2.25")

        self.assertTrue(version < "2.3.5")
        self.assertTrue(version < "2.2.4")
        self.assertTrue(version < "1.3.4")
        self.assertTrue(version < "2.1.3")
        self.assertTrue(version < "1.3.3")
        self.assertTrue(APIVersion("1.2.34") < "2.1.30")
        self.assertTrue(APIVersion("1.2.44") < "1.3.35")

        self.assertTrue(version <= "1.2.4")
