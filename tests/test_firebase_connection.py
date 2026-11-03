import tempfile
import unittest
from unittest.mock import patch
from firebase_connection import SignInHandoff, load_firebase_config


class FirebaseHandoffTest(unittest.TestCase):
    def test_credential_is_delivered_once_and_only_to_private_poller(self):
        handoff = SignInHandoff()
        session = handoff.start()
        self.assertNotEqual(session['state'], session['pollToken'])
        self.assertIsNone(handoff.consume(session['state'],session['pollToken'])['credential'])
        credential = {'providerId':'google.com','idToken':'test-google-id-token'}
        handoff.complete(session['state'],credential)
        with self.assertRaises(ValueError):
            handoff.consume(session['state'],'wrong-token')
        self.assertEqual(handoff.consume(session['state'],session['pollToken'])['credential'],credential)
        with self.assertRaises(ValueError):
            handoff.consume(session['state'],session['pollToken'])

    def test_expired_sessions_reject_completion(self):
        with patch('firebase_connection.time.monotonic',return_value=10):
            handoff=SignInHandoff(ttl=5)
            session=handoff.start()
        with patch('firebase_connection.time.monotonic',return_value=16):
            with self.assertRaises(ValueError):
                handoff.complete(session['state'],{'providerId':'google.com','idToken':'test'})

    def test_rejects_unexpected_credentials_and_missing_configuration(self):
        handoff=SignInHandoff()
        session=handoff.start()
        for credential in (None,{}, {'providerId':'password','idToken':'x'}, {'providerId':'google.com','idToken':'x'*20000}):
            with self.assertRaises(ValueError): handoff.complete(session['state'],credential)
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(load_firebase_config(root),{'configured':False})


if __name__ == '__main__': unittest.main()
