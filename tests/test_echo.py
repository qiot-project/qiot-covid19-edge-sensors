"""
This is a test file for pytest
"""
import pytest
from flask import Flask, request

TESTAPP = Flask(__name__)


@pytest.fixture
def test_client():
    """ This sets testing mode """
    TESTAPP.config['TESTING'] = True


def test_string_echo():
    """ This will test the echo endpoint for a specific behavior"""
    with TESTAPP.test_request_context('/echo/1'):
        assert request.path == '/echo/1'
