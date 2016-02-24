
import falcon
import json
import logging
from FakeYubiHSM import FakeYubiHSM


FORMAT = '%(asctime)-15s %(levelname)s %(funcName)s(%(lineno)d): %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class EncryptResource:
    """
    Resource to encrypt plaintext and return the ciphertext.
    """

    def on_post(self, req, resp):
        """
        Handle HTTP POST requests.
        Args:
            req: the request object.
            resp: the response object.
            pt: the plaintext to encrypt
        """

        body = req.stream.read()
        content = json.loads(body.decode('utf-8'))
        pt = content['plaintext']
        LOG.debug("plaintext: %s" % pt)

        ct = self.encrypt(pt)
        LOG.debug("ciphertext: %s" % ct)

        resp.body = json.dumps(dict(ciphertext=ct))

    def encrypt(self, pt):
        """
        This method will "encrypt" the provided plaintext value.
        """
        hsm = FakeYubiHSM()
        return hsm.encrypt(pt)

class DecryptResource:
    """
    Resource to decrypt ciphertext and return the plaintext.
    """

    def on_post(self, req, resp):
        """
        Handle HTTP POST requests.
        Args:
            req: the request object.
            resp: the response object.
            ct: the ciphertext to decrypt
        """

        body = req.stream.read()
        content = json.loads(body.decode('utf-8'))
        ct = content['ciphertext']
        LOG.debug("ciphertext: %s" % ct)

        pt = self.decrypt(ct)
        LOG.debug("plaintext: %s" % pt)

        resp.body = json.dumps(dict(plaintext=pt))

    def decrypt(self, ct):
        """
        This method will "decrypt" the provided plaintext value.
        """
        hsm = FakeYubiHSM()
        return hsm.encrypt(ct)


app = falcon.API()
app.add_route('/decrypt', DecryptResource())
app.add_route('/encrypt', EncryptResource())
