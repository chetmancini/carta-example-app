import streamlit as st
from dotenv import load_dotenv
from carta import create_carta_client
from securities import (
    format_certificates_data,
    format_option_grants_data,
    format_all_securities_data,
    format_rsus_data,
    format_rsas_data,
)

# Load environment variables
load_dotenv()

# Initialize Carta client if not in session state
if "carta_client" not in st.session_state:
    st.session_state.carta_client = create_carta_client()

# Main app
st.title("Carta Portfolio Viewer")

# Debug section
with st.expander("Debug Info"):
    st.write("Session State:", dict(st.session_state))
    st.write("Query Params:", dict(st.query_params))


def show_portfolio_data():
    """Display portfolio and issuer data after successful login."""
    try:
        # Fetch and display portfolios
        portfolios = st.session_state.carta_client.list_portfolios()

        if not portfolios:
            st.warning("No portfolios found")
            return

        # Portfolio selector
        selected_portfolio = st.selectbox(
            "Select Portfolio",
            options=portfolios,
            format_func=lambda x: x.get("legalName", "Unnamed Portfolio"),
        )

        if not selected_portfolio:
            return

        portfolio_id = selected_portfolio["portfolioId"]

        # Fetch issuers for the selected portfolio
        issuers = st.session_state.carta_client.list_portfolio_issuers(portfolio_id)

        if not issuers:
            st.warning("No issuers found in this portfolio")
            return

        # Issuer selector
        selected_issuer = st.selectbox(
            "Select Issuer",
            options=issuers,
            format_func=lambda x: x.get("legalName", "Unnamed Issuer"),
        )

        if not selected_issuer:
            return

        issuer_id = selected_issuer["id"]

        # Create tabs for different security types
        certificates_tab, option_grants_tab, rsus_tab, rsas_tab = st.tabs(
            ["Certificates", "Option Grants", "RSUs", "RSAs"]
        )

        try:
            # Fetch data for the selected portfolio and issuer
            certificates = st.session_state.carta_client.get_portfolio_certificates(
                portfolio_id=portfolio_id, issuer_id=issuer_id
            )
            option_grants = st.session_state.carta_client.list_option_grants(
                portfolio_id=portfolio_id, issuer_id=issuer_id
            )
            rsus = st.session_state.carta_client.list_restricted_stock_units(
                portfolio_id=portfolio_id, issuer_id=issuer_id
            )
            rsas = st.session_state.carta_client.list_restricted_stock_awards(
                portfolio_id=portfolio_id, issuer_id=issuer_id
            )

            # Display certificates in the first tab
            with certificates_tab:
                st.subheader("Certificates")
                if certificates:
                    df_certificates = format_certificates_data(certificates)
                    st.dataframe(df_certificates)
                else:
                    st.warning("No certificates found for this portfolio and issuer.")

            # Display option grants in the second tab
            with option_grants_tab:
                st.subheader("Option Grants")
                if option_grants:
                    df_option_grants = format_option_grants_data(option_grants)
                    st.dataframe(df_option_grants)
                else:
                    st.warning("No option grants found for this portfolio and issuer.")

            # Display RSUs in the third tab
            with rsus_tab:
                st.subheader("Restricted Stock Units")
                if rsus:
                    df_rsus = format_rsus_data(rsus)
                    st.dataframe(df_rsus)
                else:
                    st.warning("No RSUs found for this portfolio and issuer.")

            # Display RSAs in the fourth tab
            with rsas_tab:
                st.subheader("Restricted Stock Awards")
                if rsas:
                    df_rsas = format_rsas_data(rsas)
                    st.dataframe(df_rsas)
                else:
                    st.warning("No RSAs found for this portfolio and issuer.")

            # Add export button for all securities
            st.divider()
            st.subheader("Export All Securities")
            df_all = format_all_securities_data(
                certificates=certificates,
                option_grants=option_grants,
                rsus=rsus,
                rsas=rsas,
                portfolio_id=portfolio_id,
                issuer_id=issuer_id,
            )

            if not df_all.empty:
                csv = df_all.to_csv(index=False)
                st.download_button(
                    label="Download All Securities as CSV",
                    data=csv,
                    file_name=f"securities_{portfolio_id}_{issuer_id}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No securities found for this portfolio and issuer.")

        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            # Clear access token on error
            st.session_state.carta_client.access_token = None

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        # Clear access token on error
        st.session_state.carta_client.access_token = None


# Handle OAuth callback
if "code" in st.query_params:
    try:
        code = st.query_params["code"]
        state = st.query_params.get("state")

        st.write("Debug - Processing OAuth callback:")
        st.write(f"Code: {code}")
        st.write(f"State: {state}")

        # Exchange code for token
        token_data = st.session_state.carta_client.exchange_code_for_token(code, state)
        st.session_state.carta_client.access_token = token_data.get("access_token")

        # Clear query parameters and reload
        st.query_params.clear()
        st.rerun()

    except Exception as e:
        st.error(f"Error during authentication: {str(e)}")

# Show login or portfolio data
if not st.session_state.carta_client.access_token:
    st.write("Please log in to view your Carta portfolio data")
    auth_data = st.session_state.carta_client.get_auth_data()

    # Create login button
    st.markdown(
        f"""
        <a href="{auth_data['auth_url']}" target="_self">
            <button style="
                background-color: #FF4B4B;
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 0.5rem;
                cursor: pointer;
                font-size: 1rem;
                font-weight: bold;
            ">
                Login with Carta
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
else:
    show_portfolio_data()
