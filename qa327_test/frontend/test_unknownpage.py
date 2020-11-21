import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

class FrontEndUnknownPageTesting(BaseCase):
    def test_pageerror(self, *_):
        # open random page
        self.open(base_url + '/abc123doesNotExistLOL')
        self.assert_element("#message")
        self.assert_text("Error 404", "#message")