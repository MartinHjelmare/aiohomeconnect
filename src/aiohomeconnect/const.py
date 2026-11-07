"""Provide common constants for Home Connect API."""

from logging import getLogger

API_ENDPOINT = "https://api.home-connect.com"
OAUTH2_AUTHORIZE = "https://api.home-connect.com/security/oauth/authorize"
OAUTH2_TOKEN = "https://api.home-connect.com/security/oauth/token"  # noqa: S105

API_ENDPOINT_CHINA = "https://api.home-connect.cn"
OAUTH2_AUTHORIZE_CHINA = "https://api.home-connect.cn/security/oauth/authorize"
OAUTH2_TOKEN_CHINA = "https://api.home-connect.cn/security/oauth/token"  # noqa: S105

LOGGER = getLogger(__package__)
