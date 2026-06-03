import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Bank Retention Dashboard",
    layout="wide"
)

df = pd.read_csv("European_Bank.csv")

# ==========================
# SIDEBAR FILTERS
# ==========================

st.sidebar.header("Filters")

selected_country = st.sidebar.selectbox(
    "Geography",
    ["All"] + list(df["Geography"].unique())
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + list(df["Gender"].unique())
)

balance_threshold = st.sidebar.slider(
    "Minimum Balance",
    0,
    int(df["Balance"].max()),
    0
)

st.title("Customer Engagement & Product Utilization Analytics")

st.caption(
    "Customer Retention Strategy Dashboard | Prepared by Manav Vaje"
)

st.sidebar.markdown("---")

st.sidebar.info(
"""
European Bank

Retention Strategy Analytics

Data Analyst Internship Project
"""
)


# ==========================
# APPLY FILTERS
# ==========================

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Geography"] == selected_country
    ]

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

filtered_df = filtered_df[
    filtered_df["Balance"] >= balance_threshold
]

# ==========================
# KPI CALCULATIONS
# ==========================

total_customers = len(filtered_df)

churn_rate = (
    filtered_df["Exited"].mean()
) * 100

active_customers = (
    filtered_df["Exited"].sum()
)

avg_products = (
    filtered_df["NumOfProducts"].mean()
)

# ==========================
# KPI CARDS
# ==========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

col3.metric(
    "Active Members",
    f"{active_customers:,}"
)

col4.metric(
    "Avg Products",
    f"{avg_products:.2f}"
)
st.info(
"""
This dashboard evaluates customer retention through engagement,
product utilization, relationship strength, and financial commitment indicators.
"""
)

st.divider()

st.subheader("Engagement Retention Analysis")

# ==========================
# ACTIVE VS INACTIVE CHURN
# ==========================

active_customers_df = filtered_df[
    filtered_df["IsActiveMember"] == 1
]

inactive_customers_df = filtered_df[
    filtered_df["IsActiveMember"] == 0
]

active_churn_rate = (
    active_customers_df["Exited"].mean()
) * 100

inactive_churn_rate = (
    inactive_customers_df["Exited"].mean()
) * 100
engagement_retention_ratio = (
    inactive_churn_rate /
    active_churn_rate
) if active_churn_rate > 0 else 0

# ==========================
# ACTIVE VS INACTIVE CHURN
# ==========================

active_customers_df = filtered_df[
    filtered_df["IsActiveMember"] == 1
]

inactive_customers_df = filtered_df[
    filtered_df["IsActiveMember"] == 0
]

active_churn_rate = (
    active_customers_df["Exited"].mean()
) * 100

inactive_churn_rate = (
    inactive_customers_df["Exited"].mean()
) * 100

col1, col2 = st.columns(2)

col1.metric(
    "Active Customer Churn",
    f"{active_churn_rate:.2f}%"
)

col2.metric(
    "Inactive Customer Churn",
    f"{inactive_churn_rate:.2f}%"
)

st.metric(
    "Engagement Retention Ratio",
    f"{engagement_retention_ratio:.2f}x"
)

st.divider()

st.subheader("Product Utilization Impact Analysis")

product_churn = (
    filtered_df
    .groupby("NumOfProducts")
    .agg({
        "Exited":"mean"
    })
    .reset_index()
)

product_churn["Exited"] = (
    product_churn["Exited"] * 100
)

fig_products = px.bar(
    product_churn,
    x="NumOfProducts",
    y="Exited",
    title="Churn Rate by Number of Products",
    labels={
        "Exited":"Churn Rate (%)",
        "NumOfProducts":"Number of Products"
    }
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

single_product = filtered_df[
    filtered_df["NumOfProducts"] == 1
]

multi_product = filtered_df[
    filtered_df["NumOfProducts"] > 1
]

single_churn = (
    single_product["Exited"].mean()
) * 100

multi_churn = (
    multi_product["Exited"].mean()
) * 100

product_depth_index = (
    filtered_df["NumOfProducts"].mean()
)

col1, col2 = st.columns(2)

col1.metric(
    "Single Product Churn",
    f"{single_churn:.2f}%"
)

col2.metric(
    "Multi Product Churn",
    f"{multi_churn:.2f}%"
)

st.metric(
    "Product Depth Index",
    f"{product_depth_index:.2f}"
)

st.divider()

st.subheader("High-Value Disengaged Customer Detector")

high_balance_threshold = st.slider(
    "High Balance Threshold",
    0,
    int(filtered_df["Balance"].max()),
    100000
)

high_value_disengaged = filtered_df[
    (filtered_df["Balance"] >= high_balance_threshold)
    &
    (filtered_df["IsActiveMember"] == 0)
]

st.metric(
    "High-Value Disengaged Customers",
    len(high_value_disengaged)
)

st.dataframe(
    high_value_disengaged[
        [
            "CustomerId",
            "Geography",
            "Gender",
            "Balance",
            "NumOfProducts",
            "EstimatedSalary",
            "Exited"
        ]
    ].head(20),
    hide_index=True
)

st.subheader("Salary vs Balance Risk Analysis")

fig_salary_balance = px.scatter(
    filtered_df,
    x="EstimatedSalary",
    y="Balance",
    color="Exited",
    title="Salary vs Balance Relationship",
    hover_data=["CustomerId"]
)

st.plotly_chart(
    fig_salary_balance,
    use_container_width=True
)

st.subheader("At-Risk Premium Customers")

premium_customers = filtered_df[
    (
        filtered_df["Balance"]
        >
        filtered_df["Balance"].quantile(0.75)
    )
    &
    (
        filtered_df["IsActiveMember"] == 0
    )
]

st.metric(
    "Premium Customers at Risk",
    len(premium_customers)
)

st.dataframe(
    premium_customers[
        [
            "CustomerId",
            "Geography",
            "Balance",
            "EstimatedSalary",
            "NumOfProducts",
            "Exited"
        ]
    ].head(20),
    hide_index=True
)

st.divider()

st.subheader("Relationship Strength Assessment")

relationship_df = filtered_df.copy()

relationship_df["Relationship Strength Index"] = (
    relationship_df["NumOfProducts"] * 40
    +
    relationship_df["IsActiveMember"] * 40
    +
    relationship_df["HasCrCard"] * 20
)

avg_rsi = relationship_df[
    "Relationship Strength Index"
].mean()


card_holders = filtered_df[
    filtered_df["HasCrCard"] == 1
]

non_card_holders = filtered_df[
    filtered_df["HasCrCard"] == 0
]

card_churn = (
    card_holders["Exited"].mean()
) * 100

non_card_churn = (
    non_card_holders["Exited"].mean()
) * 100

credit_card_stickiness = (
    non_card_churn -
    card_churn
)


st.metric(
    "Relationship Strength Index",
    f"{avg_rsi:.2f}"
)

st.metric(
    "Credit Card Stickiness Score",
    f"{credit_card_stickiness:.2f}"
)

st.subheader("Sticky Customer Profiles")

sticky_customers = relationship_df[
    relationship_df[
        "Relationship Strength Index"
    ] >= 80
]

st.metric(
    "Sticky Customers",
    len(sticky_customers)
)

st.dataframe(
    sticky_customers[
        [
            "CustomerId",
            "Geography",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "Balance"
        ]
    ].head(20),
    hide_index=True
)

st.divider()
st.subheader("Key Findings")

st.markdown("""
• Active customers have significantly lower churn rates.

• Customers with multiple products demonstrate stronger loyalty.

• High-balance inactive customers represent a hidden churn risk.

• Credit card ownership contributes positively to retention.

• Relationship strength increases as product adoption increases.

• Engagement is a stronger predictor of retention than balance alone.
""")
st.subheader("Executive Insights")

st.info(
"""
• Active members exhibit significantly lower churn rates.

• Customers with multiple products demonstrate stronger retention.

• High-balance inactive customers represent a major retention risk.

• Credit card ownership improves customer stickiness.

• Relationship strength is strongly associated with customer loyalty.

• Product adoption and engagement are more predictive of retention than balance alone.
"""
)

