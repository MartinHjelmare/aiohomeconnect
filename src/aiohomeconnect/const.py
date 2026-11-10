"""Provide common constants for Home Connect API."""

from logging import getLogger

API_ENDPOINT = "https://api.home-connect.com"
OAUTH2_AUTHORIZE = f"{API_ENDPOINT}/security/oauth/authorize"
OAUTH2_TOKEN = f"{API_ENDPOINT}/security/oauth/token"

API_ENDPOINT_CHINA = "https://api.home-connect.cn"
OAUTH2_AUTHORIZE_CHINA = f"{API_ENDPOINT_CHINA}/security/oauth/authorize"
OAUTH2_TOKEN_CHINA = f"{API_ENDPOINT_CHINA}/security/oauth/token"

LOGGER = getLogger(__package__)
