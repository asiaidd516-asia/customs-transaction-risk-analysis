import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customs Transaction Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/naot_risk_output.csv")

# ============================================================
# HEADER
# ============================================================

st.title("📊 Customs Transaction Risk Dashboard")

st.markdown(
    """
    **An explainable data analytics dashboard for identifying potentially
    unusual customs transactions and prioritizing shipments for further review.**
    """
)

st.caption(
    "Prototype based on publicly available third-party trade data. "
    "Not an operational customs control system."
)

st.divider()

# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

total_shipments = len(df)

low_risk = (df["risk_category"] == "Low").sum()
medium_risk = (df["risk_category"] == "Medium").sum()
high_risk = (df["risk_category"] == "High").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shipments", f"{total_shipments:,}")
col2.metric("Low Risk", f"{low_risk:,}")
col3.metric("Medium Risk", f"{medium_risk:,}")
col4.metric("High Risk", f"{high_risk:,}")

st.divider()

# ============================================================
# RISK ANALYSIS
# ============================================================

st.subheader("Risk Analysis")

col1, col2 = st.columns(2)

# Risk category distribution
with col1:

    st.markdown("#### Risk Category Distribution")

    risk_distribution = (
        df["risk_category"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .fillna(0)
    )

    st.bar_chart(risk_distribution)

# Risk indicator frequency
with col2:

    st.markdown("#### Risk Indicator Frequency")

    risk_indicators = [
        "contract_deviation_flag",
        "market_outlier_flag",
        "benford_rare_digit_flag",
        "is_round_value"
    ]

    indicator_counts = (
        df[risk_indicators]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(indicator_counts)

st.divider()

# ============================================================
# HIGH-RISK PRIORITY REVIEW
# ============================================================

st.subheader("🚨 High-Risk Transactions")

st.markdown(
    """
    These transactions received the highest risk classification based on
    the combination of valuation and statistical risk indicators.
    They represent **priority candidates for further review**, not confirmed
    cases of fraud or tax evasion.
    """
)

high_risk = (
    df[df["risk_category"] == "High"]
    .sort_values("risk_score", ascending=False)
)

high_risk_columns = [
    "shipment_id",
    "commodity",
    "declared_value_usd",
    "contract_value_usd",
    "risk_score",
    "risk_reasons"
]

st.dataframe(
    high_risk[high_risk_columns],
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"{len(high_risk)} shipments are currently classified as High Risk."
)

st.divider()

# ============================================================
# TRANSACTION EXPLORER
# ============================================================

st.subheader("🔎 Transaction Explorer")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_commodity = st.selectbox(
        "Commodity",
        options=["All"] + sorted(df["commodity"].unique().tolist())
    )

with filter_col2:

    selected_risk = st.selectbox(
        "Risk Category",
        options=["All", "Low", "Medium", "High"]
    )

# Apply filters
filtered_df = df.copy()

if selected_commodity != "All":
    filtered_df = filtered_df[
        filtered_df["commodity"] == selected_commodity
    ]

if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["risk_category"] == selected_risk
    ]

st.write(f"**Showing {len(filtered_df):,} shipments**")

display_columns = [
    "shipment_id",
    "commodity",
    "declared_value_usd",
    "contract_value_usd",
    "risk_score",
    "risk_category",
    "risk_reasons"
]

st.dataframe(
    filtered_df[display_columns].sort_values(
        "risk_score",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# DOWNLOAD FILTERED RESULTS
# ============================================================

csv_data = filtered_df[display_columns].to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Transactions",
    data=csv_data,
    file_name="filtered_customs_risk_transactions.csv",
    mime="text/csv"
)

st.divider()

# ============================================================
# METHODOLOGY
# ============================================================

with st.expander("ℹ️ About the Risk Scoring Methodology"):

    st.markdown(
        """
        ### Risk Indicators

        The prototype combines four transaction-level indicators:

        - **Contract deviation:** identifies substantial differences between
          declared and contract values.
        - **Market outlier:** identifies values that are unusual relative to
          other transactions within the same commodity group.
        - **Benford rare-digit pattern:** identifies unusual first-digit
          patterns in declared values.
        - **Round-number bias:** identifies unusually round declared values.

        ### Risk Score

        The indicators are combined using the following prototype weights:

        | Indicator | Weight |
        |---|---:|
        | Contract deviation | 35 |
        | Market outlier | 30 |
        | Benford rare digit | 20 |
        | Round-number bias | 15 |

        The resulting score is used to classify transactions as Low, Medium,
        or High Risk.

        **Important:** These indicators are screening signals. They do not
        establish fraud, tax evasion, or non-compliance.
        """
    )

# ============================================================
# LIMITATIONS
# ============================================================

with st.expander("⚠️ Limitations"):

    st.markdown(
        """
        - The dataset is publicly available third-party trade data rather
          than TRA's internal TANCIS data.
        - HS-code classification and transport-route checks were excluded
          because reliable supporting information was not available.
        - The market-price analysis uses relative commodity-level comparisons.
        - The dataset does not contain transaction dates, limiting time-based
          analysis.
        - The risk weights are prototype assumptions and would require
          validation using real customs audit outcomes before operational use.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Customs Transaction Risk Analysis Prototype • "
    "Data Science & Artificial Intelligence"
)