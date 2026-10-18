import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from huggingface_hub import hf_hub_download


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Demand & Inventory Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# WAREHOUSE AI — PROFESSIONAL THEME
# ==========================================

st.markdown("""
<style>

/* =========================================
   GLOBAL
========================================= */

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(37, 99, 235, 0.10),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #020617 0%,
            #06152E 45%,
            #081B38 100%
        );

    color: #F8FAFC;
}


/* Main content spacing */

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

header[data-testid="stHeader"] * {
    visibility: hidden;
}


/* =========================================
   HEADER
========================================= */

.main-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #F8FAFC;
    margin-bottom: 2px;
}

.main-title span {
    color: #38BDF8;
}

.subtitle {
    font-size: 15px;
    color: #94A3B8;
    margin-bottom: 28px;
    letter-spacing: 0.2px;
}


/* =========================================
   SECTION TITLES
========================================= */

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 28px;
    margin-bottom: 14px;
}

.section-description {
    font-size: 13px;
    color: #94A3B8;
    margin-top: -8px;
    margin-bottom: 15px;
}


/* =========================================
   KPI CARDS
========================================= */

.kpi-card {
    position: relative;

    background:
        linear-gradient(
            145deg,
            rgba(15, 38, 72, 0.96),
            rgba(7, 24, 49, 0.96)
        );

    padding: 20px;

    min-height: 118px;

    border-radius: 16px;

    border: 1px solid rgba(56, 189, 248, 0.18);

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.03);

    transition: all 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);

    border-color:
        rgba(56, 189, 248, 0.45);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.35),
        0 0 20px rgba(14, 165, 233, 0.08);
}

.kpi-label {
    font-size: 12px;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 8px;
}


/* =========================================
   SELECTED SKU CARD
========================================= */

.sku-card {
    background:
        linear-gradient(
            145deg,
            rgba(14, 40, 76, 0.98),
            rgba(6, 25, 51, 0.98)
        );

    border: 1px solid rgba(59, 130, 246, 0.30);

    border-radius: 18px;

    padding: 24px;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.25);
}

.sku-title {
    font-size: 20px;
    font-weight: 750;
    color: #F8FAFC;
}

.sku-subtitle {
    font-size: 13px;
    color: #94A3B8;
}


/* =========================================
   ANALYSIS / EXPANDER CARDS
========================================= */

div[data-testid="stExpander"] {
    background:
        linear-gradient(
            145deg,
            rgba(12, 35, 68, 0.96),
            rgba(5, 23, 48, 0.96)
        );

    border: 1px solid rgba(56, 189, 248, 0.18);

    border-radius: 16px;

    margin-bottom: 14px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.22);
}

div[data-testid="stExpander"]:hover {
    border-color:
        rgba(56, 189, 248, 0.40);
}

div[data-testid="stExpander"] summary p {
    color: #F8FAFC !important;
    font-size: 16px;
    font-weight: 700;
}


/* =========================================
   SIDEBAR
========================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #020B1C 0%,
            #06152E 55%,
            #071B37 100%
        );

    border-right:
        1px solid rgba(56, 189, 248, 0.14);
}


/* Sidebar text */

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
    color: #E2E8F0 !important;
}


/* Sidebar selectbox */

section[data-testid="stSidebar"]
[data-baseweb="select"] {
    background-color: #0F2748 !important;

    border:
        1px solid rgba(56, 189, 248, 0.25) !important;

    border-radius: 10px !important;
}


/* Selected value */

section[data-testid="stSidebar"]
[data-baseweb="select"] * {
    color: #F8FAFC !important;
}


/* =========================================
   STREAMLIT METRICS
========================================= */

[data-testid="stMetric"] {
    background:
        rgba(8, 30, 59, 0.80);

    border:
        1px solid rgba(56, 189, 248, 0.16);

    padding: 15px;

    border-radius: 13px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}


/* =========================================
   DATAFRAME
========================================= */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;

    border:
        1px solid rgba(56, 189, 248, 0.15);
}


/* =========================================
   BUTTONS
========================================= */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #2563EB,
            #0EA5E9
        );

    color: white;

    border: none;

    border-radius: 10px;

    font-weight: 650;

    padding: 8px 18px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(14, 165, 233, 0.25);
}


/* =========================================
   INFO / WARNING BOXES
========================================= */

div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* =========================================
   SCROLLBAR
========================================= */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #020617;
}

::-webkit-scrollbar-thumb {
    background: #1E40AF;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #2563EB;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="main-title">
        📦Demand &Inventory  <span> Analytics</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Demand & Inventory Intelligence
        &nbsp; • &nbsp;
        AI-powered forecasting
        &nbsp; • &nbsp;
        Inventory optimization
        &nbsp; • &nbsp;
        Stockout prevention
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# LOAD DATA FROM HUGGING FACE
# ==========================================

HF_REPO_ID = "sandhusandy/warehouse-ai-data"


@st.cache_data
def load_csv_from_huggingface(filename):

    file_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=filename,
        repo_type="dataset",
        token=st.secrets["HF_TOKEN"]
    )

    return pd.read_csv(file_path)


recommendations = load_csv_from_huggingface(
    "final_inventory_recommendations.csv"
)

stockout = load_csv_from_huggingface(
    "stockout_analysis.csv"
)

# ==========================================
# LOAD HISTORICAL SALES DATA FROM HUGGING FACE
# ==========================================

@st.cache_data
def load_sales_data():

    file_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename="processed_retail_sales.csv",
        repo_type="dataset",
        token=st.secrets["HF_TOKEN"]
    )

    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"])

    return df


# ==========================================
# LOAD LIGHTGBM MODEL
# ==========================================

@st.cache_resource
def load_model():

    return joblib.load(
        "models/lightgbm_model.pkl"
    )

sales_data = load_sales_data()

model = load_model()

# Convert numeric columns
numeric_columns = [
    "average_demand",
    "demand_std",
    "lead_time_demand",
    "safety_stock",
    "reorder_point",
    "stockout_days",
    "total_shortage",
    "total_demand",
    "stockout_rate",
    "recommended_safety_stock",
    "recommended_reorder_point",
    "recommended_order_quantity"
]

for column in numeric_columns:

    if column in recommendations.columns:

        recommendations[column] = pd.to_numeric(
            recommendations[column],
            errors="coerce"
        )

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_skus = len(recommendations)

critical_skus = (
    recommendations["priority"]
    .eq("Critical")
    .sum()
)

total_shortage = (
    recommendations["total_shortage"]
    .sum()
)

average_stockout_rate = (
    recommendations["stockout_rate"]
    .mean()
)

total_recommended_order = (
    recommendations["recommended_order_quantity"]
    .sum()
)

# ==========================================
# WAREHOUSE OVERVIEW
# ==========================================

st.markdown(
    '<div class="section-title">📊 Warehouse Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Key inventory health indicators across all warehouses and SKUs'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total SKUs</div>
            <div class="kpi-value">{total_skus:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Critical SKUs</div>
            <div class="kpi-value">{critical_skus:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Shortage</div>
            <div class="kpi-value">{total_shortage:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Stockout Rate</div>
            <div class="kpi-value">{average_stockout_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Recommended Order</div>
            <div class="kpi-value">{total_recommended_order:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# INVENTORY HEALTH
# ==========================================

col_health, col_stockout = st.columns(2)


with col_health:

    st.markdown(
        '<div class="section-title">🚦 Inventory Health</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Distribution of SKUs by inventory priority'
        '</div>',
        unsafe_allow_html=True
    )

    priority_counts = (
        recommendations["priority"]
        .value_counts()
        .reset_index()
    )

    priority_counts.columns = [
        "priority",
        "count"
    ]

    fig_priority = px.bar(
        priority_counts,
        x="priority",
        y="count",
        color="priority",
        text="count"
    )

    fig_priority.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title="Number of SKUs",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#CBD5E1"
        ),
        showlegend=False,
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10
        ),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,0.10)"
        )
    )

    fig_priority.update_traces(
        textposition="outside",
        textfont=dict(
            color="#E2E8F0"
        )
    )

    st.plotly_chart(
        fig_priority,
         width="stretch"
    )

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Dashboard Filters")

store_list = sorted(
    recommendations["store_id"].unique()
)

selected_store = st.sidebar.selectbox(
    "Select Store",
    store_list
)

filtered = recommendations[
    recommendations["store_id"] == selected_store
]

item_list = sorted(
    filtered["item_id"].unique()
)

selected_item = st.sidebar.selectbox(
    "Select Item",
    item_list
)

# ==========================================
# INTERACTIVE STOCKOUT ANALYSIS
# ==========================================

# ==========================================
# STOCKOUT RISK
# ==========================================

with col_stockout:

    st.markdown(
        '<div class="section-title">⚠️ Stockout Risk</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="section-description">'
        f'Top 10 stockout-risk SKUs for {selected_store}'
        f'</div>',
        unsafe_allow_html=True
    )

    # Filter stockout data by selected store
    store_stockouts = recommendations[
        recommendations["store_id"] == selected_store
    ].copy()

    # Sort by stockout rate
    top_stockouts = (
        store_stockouts
        .sort_values(
            "stockout_rate",
            ascending=False
        )
        .head(10)
    )

    fig_stockout = px.bar(
        top_stockouts,
        x="item_id",
        y="stockout_rate",
        text="stockout_rate"
    )

    fig_stockout.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#CBD5E1"
        ),
        xaxis=dict(
            title="Item",
            color="#94A3B8",
            gridcolor="rgba(148,163,184,0.08)"
        ),
        yaxis=dict(
            title="Stockout Rate (%)",
            color="#94A3B8",
            gridcolor="rgba(148,163,184,0.10)"
        ),
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=15,
            b=20
        )
    )

    fig_stockout.update_traces(
        marker_color="#0BBEF5",
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig_stockout,
       width ='stretch'
    )


    # ==========================================
# SELECT SKU
# ==========================================
st.markdown(
    '<div class="section-title">📦 Selected Inventory</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Inventory details and risk profile for the selected store and item'
    '</div>',
    unsafe_allow_html=True
)

sku = filtered[
    filtered["item_id"] == selected_item
].iloc[0]

# # ==========================================
# SELECTED SKU OVERVIEW
# ==========================================

st.markdown(
    f"""<div class="sku-card">
<div class="sku-title">{selected_store} / {selected_item}</div>
<div class="sku-subtitle">Current inventory recommendation and historical risk profile</div>
</div>""",
    unsafe_allow_html=True
)


# ==========================================
# SKU METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Average Demand",
        f"{sku['average_demand']:.2f}"
    )

with col2:

    st.metric(
        "Safety Stock",
        f"{sku['recommended_safety_stock']:.0f}"
    )

with col3:

    st.metric(
        "Reorder Point",
        f"{sku['recommended_reorder_point']:.0f}"
    )

with col4:

    st.metric(
        "Recommended Order",
        f"{sku['recommended_order_quantity']:,}"
    )


# ==========================================
# STATUS ROW
# ==========================================

stockout_rate = float(
    sku["stockout_rate"]
)

priority = sku["priority"]


if stockout_rate >= 5:

    status_text = "HIGH RISK"
    status_icon = "🔴"

elif stockout_rate >= 2:

    status_text = "MODERATE RISK"
    status_icon = "🟠"

else:

    status_text = "LOW RISK"
    status_icon = "🟢"


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Historical Stockout Rate",
        f"{stockout_rate:.2f}%"
    )

with col2:

    st.metric(
        "Inventory Priority",
        priority
    )

with col3:

    st.metric(
        "Inventory Status",
        f"{status_icon} {status_text}"
    )

