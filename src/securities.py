"""Functions for formatting securities data from Carta API."""

import pandas as pd
from typing import List, Dict, Any

# Define column names as constants
CERTIFICATE_COLUMNS = [
    "Security Label",
    "Share Class",
    "Quantity",
    "Issue Date",
    "Price Per Share",
]

OPTION_GRANT_COLUMNS = [
    "Grant Label",
    "Share Class",
    "Grant Date",
    "Expiration Date",
    "Exercise Price",
    "Total Shares",
    "Vested Shares",
    "Unvested Shares",
]

RSU_COLUMNS = [
    "Grant Label",
    "Share Class",
    "Grant Date",
    "Total Shares",
    "Vested Shares",
    "Unvested Shares",
]

RSA_COLUMNS = [
    "Grant Label",
    "Share Class",
    "Grant Date",
    "Total Shares",
    "Vested Shares",
    "Unvested Shares",
]

ALL_SECURITIES_COLUMNS = [
    "Security Type",
    "Portfolio ID",
    "Issuer ID",
    "Security Label",
    "Share Class",
    "Quantity",
    "Issue Date",
    "Price Per Share",
    "Grant Date",
    "Expiration Date",
    "Exercise Price",
    "Total Shares",
    "Vested Shares",
    "Unvested Shares",
]


def format_certificates_data(certificates: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format certificates data for display and download.

    Args:
        certificates: List of certificate objects from Carta API

    Returns:
        DataFrame with formatted certificate data
    """
    cert_data = []
    for cert in certificates:
        cert_data.append(
            {
                "Security Label": cert.get("securityLabel"),
                "Share Class": cert.get("shareClassName"),
                "Quantity": cert.get("quantity", {}).get("value"),
                "Issue Date": cert.get("issueDate", {}).get("value"),
                "Price Per Share": f"${cert.get('pricePerShare', {}).get('amount', {}).get('value', '0.00')}",
            }
        )
    return pd.DataFrame(cert_data, columns=CERTIFICATE_COLUMNS)


def format_option_grants_data(grants: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format option grants data for display and download.

    Args:
        grants: List of option grant objects from Carta API

    Returns:
        DataFrame with formatted option grant data
    """
    grant_data = []
    for grant in grants:
        grant_data.append(
            {
                "Grant Label": grant.get("grantLabel"),
                "Share Class": grant.get("shareClassName"),
                "Grant Date": grant.get("grantDate", {}).get("value"),
                "Expiration Date": grant.get("expirationDate", {}).get("value"),
                "Exercise Price": f"${grant.get('exercisePrice', {}).get('amount', {}).get('value', '0.00')}",
                "Total Shares": grant.get("totalShares", {}).get("value"),
                "Vested Shares": grant.get("vestedShares", {}).get("value"),
                "Unvested Shares": grant.get("unvestedShares", {}).get("value"),
            }
        )
    return pd.DataFrame(grant_data, columns=OPTION_GRANT_COLUMNS)


def format_rsus_data(rsus: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format RSU data for display and download.

    Args:
        rsus: List of RSU objects from Carta API

    Returns:
        DataFrame with formatted RSU data
    """
    rsu_data = []
    for rsu in rsus:
        rsu_data.append(
            {
                "Grant Label": rsu.get("grantLabel"),
                "Share Class": rsu.get("shareClassName"),
                "Grant Date": rsu.get("grantDate", {}).get("value"),
                "Total Shares": rsu.get("totalShares", {}).get("value"),
                "Vested Shares": rsu.get("vestedShares", {}).get("value"),
                "Unvested Shares": rsu.get("unvestedShares", {}).get("value"),
            }
        )
    return pd.DataFrame(rsu_data, columns=RSU_COLUMNS)


def format_rsas_data(rsas: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Format RSA data for display and download.

    Args:
        rsas: List of RSA objects from Carta API

    Returns:
        DataFrame with formatted RSA data
    """
    rsa_data = []
    for rsa in rsas:
        rsa_data.append(
            {
                "Grant Label": rsa.get("grantLabel"),
                "Share Class": rsa.get("shareClassName"),
                "Grant Date": rsa.get("grantDate", {}).get("value"),
                "Total Shares": rsa.get("totalShares", {}).get("value"),
                "Vested Shares": rsa.get("vestedShares", {}).get("value"),
                "Unvested Shares": rsa.get("unvestedShares", {}).get("value"),
            }
        )
    return pd.DataFrame(rsa_data, columns=RSA_COLUMNS)


def format_all_securities_data(
    certificates: List[Dict[str, Any]],
    option_grants: List[Dict[str, Any]],
    rsus: List[Dict[str, Any]],
    rsas: List[Dict[str, Any]],
    portfolio_id: str,
    issuer_id: str,
) -> pd.DataFrame:
    """
    Format all securities data into a single DataFrame for export.

    Args:
        certificates: List of certificate objects from Carta API
        option_grants: List of option grant objects from Carta API
        rsus: List of RSU objects from Carta API
        rsas: List of RSA objects from Carta API
        portfolio_id: ID of the portfolio
        issuer_id: ID of the issuer

    Returns:
        DataFrame with all securities data combined
    """
    all_data = []

    # Add certificates
    for cert in certificates:
        all_data.append(
            {
                "Security Type": "Certificate",
                "Portfolio ID": portfolio_id,
                "Issuer ID": issuer_id,
                "Security Label": cert.get("securityLabel"),
                "Share Class": cert.get("shareClassName"),
                "Quantity": cert.get("quantity", {}).get("value"),
                "Issue Date": cert.get("issueDate", {}).get("value"),
                "Price Per Share": cert.get("pricePerShare", {})
                .get("amount", {})
                .get("value"),
                "Grant Date": None,
                "Expiration Date": None,
                "Exercise Price": None,
                "Total Shares": cert.get("quantity", {}).get("value"),
                "Vested Shares": None,
                "Unvested Shares": None,
            }
        )

    # Add option grants
    for grant in option_grants:
        all_data.append(
            {
                "Security Type": "Option Grant",
                "Portfolio ID": portfolio_id,
                "Issuer ID": issuer_id,
                "Security Label": grant.get("grantLabel"),
                "Share Class": grant.get("shareClassName"),
                "Quantity": grant.get("totalShares", {}).get("value"),
                "Issue Date": None,
                "Price Per Share": None,
                "Grant Date": grant.get("grantDate", {}).get("value"),
                "Expiration Date": grant.get("expirationDate", {}).get("value"),
                "Exercise Price": grant.get("exercisePrice", {})
                .get("amount", {})
                .get("value"),
                "Total Shares": grant.get("totalShares", {}).get("value"),
                "Vested Shares": grant.get("vestedShares", {}).get("value"),
                "Unvested Shares": grant.get("unvestedShares", {}).get("value"),
            }
        )

    # Add RSUs
    for rsu in rsus:
        all_data.append(
            {
                "Security Type": "RSU",
                "Portfolio ID": portfolio_id,
                "Issuer ID": issuer_id,
                "Security Label": rsu.get("grantLabel"),
                "Share Class": rsu.get("shareClassName"),
                "Quantity": rsu.get("totalShares", {}).get("value"),
                "Issue Date": None,
                "Price Per Share": None,
                "Grant Date": rsu.get("grantDate", {}).get("value"),
                "Expiration Date": None,
                "Exercise Price": None,
                "Total Shares": rsu.get("totalShares", {}).get("value"),
                "Vested Shares": rsu.get("vestedShares", {}).get("value"),
                "Unvested Shares": rsu.get("unvestedShares", {}).get("value"),
            }
        )

    # Add RSAs
    for rsa in rsas:
        all_data.append(
            {
                "Security Type": "RSA",
                "Portfolio ID": portfolio_id,
                "Issuer ID": issuer_id,
                "Security Label": rsa.get("grantLabel"),
                "Share Class": rsa.get("shareClassName"),
                "Quantity": rsa.get("totalShares", {}).get("value"),
                "Issue Date": None,
                "Price Per Share": None,
                "Grant Date": rsa.get("grantDate", {}).get("value"),
                "Expiration Date": None,
                "Exercise Price": None,
                "Total Shares": rsa.get("totalShares", {}).get("value"),
                "Vested Shares": rsa.get("vestedShares", {}).get("value"),
                "Unvested Shares": rsa.get("unvestedShares", {}).get("value"),
            }
        )

    df = pd.DataFrame(all_data, columns=ALL_SECURITIES_COLUMNS)

    # Format currency columns
    for col in ["Price Per Share", "Exercise Price"]:
        df[col] = df[col].apply(lambda x: f"${x}" if pd.notnull(x) else None)

    return df
