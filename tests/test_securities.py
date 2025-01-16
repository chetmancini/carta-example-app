"""Tests for securities data formatting functions."""

import pandas as pd
import pytest
from securities import (
    format_certificates_data,
    format_option_grants_data,
    format_rsus_data,
    format_rsas_data,
    format_all_securities_data,
)


@pytest.fixture
def sample_certificate():
    """Sample certificate data fixture."""
    return {
        "securityLabel": "CERT-123",
        "shareClassName": "Common Stock",
        "quantity": {"value": 1000},
        "issueDate": {"value": "2024-01-01"},
        "pricePerShare": {"amount": {"value": "10.50"}},
    }


@pytest.fixture
def sample_option_grant():
    """Sample option grant data fixture."""
    return {
        "grantLabel": "OPT-456",
        "shareClassName": "Common Stock",
        "grantDate": {"value": "2024-01-01"},
        "expirationDate": {"value": "2034-01-01"},
        "exercisePrice": {"amount": {"value": "5.00"}},
        "totalShares": {"value": 2000},
        "vestedShares": {"value": 500},
        "unvestedShares": {"value": 1500},
    }


@pytest.fixture
def sample_rsu():
    """Sample RSU data fixture."""
    return {
        "grantLabel": "RSU-789",
        "shareClassName": "Common Stock",
        "grantDate": {"value": "2024-01-01"},
        "totalShares": {"value": 1000},
        "vestedShares": {"value": 250},
        "unvestedShares": {"value": 750},
    }


@pytest.fixture
def sample_rsa():
    """Sample RSA data fixture."""
    return {
        "grantLabel": "RSA-012",
        "shareClassName": "Common Stock",
        "grantDate": {"value": "2024-01-01"},
        "totalShares": {"value": 1000},
        "vestedShares": {"value": 250},
        "unvestedShares": {"value": 750},
    }


def test_format_certificates_data(sample_certificate):
    """Test certificate data formatting."""
    df = format_certificates_data([sample_certificate])

    assert len(df) == 1
    row = df.iloc[0]
    assert row["Security Label"] == "CERT-123"
    assert row["Share Class"] == "Common Stock"
    assert row["Quantity"] == 1000
    assert row["Issue Date"] == "2024-01-01"
    assert row["Price Per Share"] == "$10.50"


def test_format_certificates_data_empty():
    """Test certificate data formatting with empty input."""
    df = format_certificates_data([])
    assert len(df) == 0
    assert list(df.columns) == [
        "Security Label",
        "Share Class",
        "Quantity",
        "Issue Date",
        "Price Per Share",
    ]


def test_format_option_grants_data(sample_option_grant):
    """Test option grant data formatting."""
    df = format_option_grants_data([sample_option_grant])

    assert len(df) == 1
    row = df.iloc[0]
    assert row["Grant Label"] == "OPT-456"
    assert row["Share Class"] == "Common Stock"
    assert row["Grant Date"] == "2024-01-01"
    assert row["Expiration Date"] == "2034-01-01"
    assert row["Exercise Price"] == "$5.00"
    assert row["Total Shares"] == 2000
    assert row["Vested Shares"] == 500
    assert row["Unvested Shares"] == 1500


def test_format_option_grants_data_empty():
    """Test option grant data formatting with empty input."""
    df = format_option_grants_data([])
    assert len(df) == 0
    assert list(df.columns) == [
        "Grant Label",
        "Share Class",
        "Grant Date",
        "Expiration Date",
        "Exercise Price",
        "Total Shares",
        "Vested Shares",
        "Unvested Shares",
    ]


def test_format_rsus_data(sample_rsu):
    """Test RSU data formatting."""
    df = format_rsus_data([sample_rsu])

    assert len(df) == 1
    row = df.iloc[0]
    assert row["Grant Label"] == "RSU-789"
    assert row["Share Class"] == "Common Stock"
    assert row["Grant Date"] == "2024-01-01"
    assert row["Total Shares"] == 1000
    assert row["Vested Shares"] == 250
    assert row["Unvested Shares"] == 750


def test_format_rsus_data_empty():
    """Test RSU data formatting with empty input."""
    df = format_rsus_data([])
    assert len(df) == 0
    assert list(df.columns) == [
        "Grant Label",
        "Share Class",
        "Grant Date",
        "Total Shares",
        "Vested Shares",
        "Unvested Shares",
    ]


def test_format_rsas_data(sample_rsa):
    """Test RSA data formatting."""
    df = format_rsas_data([sample_rsa])

    assert len(df) == 1
    row = df.iloc[0]
    assert row["Grant Label"] == "RSA-012"
    assert row["Share Class"] == "Common Stock"
    assert row["Grant Date"] == "2024-01-01"
    assert row["Total Shares"] == 1000
    assert row["Vested Shares"] == 250
    assert row["Unvested Shares"] == 750


def test_format_rsas_data_empty():
    """Test RSA data formatting with empty input."""
    df = format_rsas_data([])
    assert len(df) == 0
    assert list(df.columns) == [
        "Grant Label",
        "Share Class",
        "Grant Date",
        "Total Shares",
        "Vested Shares",
        "Unvested Shares",
    ]


def test_format_all_securities_data(
    sample_certificate, sample_option_grant, sample_rsu, sample_rsa
):
    """Test combined securities data formatting."""
    df = format_all_securities_data(
        certificates=[sample_certificate],
        option_grants=[sample_option_grant],
        rsus=[sample_rsu],
        rsas=[sample_rsa],
        portfolio_id="PORT-123",
        issuer_id="ISS-456",
    )

    assert len(df) == 4

    # Check certificate row
    cert_row = df[df["Security Type"] == "Certificate"].iloc[0]
    assert cert_row["Portfolio ID"] == "PORT-123"
    assert cert_row["Issuer ID"] == "ISS-456"
    assert cert_row["Security Label"] == "CERT-123"
    assert cert_row["Share Class"] == "Common Stock"
    assert cert_row["Quantity"] == 1000
    assert cert_row["Issue Date"] == "2024-01-01"
    assert cert_row["Price Per Share"] == "$10.50"
    assert pd.isna(cert_row["Grant Date"])
    assert pd.isna(cert_row["Exercise Price"])
    assert pd.isna(cert_row["Vested Shares"])

    # Check option grant row
    opt_row = df[df["Security Type"] == "Option Grant"].iloc[0]
    assert opt_row["Portfolio ID"] == "PORT-123"
    assert opt_row["Issuer ID"] == "ISS-456"
    assert opt_row["Security Label"] == "OPT-456"
    assert opt_row["Share Class"] == "Common Stock"
    assert opt_row["Quantity"] == 2000
    assert pd.isna(opt_row["Issue Date"])
    assert pd.isna(opt_row["Price Per Share"])
    assert opt_row["Grant Date"] == "2024-01-01"
    assert opt_row["Exercise Price"] == "$5.00"
    assert opt_row["Vested Shares"] == 500

    # Check RSU row
    rsu_row = df[df["Security Type"] == "RSU"].iloc[0]
    assert rsu_row["Portfolio ID"] == "PORT-123"
    assert rsu_row["Issuer ID"] == "ISS-456"
    assert rsu_row["Security Label"] == "RSU-789"
    assert rsu_row["Share Class"] == "Common Stock"
    assert rsu_row["Quantity"] == 1000
    assert pd.isna(rsu_row["Issue Date"])
    assert pd.isna(rsu_row["Price Per Share"])
    assert rsu_row["Grant Date"] == "2024-01-01"
    assert pd.isna(rsu_row["Exercise Price"])
    assert rsu_row["Vested Shares"] == 250

    # Check RSA row
    rsa_row = df[df["Security Type"] == "RSA"].iloc[0]
    assert rsa_row["Portfolio ID"] == "PORT-123"
    assert rsa_row["Issuer ID"] == "ISS-456"
    assert rsa_row["Security Label"] == "RSA-012"
    assert rsa_row["Share Class"] == "Common Stock"
    assert rsa_row["Quantity"] == 1000
    assert pd.isna(rsa_row["Issue Date"])
    assert pd.isna(rsa_row["Price Per Share"])
    assert rsa_row["Grant Date"] == "2024-01-01"
    assert pd.isna(rsa_row["Exercise Price"])
    assert rsa_row["Vested Shares"] == 250


def test_format_all_securities_data_empty():
    """Test combined securities data formatting with empty inputs."""
    df = format_all_securities_data(
        certificates=[],
        option_grants=[],
        rsus=[],
        rsas=[],
        portfolio_id="PORT-123",
        issuer_id="ISS-456",
    )

    assert len(df) == 0
    assert list(df.columns) == [
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


def test_format_all_securities_data_missing_fields():
    """Test combined securities data formatting with missing fields."""
    certificate = {"securityLabel": "CERT-123"}  # Minimal data
    option_grant = {"grantLabel": "OPT-456"}  # Minimal data
    rsu = {"grantLabel": "RSU-789"}  # Minimal data
    rsa = {"grantLabel": "RSA-012"}  # Minimal data

    df = format_all_securities_data(
        certificates=[certificate],
        option_grants=[option_grant],
        rsus=[rsu],
        rsas=[rsa],
        portfolio_id="PORT-123",
        issuer_id="ISS-456",
    )

    assert len(df) == 4
    cert_row = df[df["Security Type"] == "Certificate"].iloc[0]
    opt_row = df[df["Security Type"] == "Option Grant"].iloc[0]
    rsu_row = df[df["Security Type"] == "RSU"].iloc[0]
    rsa_row = df[df["Security Type"] == "RSA"].iloc[0]

    # Check that missing fields are handled gracefully
    assert cert_row["Security Label"] == "CERT-123"
    assert pd.isna(cert_row["Share Class"])
    assert pd.isna(cert_row["Quantity"])

    assert opt_row["Security Label"] == "OPT-456"
    assert pd.isna(opt_row["Share Class"])
    assert pd.isna(opt_row["Total Shares"])

    assert rsu_row["Security Label"] == "RSU-789"
    assert pd.isna(rsu_row["Share Class"])
    assert pd.isna(rsu_row["Total Shares"])

    assert rsa_row["Security Label"] == "RSA-012"
    assert pd.isna(rsa_row["Share Class"])
    assert pd.isna(rsa_row["Total Shares"])
