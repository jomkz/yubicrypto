#!/usr/bin/env python2.7

import os
import base64
from Crypto.Cipher import AES
import yubico


class FakeYubiHSM(object):
    # the block size for the cipher object; must be 16 per FIPS-197
    BLOCK_SIZE = 16
    PADDING = b'\x00'

    def __init__(self):
        self._yubikey = yubico.find_yubikey(debug=False)

    def _pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * self.PADDING

    def _get_key(self, salt=None):
        if salt is None:
            salt = os.urandom(self.BLOCK_SIZE)
        elif len(salt) != self.BLOCK_SIZE:
            raise ValueError('Salt must be exactly %d bytes in length' % self.BLOCK_SIZE)

        key = self._pad(self._yubikey.challenge_response(salt, slot=2))[:self.BLOCK_SIZE]

        return salt, key

    def encrypt(self, s):
        salt, key = self._get_key()

        cipher = AES.new(key)
        encoded_data = base64.b64encode(cipher.encrypt(self._pad(s)))
        encoded_salt = base64.b64encode(salt)

        return '%s%s' % (encoded_salt, encoded_data)

    def decrypt(self, s):
        try:
            encoded_salt = s[:24]
            encoded_data = s[24:]
            salt = base64.b64decode(encoded_salt)

            salt, key = self._get_key(salt)

            cipher = AES.new(key)
            decoded_data = cipher.decrypt(base64.b64decode(encoded_data)).rstrip(self.PADDING)

            return decoded_data
        except:
            raise ValueError('Not a valid encrypted string')
