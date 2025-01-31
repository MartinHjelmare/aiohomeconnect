"""Provide common constants for Home Connect API."""

from logging import getLogger

API_ENDPOINT = "https://api.home-connect.com"
OAUTH2_AUTHORIZE = "https://api.home-connect.com/security/oauth/authorize"
OAUTH2_TOKEN = "https://api.home-connect.com/security/oauth/token"  # noqa: S105
LOGGER = getLogger(__package__)
