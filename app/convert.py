"""Deliverable1"""
import re


class CidrMaskConvert:
    """Class to convert Cidr to Mask or Mask to Cidr"""
    @staticmethod
    def cidr_to_mask(cidr):
        """converts Cidr to Mask"""
        if IpValidate.cidr_validation(cidr):
            cidr = int(cidr)
            if cidr == 0:
                netmask = "0.0.0.0"
                return netmask
            full_octets = cidr // 8
            if full_octets == 4:
                netmask = "255.255.255.255"
            else:
                netmask = ["0"] * 4
                for i in range(0, full_octets):
                    netmask[i] = "255"
                next_octet = full_octets + 1
                zeros_next_octet = (8 * next_octet) - cidr
                value_next_octet = 256 - (2 ** zeros_next_octet)
                netmask[next_octet - 1] = str(value_next_octet)
                netmask = ".".join(netmask)
            return netmask
        return False

    @staticmethod
    def mask_to_cidr(netmask):
        """converts Mask to Cidr"""
        if IpValidate.ipv4_validation(netmask):
            cidr = 0
            octets = netmask.split('.')
            mask_validation = True
            for index in range(0, 3):
                cidr += bin(int(octets[index])).count('1')
                if octets[index] != "255" and octets[index+1] != "0":
                    mask_validation = False
                    break
            if mask_validation:
                cidr += bin(int(octets[3])).count('1')
                return int(cidr)
        return False


class IpValidate:
    """Validation of ip address format and cidr"""
    @staticmethod
    def ipv4_validation(ip_address):
        """validates ip address"""
        octets = ip_address.split(".")
        count = len(octets)
        if count != 4:
            return False
        for i in range(0, count-1):
            if octets[i].isnumeric() and 0 <= int(octets[i]) <= 255:
                return True
        return False

    @staticmethod
    def cidr_validation(cidr):
        """validates cidr"""
        if not re.search("[^0-9]", cidr):
            if 0 <= int(cidr) <= 32:
                return True
        return False
