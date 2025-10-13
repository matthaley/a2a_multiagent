import os
import time
import unittest
from unittest.mock import patch, MagicMock
import base64

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from auth_lib.test_config import PRIVATE_KEY
from auth_lib.validator import is_token_valid


class TestTokenValidator(unittest.TestCase):
    def setUp(self):
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY.encode(), password=None
        )
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()

        # Helper to encode numbers to base64url
        def int_to_base64url(n):
            return base64.urlsafe_b64encode(
                n.to_bytes((n.bit_length() + 7) // 8, "big")
            ).rstrip(b"=")

        self.mock_jwks = {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": "test-key",
                    "n": int_to_base64url(public_numbers.n).decode("utf-8"),
                    "e": int_to_base64url(public_numbers.e).decode("utf-8"),
                }
            ]
        }

        # This mocks the OIDC discovery document provided by the IDP.
        self.mock_oidc_config = {
            "issuer": "http://mock.idp",
            "authorization_endpoint": "http://mock.idp/auth",
            "token_endpoint": "http://mock.idp/token",
            "userinfo_endpoint": "http://mock.idp/userinfo",
            "jwks_uri": "http://mock.idp/.well-known/jwks.json",
        }

    def _generate_test_token(
        self,
        tenant_id: str | None = None,
        expires_in_seconds: int = 3600,
        issuer: str = "http://mock.idp",
    ) -> str:
        """
        Generates a JWT for testing purposes.
        """
        payload = {
            "iss": issuer,
            "sub": "test-user",
            "aud": "http://localhost:8081",
            "exp": int(time.time()) + expires_in_seconds,
            "iat": int(time.time()),
        }
        if tenant_id:
            payload["tenant_id"] = tenant_id

        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY.encode(), password=None
        )
        return jwt.encode(
            payload, private_key, algorithm="RS256", headers={"kid": "test-key"}
        )

    @patch("auth_lib.validator.requests.get")
    @patch.dict(
        os.environ,
        {"OIDC_CONFIG_URL": "http://mock.idp/.well-known/openid-configuration"},
    )
    def test_valid_token_with_tenant_id(self, mock_get):
        """Test a valid token with a matching tenant ID."""
        mock_get.return_value.json.side_effect = [
            self.mock_oidc_config,
            self.mock_jwks,
        ]
        token = self._generate_test_token(tenant_id="tenant-abc")
        is_valid, message = is_token_valid(
            token,
            required_tenant_id="tenant-abc",
        )
        self.assertTrue(is_valid, msg=message)

    @patch("auth_lib.validator.requests.get")
    @patch.dict(
        os.environ,
        {"OIDC_CONFIG_URL": "http://mock.idp/.well-known/openid-configuration"},
    )
    def test_valid_token_no_tenant_id_check(self, mock_get):
        """Test a valid token when no tenant ID check is required."""
        mock_get.return_value.json.side_effect = [
            self.mock_oidc_config,
            self.mock_jwks,
        ]
        token = self._generate_test_token(tenant_id="tenant-abc")
        is_valid, message = is_token_valid(
            token,
        )
        self.assertTrue(is_valid, msg=message)

    @patch("auth_lib.validator.requests.get")
    @patch.dict(
        os.environ,
        {"OIDC_CONFIG_URL": "http://mock.idp/.well-known/openid-configuration"},
    )
    def test_expired_token(self, mock_get):
        """Test that an expired token is rejected."""
        mock_get.return_value.json.side_effect = [
            self.mock_oidc_config,
            self.mock_jwks,
        ]
        token = self._generate_test_token(tenant_id="tenant-abc", expires_in_seconds=-1)
        is_valid, message = is_token_valid(
            token,
            required_tenant_id="tenant-abc",
        )
        self.assertFalse(is_valid)
        self.assertEqual(message, "Token has expired.")

    @patch("auth_lib.validator.requests.get")
    @patch.dict(
        os.environ,
        {"OIDC_CONFIG_URL": "http://mock.idp/.well-known/openid-configuration"},
    )
    def test_mismatched_tenant_id(self, mock_get):
        """Test that a token with a mismatched tenant ID is rejected."""
        mock_get.return_value.json.side_effect = [
            self.mock_oidc_config,
            self.mock_jwks,
        ]
        token = self._generate_test_token(tenant_id="tenant-xyz")
        is_valid, message = is_token_valid(
            token,
            required_tenant_id="tenant-abc",
        )
        self.assertFalse(is_valid)
        self.assertIn("does not match required tenant_id", message)

    @patch("auth_lib.validator.requests.get")
    @patch.dict(
        os.environ,
        {"OIDC_CONFIG_URL": "http://mock.idp/.well-known/openid-configuration"},
    )
    def test_missing_tenant_id_when_required(self, mock_get):
        """Test that a token without a tenant_id is rejected when one is required."""
        mock_get.return_value.json.side_effect = [
            self.mock_oidc_config,
            self.mock_jwks,
        ]
        token = self._generate_test_token()  # No tenant_id in token
        is_valid, message = is_token_valid(
            token,
            required_tenant_id="tenant-abc",
        )
        self.assertFalse(is_valid)
        self.assertEqual(message, "'tenant_id' claim not found in token.")


if __name__ == "__main__":
    unittest.main()
