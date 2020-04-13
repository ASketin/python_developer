import unittest
from hw2.Patient import Patient, PatientCollection
from datetime import datetime


class TestPatient(unittest.TestCase):

    def test_creation(self):
        simple = Patient("Кондрат", "Коловрат", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        class_simple = Patient.create("Кондрат", "Коловрат", "1978-01-31",
                                      "+7-916-000-00-00", "паспорт", "4514 000000")
        self.assertEqual(simple.first_name, class_simple.first_name)
        self.assertEqual(simple.last_name, class_simple.last_name)
        self.assertEqual(simple.birth_date, class_simple.birth_date)
        self.assertEqual(simple.phone, class_simple.phone)
        self.assertEqual(simple.document_type, class_simple.document_type)
        self.assertEqual(simple.document_id, class_simple.document_id)
        print("Creation: Done")

    def test_name(self):
        simple = Patient("abc", "abc", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        with self.assertRaises(ValueError):
            simple.first_name = 0
        with self.assertRaises(ValueError):
            simple.last_name = 0
        with self.assertRaises(ValueError):
            simple.first_name = "aaaaa"
        with self.assertRaises(ValueError):
            simple.first_name = "121"
        with self.assertRaises(ValueError):
            simple.first_name = "**##"
        with self.assertRaises(ValueError):
            simple.first_name = "Ян"
        print("Name modification: Done")

    def test_date(self):
        simple = Patient("abc", "abc", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        with self.assertRaises(ValueError):
            simple.birth_date = "aaaaa"
        with self.assertRaises(ValueError):
            simple.birth_date = 1
        simple.birth_date = "01-31-1978"
        self.assertEqual(simple.birth_date, datetime(1978, 1, 31).date())
        print("Date modification: Done")

    def test_phone(self):
        simple = Patient("abc", "abc", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        simple.phone = "+7(916) 000-00-01"
        self.assertEqual(simple.phone, "89160000001")
        simple.phone = "8(916) 000  00 01"
        self.assertEqual(simple.phone, "89160000001")
        with self.assertRaises(ValueError):
            simple.phone = "8916 000  00.01"
        self.assertEqual(simple.phone, "89160000001")
        with self.assertRaises(ValueError):
            simple.phone = "8916 000  00.016767"
        with self.assertRaises(ValueError):
            simple.phone = "8916 000  00.01 trash"
        with self.assertRaises(ValueError):
            simple.phone = "8916 000  00.01 мусор"
        with self.assertRaises(ValueError):
            simple.phone = "81110000001"
        with self.assertRaises(ValueError):
            simple.phone = "00000000000"
        print("Phone modification: Done")

    def test_doc(self):
        simple = Patient("abc", "abc", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        simple.document_type = "ПАСПОРТ"
        with self.assertRaises(ValueError):
            simple.document_type = "удостоверение"
        print("Doc check: Done")

    def test_id(self):
        simple = Patient("abc", "abc", "1978-01-31",
                         "+7-916-000-00-00", "паспорт", "4514 000000")
        with self.assertRaises(ValueError):
            simple.document_id = "4514 *** 000000"
        print("Id check: Done")


if __name__ == "__main_":
    unittest.main()
