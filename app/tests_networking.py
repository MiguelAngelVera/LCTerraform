"""Deliverable 1 test"""
import unittest
from convert import CidrMaskConvert, IpValidate


class TestStringMethods(unittest.TestCase):
    """Tests cidr_to_mask, mask_to_cidr and ipv4_validation"""
    def setUp(self):
        """Initial"""
        self.convert = CidrMaskConvert()
        self.validate = IpValidate()

    def test_valid_cidr_to_mask(self):
        self.assertEqual('128.0.0.0', self.convert.cidr_to_mask('1'))
        self.assertEqual('255.255.255.0', self.convert.cidr_to_mask('24'))
        self.assertEqual('0.0.0.0', self.convert.cidr_to_mask('0'))
        self.assertEqual('255.255.255.255', self.convert.cidr_to_mask('32'))

    def test_valid_mask_to_cidr(self):
        self.assertEqual(0, self.convert.mask_to_cidr('0.0.0.0'))
        self.assertEqual(1, self.convert.mask_to_cidr('128.0.0.0'))
        self.assertEqual(24, self.convert.mask_to_cidr('255.255.255.0'))
        self.assertEqual(32, self.convert.mask_to_cidr('255.255.255.255'))

    def test_invalid_cidr_to_mask(self):
        self.assertFalse(self.convert.cidr_to_mask('ae'))
        self.assertFalse(self.convert.cidr_to_mask('-5'))
        self.assertFalse(self.convert.cidr_to_mask('33'))

    def test_invalid_mask_to_cidr(self):
        self.assertFalse(self.convert.mask_to_cidr('0.0.0'))
        self.assertFalse(self.convert.mask_to_cidr('255.128.255.0'))
        self.assertFalse(self.convert.mask_to_cidr('255.0.255.0'))
        self.assertFalse(self.convert.mask_to_cidr('255.-255.131.0'))

    def test_valid_ipv4(self):
        self.assertTrue(self.validate.ipv4_validation('127.0.0.1'))
        self.assertTrue(self.validate.ipv4_validation('192.255.0.0'))

    def test_invalid_ipv4(self):
        self.assertFalse(self.validate.ipv4_validation('192.168.1.2.3'))
        self.assertFalse(self.validate.ipv4_validation('a.b.c.d.0'))


if __name__ == '__main__':
    unittest.main()
