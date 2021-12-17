"""Deliverable 1 test"""
import unittest
from methods import Token, Restricted


class TestStringMethods(unittest.TestCase):
    """Testing login and restricted data"""
    def setUp(self):
        """Initial"""
        self.convert = Token()
        self.validate = Restricted()

    def test_generate_token(self):
        """Validates login"""
        self.assertEqual(
            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
            'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w',
            self.convert.generate_token('admin', 'secret')
        )
        self.assertFalse(
            self.convert.generate_token('pepe', 'secret')
        )
        self.assertFalse(
            self.convert.generate_token('jose', '')
        )
        self.assertFalse(
            self.convert.generate_token("' or 1=1 --", '')
        )
        self.assertTrue(
            self.convert.generate_token('admin ', 'secret')
        )
        self.assertFalse(
            self.convert.generate_token('admin.*', 'secret')
        )

    def test_access_data(self):
        """Validates access to restricted data"""
        self.assertTrue(
            self.validate.access_data(
                'Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w')
        )
        self.assertFalse(
            self.validate.access_data(
                'Bearer:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w')
        )
        self.assertFalse(
            self.validate.access_data(
                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w')
        )
        self.assertFalse(
            self.validate.access_data(
                ':eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w')
        )
        self.assertFalse(
            self.validate.access_data(
                'Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXO')
        )
        self.assertFalse(
            self.validate.access_data(
                ' eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXO')
        )
        self.assertFalse(
            self.validate.access_data(
                ' eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXO ')
        )
        self.assertFalse(
            self.validate.access_data(
                'Bearer: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.'
                'BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXO ')
        )


if __name__ == '__main__':
    unittest.main()
