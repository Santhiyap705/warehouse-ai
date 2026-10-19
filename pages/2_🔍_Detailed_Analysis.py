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
# PROFESSIONAL THEME
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
   ANALYSIS TILES
========================================= */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #0F2E55,
            #0A2343
        );

    color: #F8FAFC;

    border: 1px solid rgba(56, 189, 248, 0.20);

    border-radius: 16px;

    font-weight: 700;

    min-height: 95px;

    padding: 18px;

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);

    border-color:
        rgba(56, 189, 248, 0.55);

    background:
        linear-gradient(
            135deg,
            #123968,
            #0B294D
        );

    box-shadow:
        0 10px 25px rgba(14, 165, 233, 0.16);
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
   RECOMMENDATION CARD
========================================= */

.recommendation-card {
    background:
        linear-gradient(
            135deg,
            rgba(14, 40, 76, 0.98),
            rgba(6, 25, 51, 0.98)
        );

    border: 1px solid rgba(56, 189, 248, 0.25);

    border-radius: 16px;

    padding: 22px;

    margin-top: 18px;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.20);
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

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
    color: #E2E8F0 !important;
}

section[data-testid="stSidebar"]
[data-baseweb="select"] {
    background-color: #0F2748 !important;

    border:
        1px solid rgba(56, 189, 248, 0.25) !important;

    border-radius: 10px !important;
}

section[data-testid="stSidebar"]
[data-baseweb="select"] * {
    color: #F8FAFC !important;
}


/* =========================================
   ALERTS
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
        📦 Demand & Inventory <span>Analytics</span>
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


# LOAD HISTORICAL SALES DATA
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


sales_data = None
model = None

if st.session_state.get("analysis_section") == "demand":
    sales_data = load_sales_data()
    model = load_model()


# ==========================================
# CONVERT NUMERIC COLUMNS
# ==========================================

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
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header(
    "🔎 Dashboard Filters"
)

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
# SELECTED SKU
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


# ==========================================
# SELECTED SKU OVERVIEW
# ==========================================

st.markdown( f"""<div class="sku-card"> <div class="sku-title">{selected_store} / {selected_item}
</div> <div class="sku-subtitle">Current inventory recommendation and historical risk profile</div>
 </div>""", unsafe_allow_html=True )


# ==========================================
# ANALYSIS TILE NAVIGATION
# ==========================================

st.markdown(
    '<div class="section-title">🔍 Explore Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select an analysis area to explore detailed insights'
    '</div>',
    unsafe_allow_html=True
)


if "analysis_section" not in st.session_state:
    st.session_state["analysis_section"] = None


# ==========================================
# FOUR ANALYSIS TILES
# ==========================================

tile1, tile2, tile3, tile4 = st.columns(4)


with tile1:

    if st.button(
        "📈\nDemand Intelligence",
        width='stretch',
        key="tile_demand"
    ):

        st.session_state["analysis_section"] = "demand"


with tile2:

    if st.button(
        "⚠️\nStockout Analysis",
        use_container_width=True,
        key="tile_stockout"
    ):

        st.session_state["analysis_section"] = "stockout"


with tile3:

    if st.button(
        "📦\nInventory Analysis",
        use_container_width=True,
        key="tile_inventory"
    ):

        st.session_state["analysis_section"] = "inventory"


with tile4:

    if st.button(
        "🤖\nAI Recommendation",
        use_container_width=True,
        key="tile_ai"
    ):

        st.session_state["analysis_section"] = "ai"


# ==========================================
# PREPARE FORECAST DATA
# ==========================================

sku_sales = pd.DataFrame()

if (
    st.session_state.get("analysis_section") == "demand"
    and sales_data is not None
):
    sku_sales = sales_data[
        (sales_data["store_id"] == selected_store) &
        (sales_data["item_id"] == selected_item)
    ].copy()

    sku_sales = sku_sales.sort_values(
        "date"
    ).reset_index(drop=True)


forecast_available = False

forecast_df = pd.DataFrame()

total_forecast = 0

average_forecast = 0

peak_forecast = 0

# ==========================================
# CREATE 30-DAY FORECAST
# ==========================================

if len(sku_sales) >= 30:

    demand_history = (
        sku_sales["sales"]
        .astype(float)
        .tolist()
    )

    last_price = float(
        sku_sales["price"].iloc[-1]
    )

    forecast_dates = []

    forecast_values = []

    last_date = sku_sales["date"].iloc[-1]


    for i in range(1, 31):

        future_date = (
            last_date +
            pd.Timedelta(days=i)
        )

        lag_1 = demand_history[-1]

        lag_7 = demand_history[-7]

        lag_30 = demand_history[-30]

        rolling_mean_7 = (
            sum(demand_history[-7:]) / 7
        )

        rolling_mean_30 = (
            sum(demand_history[-30:]) / 30
        )

        day_of_week = future_date.dayofweek

        month = future_date.month

        is_weekend = int(
            day_of_week >= 5
        )

        promo = 0


        features = pd.DataFrame([{
            "lag_1": lag_1,
            "lag_7": lag_7,
            "lag_30": lag_30,
            "rolling_mean_7": rolling_mean_7,
            "rolling_mean_30": rolling_mean_30,
            "price": last_price,
            "promo": promo,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend
        }])


        prediction = model.predict(
            features
        )[0]

        prediction = max(
            0,
            prediction
        )


        forecast_dates.append(
            future_date
        )

        forecast_values.append(
            prediction
        )


        demand_history.append(
            prediction
        )


    forecast_df = pd.DataFrame({
        "date": forecast_dates,
        "forecast_demand": forecast_values
    })


    total_forecast = (
        forecast_df["forecast_demand"].sum()
    )

    average_forecast = (
        forecast_df["forecast_demand"].mean()
    )

    peak_forecast = (
        forecast_df["forecast_demand"].max()
    )

    forecast_available = True


# ==========================================
# DEMAND INTELLIGENCE
# ==========================================

if st.session_state["analysis_section"] == "demand":

    st.markdown(
        '<div class="section-title">'
        '📈 Demand Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'AI-powered demand forecast based on historical SKU patterns'
        '</div>',
        unsafe_allow_html=True
    )


    if not forecast_available:

        st.warning(
            "Not enough historical data available for this SKU."
        )

    else:

        recent_history = sku_sales[
            ["date", "sales"]
        ].tail(60).copy()

        recent_history["type"] = "Historical"

        recent_history = recent_history.rename(
            columns={
                "sales": "demand"
            }
        )


        forecast_plot = forecast_df.copy()

        forecast_plot["type"] = "Forecast"

        forecast_plot = forecast_plot.rename(
            columns={
                "forecast_demand": "demand"
            }
        )


        chart_data = pd.concat(
            [
                recent_history[
                    ["date", "demand", "type"]
                ],
                forecast_plot[
                    ["date", "demand", "type"]
                ]
            ],
            ignore_index=True
        )


        fig_forecast = px.line(
            chart_data,
            x="date",
            y="demand",
            color="type",
            markers=True,
            title=(
                "Historical vs Forecast Demand - "
                f"{selected_store} / {selected_item}"
            )
        )


        fig_forecast.update_layout(

            plot_bgcolor="rgba(0,0,0,0)",

            paper_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#CBD5E1"
            ),

            title=dict(
                font=dict(
                    size=18,
                    color="#F8FAFC"
                ),
                x=0.01,
                xanchor="left"
            ),

            xaxis=dict(
                title="Date",
                color="#94A3B8",
                gridcolor="rgba(148,163,184,0.10)",
                linecolor="rgba(148,163,184,0.20)"
            ),

            yaxis=dict(
                title="Demand",
                color="#94A3B8",
                gridcolor="rgba(148,163,184,0.10)",
                linecolor="rgba(148,163,184,0.20)"
            ),

            legend=dict(
                font=dict(
                    color="#CBD5E1"
                ),
                bgcolor="rgba(0,0,0,0)"
            ),

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )


        fig_forecast.for_each_trace(
            lambda trace: trace.update(
                line=dict(
                    color=(
                        "#38BDF8"
                        if trace.name == "Forecast"
                        else "#2563EB"
                    ),
                    width=3
                )
            )
        )


        st.plotly_chart(
            fig_forecast,
            width="content"
        )


        # ==================================
        # FORECAST SUMMARY
        # ==================================

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "30-Day Forecast Demand",
            f"{total_forecast:,.0f}"
        )


        col2.metric(
            "Average Daily Forecast",
            f"{average_forecast:,.2f}"
        )


        col3.metric(
            "Peak Daily Forecast",
            f"{peak_forecast:,.2f}"
        )


# ==========================================
# STOCKOUT ANALYSIS
# ==========================================

elif st.session_state["analysis_section"] == "stockout":

    st.markdown(
        '<div class="section-title">'
        '⚠️ Stockout Risk Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'High-risk SKUs and historical shortage analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # ======================================
    # SELECTED SKU STOCKOUT METRICS
    # ======================================

    selected_stockout_rate = float(
        sku["stockout_rate"]
    )

    selected_stockout_days = int(
        sku["stockout_days"]
    )

    selected_shortage = float(
        sku["total_shortage"]
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Stockout Rate",
        f"{selected_stockout_rate:.2f}%"
    )

    col2.metric(
        "Stockout Days",
        f"{selected_stockout_days:,}"
    )

    col3.metric(
        "Total Shortage",
        f"{selected_shortage:,.0f}"
    )


    # ======================================
    # TOP STOCKOUT SKUS
    # ======================================

    st.markdown(
        "### ⚠️ Highest-Risk SKUs"
    )

    st.caption(
        f"Highest stockout-risk SKUs for {selected_store}"
    )


    store_stockouts = recommendations[
        recommendations["store_id"] == selected_store
    ].copy()


    top_stockouts = (
        store_stockouts
        .sort_values(
            "stockout_rate",
            ascending=False
        )
        .head(10)
    )


    # ======================================
    # STYLED STOCKOUT TABLE
    # ======================================

    display_df = top_stockouts[
        [
            "store_id",
            "item_id",
            "stockout_rate",
            "stockout_days",
            "total_shortage",
            "priority"
        ]
    ].copy()


    # Format stockout rate

    display_df["stockout_rate"] = (
        display_df["stockout_rate"]
        .map(lambda x: f"{x:.2f}%")
    )


    # ======================================
    # PRIORITY COLORS
    # ======================================

    def highlight_priority(value):

        if value == "Critical":
            return "color: #EF4444; font-weight: 700;"

        elif value == "High":
            return "color: #F59E0B; font-weight: 700;"

        elif value == "Medium":
            return "color: #38BDF8; font-weight: 600;"

        else:
            return "color: #22C55E; font-weight: 600;"


    styled_df = (
        display_df.style
        .set_properties(
            **{
                "background-color": "#0B1F3A",
                "color": "#E2E8F0",
                "border-color": "#1E3A5F"
            }
        )
        .map(
            highlight_priority,
            subset=["priority"]
        )
    )


    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# INVENTORY ANALYSIS
# ==========================================

elif st.session_state["analysis_section"] == "inventory":

    st.markdown(
        '<div class="section-title">'
        '📦 Inventory Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Safety stock, reorder point, order quantity and inventory coverage'
        '</div>',
        unsafe_allow_html=True
    )


    # ======================================
    # INVENTORY VALUES
    # ======================================

    recommended_safety_stock = float(
        sku["recommended_safety_stock"]
    )

    recommended_reorder_point = float(
        sku["recommended_reorder_point"]
    )

    recommended_order_quantity = int(
        sku["recommended_order_quantity"]
    )

    stockout_rate = float(
        sku["stockout_rate"]
    )

    priority = sku["priority"]


    # ======================================
    # INVENTORY METRICS
    # ======================================

    col1, col2, col3, col4 = st.columns(4)


    if forecast_available:

        col1.metric(
            "30-Day Forecast",
            f"{total_forecast:,.0f}"
        )

    else:

        col1.metric(
            "30-Day Forecast",
            "N/A"
        )


    col2.metric(
        "Safety Stock",
        f"{recommended_safety_stock:,.0f}"
    )

    col3.metric(
        "Reorder Point",
        f"{recommended_reorder_point:,.0f}"
    )

    col4.metric(
        "Order Quantity",
        f"{recommended_order_quantity:,}"
    )


    # ======================================
    # INVENTORY COVERAGE
    # ======================================

    st.markdown(
        "### 📊 Inventory Coverage"
    )


    if forecast_available:

        daily_demand = average_forecast

    else:

        daily_demand = float(
            sku["average_demand"]
        )


    if daily_demand > 0:

        coverage_days = (
            recommended_order_quantity /
            daily_demand
        )

    else:

        coverage_days = 0


    # ======================================
    # INVENTORY STATUS
    # ======================================

    if stockout_rate >= 5:

        inventory_status = (
            "🔴 High Stockout Risk"
        )

    elif stockout_rate >= 2:

        inventory_status = (
            "🟠 Moderate Stockout Risk"
        )

    else:

        inventory_status = (
            "🟢 Low Stockout Risk"
        )


    col1, col2 = st.columns(2)


    col1.metric(
        "Order Quantity Coverage",
        f"{coverage_days:.1f} days"
    )

    col2.metric(
        "Inventory Status",
        inventory_status
    )


    st.caption(
        f"The recommended order quantity of "
        f"{recommended_order_quantity:,} units can cover "
        f"approximately {coverage_days:.1f} days "
        f"of forecast demand."
    )


# ==========================================
# AI RECOMMENDATION
# ==========================================

elif st.session_state["analysis_section"] == "ai":

    st.markdown(
        '<div class="section-title">'
        '🤖 AI Recommendation'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Recommended inventory action based on historical risk and inventory metrics'
        '</div>',
        unsafe_allow_html=True
    )


    # ======================================
    # AI VALUES
    # ======================================

    recommended_action = sku[
        "recommended_action"
    ]

    priority = sku[
        "priority"
    ]

    stockout_rate = float(
        sku["stockout_rate"]
    )


    # ======================================
    # PRIORITY & STOCKOUT RATE
    # ======================================

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Inventory Priority",
            priority
        )


    with col2:

        st.metric(
            "Historical Stockout Rate",
            f"{stockout_rate:.2f}%"
        )


    # ======================================
    # RECOMMENDED ACTION
    # ======================================

    st.markdown( f"""<div class="recommendation-card">
      <div class="kpi-label">RECOMMENDED ACTION</div> 
      <div class="kpi-value" style="font-size:20px;">💡 {recommended_action}</div>
        </div>""", unsafe_allow_html=True )
