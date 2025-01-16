import os
import secrets
import requests
import streamlit as st
from urllib.parse import urlencode
from typing import Dict, Optional, List
from requests.auth import HTTPBasicAuth


class CartaAPI:
    AUTH_URL = "https://login.playground.carta.team/o/authorize"
    TOKEN_URL = "https://login.playground.carta.team/o/access_token/"
    API_BASE_URL = "https://api.playground.carta.team"
    SCOPES = ["read_portfolio_securities", "read_portfolio_info"]

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._access_token: Optional[str] = None

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @access_token.setter
    def access_token(self, token: str):
        self._access_token = token

    def get_auth_data(self) -> dict[str, str]:
        """Generate the OAuth authorization URL with PKCE."""
        state = secrets.token_urlsafe(4)
        st.write("Debug - Generating Auth URL:")
        st.write(f"Generated State: {state}")

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": " ".join(self.SCOPES),
            "redirect_uri": self.redirect_uri,
            "state": state,
        }
        return {
            "auth_url": f"{self.AUTH_URL}?{urlencode(params)}",
            "state": state,
        }

    def exchange_code_for_token(self, code: str, state: Optional[str] = None) -> Dict:
        """Exchange authorization code for access token."""
        st.write("Debug - Token Exchange:")
        st.write("Received State:", state)
        auth: HTTPBasicAuth = HTTPBasicAuth(self.client_id, self.client_secret)

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }

        st.write("Debug - Token Exchange Request:")
        st.write("URL:", self.TOKEN_URL)
        st.write(
            "Data:", {k: v if k != "client_secret" else "***" for k, v in data.items()}
        )

        response = requests.post(self.TOKEN_URL, data=data, auth=auth)
        if not response.ok:
            st.error(f"Token exchange failed: {response.status_code}")
            st.error(f"Response: {response.text}")
        response.raise_for_status()
        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        """Get common headers for API requests."""
        if not self._access_token:
            raise ValueError("Access token not set. Please authenticate first.")

        return {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }

    def list_portfolio_issuers(
        self, portfolio_id: str, page_size: int = 50
    ) -> List[Dict]:
        """
        Fetch all issuers in a portfolio with pagination support.

        Args:
            portfolio_id: The ID of the portfolio
            page_size: Number of items per page (default: 50)

        Returns:
            List of all issuers across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """
        all_issuers = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios/{portfolio_id}/issuers",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "issuers" in data:
                all_issuers.extend(data["issuers"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_issuers

    def get_portfolio_certificates(
        self, portfolio_id: str, issuer_id: str, page_size: int = 50
    ) -> List[Dict]:
        """
        Fetch all certificates for a portfolio issuer with pagination support.

        Args:
            portfolio_id: The ID of the portfolio
            issuer_id: The ID of the issuer
            page_size: Number of items per page (default: 50)

        Returns:
            List of all certificates across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """
        all_certificates = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios/{portfolio_id}/issuers/{issuer_id}/certificates",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "certificates" in data:
                all_certificates.extend(data["certificates"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_certificates

    def list_portfolios(self, page_size: int = 50) -> List[Dict]:
        """
        Fetch all shareholder portfolios with pagination support.

        Args:
            page_size: Number of items per page (default: 50)

        Returns:
            List of portfolio objects across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """
        all_portfolios = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "portfolios" in data:
                all_portfolios.extend(data["portfolios"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_portfolios

    def list_option_grants(
        self, portfolio_id: str, issuer_id: str, page_size: int = 50
    ) -> List[Dict]:
        """
        Fetch all option grants for a portfolio issuer with pagination support.

        Args:
            portfolio_id: The ID of the portfolio
            issuer_id: The ID of the issuer
            page_size: Number of items per page (default: 50)

        Returns:
            List of all option grants across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """

        all_option_grants = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios/{portfolio_id}/issuers/{issuer_id}/optionGrants",
                headers=self._get_headers(),
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "optionGrants" in data:
                all_option_grants.extend(data["optionGrants"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_option_grants

    def list_restricted_stock_units(
        self, portfolio_id: str, issuer_id: str, page_size: int = 50
    ) -> List[Dict]:
        """
        Fetch all restricted stock units (RSUs) for a portfolio issuer with pagination support.

        Args:
            portfolio_id: The ID of the portfolio
            issuer_id: The ID of the issuer
            page_size: Number of items per page (default: 50)

        Returns:
            List of all RSUs across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """
        if not self._access_token:
            raise ValueError("Access token not set. Please authenticate first.")

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }

        all_rsus = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios/{portfolio_id}/issuers/{issuer_id}/restrictedStockUnits",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "restrictedStockUnits" in data:
                all_rsus.extend(data["restrictedStockUnits"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_rsus

    def list_restricted_stock_awards(
        self, portfolio_id: str, issuer_id: str, page_size: int = 50
    ) -> List[Dict]:
        """
        Fetch all restricted stock awards (RSAs) for a portfolio issuer with pagination support.

        Args:
            portfolio_id: The ID of the portfolio
            issuer_id: The ID of the issuer
            page_size: Number of items per page (default: 50)

        Returns:
            List of all RSAs across all pages

        Raises:
            ValueError: If access token is not set
            requests.exceptions.RequestException: If API request fails
        """
        if not self._access_token:
            raise ValueError("Access token not set. Please authenticate first.")

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }

        all_rsas = []
        next_page_token = None

        while True:
            # Build query parameters
            params = {"pageSize": page_size}
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make API request
            response = requests.get(
                f"{self.API_BASE_URL}/v1alpha1/portfolios/{portfolio_id}/issuers/{issuer_id}/restrictedStockAwards",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            # Add results to our collection
            if "restrictedStockAwards" in data:
                all_rsas.extend(data["restrictedStockAwards"])

            # Check if there are more pages
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break

        return all_rsas


def create_carta_client() -> CartaAPI:
    """Create a CartaAPI instance using environment variables."""
    client_id = os.getenv("CARTA_CLIENT_ID")
    client_secret = os.getenv("CARTA_CLIENT_SECRET")
    redirect_uri = os.getenv("CARTA_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError(
            "Missing required environment variables. "
            "Please set CARTA_CLIENT_ID, CARTA_CLIENT_SECRET, and CARTA_REDIRECT_URI"
        )

    return CartaAPI(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )
