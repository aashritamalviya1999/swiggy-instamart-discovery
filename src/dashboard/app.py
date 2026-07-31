import sys
from pathlib import Path

# Add project root to python path dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gr
import json
import logging
from src.database.connection import get_db_connection, init_db
from src.agents.pipeline_orchestrator import PipelineOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Premium Brand Colors: Blue, Swiggy Orange, and White
COLOR_BLUE = "#0056b3"
COLOR_ORANGE = "#fc8019"
COLOR_WHITE = "#ffffff"
COLOR_LIGHT_BG = "#f8f9fa"
COLOR_DARK_TEXT = "#1a202c"
COLOR_MUTED_TEXT = "#4a5568"
COLOR_BORDER = "#e2e8f0"

st.set_page_config(
    page_title="Swiggy Instamart AI Product Discovery Engine",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Light Styling matching Blue, Orange, and White palette
st.markdown(f"""
<style>
    .main {{
        background-color: {COLOR_LIGHT_BG};
        color: {COLOR_DARK_TEXT};
    }}
    h1, h2, h3, h4 {{
        color: {COLOR_BLUE} !important;
        font-family: 'Outfit', sans-serif;
    }}
    .sidebar .sidebar-content {{
        background-color: {COLOR_BLUE};
        color: #ffffff;
    }}
    .stCard {{
        background-color: {COLOR_WHITE};
        border-radius: 12px;
        padding: 20px;
        border: 1px solid {COLOR_BORDER};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }}
    .stMetric {{
        background-color: {COLOR_WHITE};
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_ORANGE};
        border-top: 1px solid {COLOR_BORDER};
        border-right: 1px solid {COLOR_BORDER};
        border-bottom: 1px solid {COLOR_BORDER};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .quote-box {{
        background-color: {COLOR_LIGHT_BG};
        border-left: 4px solid {COLOR_BLUE};
        padding: 12px;
        margin: 8px 0px;
        border-radius: 4px;
        font-style: italic;
        color: {COLOR_MUTED_TEXT};
    }}
    .badge {{
        background-color: rgba(0, 86, 179, 0.1);
        color: {COLOR_BLUE};
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 5px;
        border: 1px solid rgba(0, 86, 179, 0.2);
    }}
    .orange-badge {{
        background-color: rgba(252, 128, 25, 0.1);
        color: {COLOR_ORANGE};
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 5px;
        border: 1px solid rgba(252, 128, 25, 0.2);
    }}
</style>
""", unsafe_allow_html=True)

def get_db_stats():
    try:
        with get_db_connection() as conn:
            rev_count = conn.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
            analyzed_count = conn.execute("SELECT COUNT(*) FROM analysis_results").fetchone()[0]
            cluster_count = conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0]
            return {"reviews": rev_count, "analyzed": analyzed_count, "clusters": cluster_count}
    except Exception:
        return {"reviews": 0, "analyzed": 0, "clusters": 0}

stats = get_db_stats()

st.title("🍊 Swiggy Instamart AI Product Discovery Engine")
st.markdown("##### *AI-Powered Customer Feedback & Cross-Category Exploration Command Center*")
st.markdown("---")

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=120)
st.sidebar.markdown("### Control Center")

if stats["reviews"] == 0:
    st.sidebar.warning("Database is currently empty.")
    if st.sidebar.button("🚀 Run Discovery Engine Pipeline", type="primary"):
        with st.spinner("Executing 7-Agent AI Ingestion & Analysis Pipeline... Please wait..."):
            try:
                orchestrator = PipelineOrchestrator()
                res = orchestrator.run_pipeline()
                st.success(f"Pipeline executed! Ingested {res['reviews_collected']} items.")
                st.rerun()
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                logger.exception(e)
    st.stop()

# Load filter options
with get_db_connection() as conn:
    platforms = [row["platform"] for row in conn.execute("SELECT DISTINCT platform FROM reviews").fetchall()]
    segments = [row["user_segment"] for row in conn.execute("SELECT DISTINCT user_segment FROM analysis_results").fetchall()]
    
    categories_raw = conn.execute("SELECT detected_categories FROM analysis_results").fetchall()
    all_categories = set()
    for row in categories_raw:
        try:
            cats = json.loads(row["detected_categories"])
            for c in cats:
                all_categories.add(c)
        except:
            pass

# Sidebar Filters
st.sidebar.subheader("Global Filters")
selected_platforms = st.sidebar.multiselect("Platforms", ["All"] + platforms, default="All")
selected_segments = st.sidebar.multiselect("User Segments", ["All"] + list(segments), default="All")
selected_categories = st.sidebar.multiselect("Instamart Categories", ["All"] + list(all_categories), default="All")
selected_sentiment = st.sidebar.selectbox("Sentiment Filter", ["All", "positive", "neutral", "negative"], index=0)

if st.sidebar.button("🔄 Reload & Re-run Ingestion Pipeline", use_container_width=True):
    with st.spinner("Processing 7-Agent Ingestion Pipeline..."):
        try:
            orchestrator = PipelineOrchestrator()
            res = orchestrator.run_pipeline()
            st.success("Analysis complete!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Fetch data
query = """
SELECT r.id, r.platform, r.raw_content, r.cleaned_content, r.rating, r.created_at,
       a.sentiment, a.summary, a.intent, a.barriers, a.motivations, a.pain_points,
       a.feature_requests, a.shopping_behavior, a.user_segment, a.detected_categories
FROM reviews r
JOIN analysis_results a ON r.id = a.review_id
WHERE r.is_spam = 0
"""

with get_db_connection() as conn:
    df = pd.read_sql_query(query, conn)

# Filter df locally
if "All" not in selected_platforms and selected_platforms:
    df = df[df["platform"].isin(selected_platforms)]
if "All" not in selected_segments and selected_segments:
    df = df[df["user_segment"].isin(selected_segments)]
if selected_sentiment != "All":
    df = df[df["sentiment"] == selected_sentiment]
if "All" not in selected_categories and selected_categories:
    def has_cat(cat_str):
        try:
            cats = json.loads(cat_str)
            return any(c in selected_categories for c in cats)
        except:
            return False
    df = df[df["detected_categories"].apply(has_cat)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Reviews Analyzed", len(df))
with col2:
    pos_count = len(df[df["sentiment"] == "positive"])
    pos_pct = round((pos_count / len(df) * 100), 1) if len(df) > 0 else 0
    st.metric("Positive Sentiment", f"{pos_pct}%")
with col3:
    all_barriers = []
    for val in df["barriers"]:
        try:
            all_barriers.extend(json.loads(val))
        except:
            pass
    top_barrier = max(set(all_barriers), key=all_barriers.count) if all_barriers else "None"
    st.metric("Key Exploration Barrier", top_barrier[:30] + "...")
with col4:
    top_segment = df["user_segment"].mode()[0] if not df.empty else "None"
    st.metric("Active Target Segment", top_segment)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Overview & Sentiment", 
    "🎯 Themes & Barriers", 
    "👥 User Segments & Habits",
    "💡 UX Discovery Insights",
    "🏆 Opportunity Scorecard",
    "🔍 Review Explorer",
    "⚙️ Engine Workflow & Methodology"
])

# ----- TAB 1: OVERVIEW -----
with tab1:
    st.subheader("Dataset Source Bifurcation")
    
    # Platform counts dictionary from database query
    counts = df["platform"].value_counts().to_dict()
    
    col_plat1, col_plat2, col_plat3, col_plat4, col_plat5, col_plat6 = st.columns(6)
    with col_plat1:
        st.metric("Play Store Reviews", counts.get("play_store", 0))
    with col_plat2:
        st.metric("Reddit Discussions", counts.get("reddit", 0))
    with col_plat3:
        st.metric("App Store Reviews", counts.get("app_store", 0))
    with col_plat4:
        st.metric("YouTube Comments", counts.get("youtube", 0))
    with col_plat5:
        st.metric("Twitter Posts", counts.get("twitter", 0))
    with col_plat6:
        st.metric("Quora Discussions", counts.get("quora", 0))
        
    st.markdown("---")
    st.subheader("Sentiment Analysis & Feedback Volume")
    
    col_t1_1, col_t1_2 = st.columns([1, 2])
    with col_t1_1:
        sentiment_counts = df["sentiment"].value_counts().reset_index()
        fig_pie = px.pie(
            sentiment_counts,
            values="count",
            names="sentiment",
            title="Customer Sentiment Distribution",
            color="sentiment",
            color_discrete_map={"positive": "#28a745", "neutral": "#ffc107", "negative": "#dc3545"},
            hole=0.45
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_t1_2:
        platform_counts = df["platform"].value_counts().reset_index()
        fig_bar = px.bar(
            platform_counts,
            x="platform",
            y="count",
            title="Feedback Volume by Channel Source",
            color="platform",
            color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE, "#17a2b8", "#6c757d", "#fd7e14"]
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Customer Keywords & Word Frequencies")
    words = []
    for text in df["cleaned_content"]:
        w_list = [w.lower().strip() for w in text.split() if len(w) > 4 and w.lower() not in ["swiggy", "delivery", "minutes", "order", "instamart", "buying"]]
        words.extend(w_list)
        
    word_counts = pd.Series(words).value_counts().reset_index()[:15]
    word_counts.columns = ["Word", "Frequency"]
    
    fig_words = px.bar(
        word_counts,
        x="Frequency",
        y="Word",
        orientation="h",
        title="Top 15 Keywords in Reviews (Reflecting Customer Focus)",
        color="Frequency",
        color_continuous_scale=["#e0ecf8", COLOR_BLUE]
    )
    st.plotly_chart(fig_words, use_container_width=True)

# ----- TAB 2: THEMES -----
with tab2:
    st.subheader("Discovered Feedback Cluster Themes")
    with get_db_connection() as conn:
        clusters = pd.read_sql_query("SELECT * FROM clusters", conn)
        
    if not clusters.empty:
        for idx, row in clusters.iterrows():
            st.markdown(f"""
            <div class="stCard">
                <h4>Cluster #{row['id']}: {row['name']} <span class="badge">{row['size']} Reviews</span></h4>
                <p><strong>Subtheme:</strong> {row['subtheme']}</p>
                <p style="color:{COLOR_MUTED_TEXT};">{row['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No theme clusters discovered yet.")
        
    st.markdown("---")
    st.subheader("Friction Heatmap: Barriers by Instamart Categories")
    
    category_barriers = []
    for idx, row in df.iterrows():
        try:
            cats = json.loads(row["detected_categories"])
            barrs = json.loads(row["barriers"])
            for c in cats:
                for b in barrs:
                    category_barriers.append({"Category": c, "Barrier": b})
        except:
            pass
            
    if category_barriers:
        cb_df = pd.DataFrame(category_barriers)
        pivot_df = cb_df.pivot_table(index="Barrier", columns="Category", aggfunc="size", fill_value=0)
        
        fig_heat = px.imshow(
            pivot_df,
            labels=dict(x="Instamart Category", y="Adoption Barrier", color="Friction Count"),
            title="Category exploration friction matrix",
            color_continuous_scale="Oranges"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Insufficient category-to-barrier mapping data to render heatmap.")

# ----- TAB 3: SEGMENTS -----
with tab3:
    st.subheader("User Segments & Shopping Habits")
    
    col_t3_1, col_t3_2 = st.columns([2, 1])
    with col_t3_1:
        segment_counts = df["user_segment"].value_counts().reset_index()
        fig_seg = px.bar(
            segment_counts,
            y="user_segment",
            x="count",
            orientation="h",
            title="User Segment Distribution",
            color="user_segment",
            color_discrete_sequence=px.colors.sequential.Plotly3
        )
        st.plotly_chart(fig_seg, use_container_width=True)
        
    with col_t3_2:
        behavior_counts = df["shopping_behavior"].value_counts().reset_index()
        fig_beh = px.pie(
            behavior_counts,
            values="count",
            names="shopping_behavior",
            title="Shopping Habit Profile",
            color_discrete_sequence=[COLOR_BLUE, COLOR_ORANGE, "#6c757d", "#17a2b8"]
        )
        st.plotly_chart(fig_beh, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Category Purchasing Volume")
    all_cats_list = []
    for val in df["detected_categories"]:
        try:
            all_cats_list.extend(json.loads(val))
        except:
            pass
            
    cat_counts = pd.Series(all_cats_list).value_counts().reset_index()
    cat_counts.columns = ["Category", "Mentions"]
    
    fig_cat = px.bar(
        cat_counts,
        x="Category",
        y="Mentions",
        title="Volume of Mentions by Instamart Category",
        color="Mentions",
        color_continuous_scale=["#ffe8d6", COLOR_ORANGE]
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ----- TAB 4: INSIGHTS -----
with tab4:
    st.subheader("Validated UX Discovery Insights")
    st.markdown("Answers to the core PM discovery questions regarding category exploration barriers:")
    
    with get_db_connection() as conn:
        insights = conn.execute("SELECT * FROM insights").fetchall()
        
    if insights:
        for ins in insights:
            quotes = json.loads(ins["supporting_quotes"])
            contradict = json.loads(ins["contradicting_opinions"])
            platforms_list = json.loads(ins["platforms"])
            
            with st.expander(f"❓ {ins['question']} (Validation Confidence: {int(ins['confidence_score']*100)}%)"):
                st.markdown(f"**Synthesis:** {ins['answer']}")
                st.markdown(f"**Validation Explanation:** {ins['confidence_explanation']}")
                
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.markdown("💬 **Supporting Quotes from Data:**")
                    for q in quotes[:3]:
                        st.markdown(f"<div class='quote-box'>\"{q}\"</div>", unsafe_allow_html=True)
                with col_i2:
                    st.markdown("⚠️ **Exceptions & Contradictions:**")
                    for c in contradict[:2]:
                        st.markdown(f"<div class='quote-box'>\"{c}\"</div>", unsafe_allow_html=True)
                        
                st.markdown(
                    f"**Sources observed on:** " + " ".join([f"<span class='badge'>{p}</span>" for p in platforms_list]), 
                    unsafe_allow_html=True
                )
    else:
        st.info("No insights synthesized yet. Run the pipeline.")

# ----- TAB 5: OPPORTUNITIES -----
with tab5:
    st.subheader("Product Opportunity Prioritization backlog")
    st.markdown("Opportunities evaluated using ICE Scoring methodology (`Score = Impact * Confidence`):")
    
    with get_db_connection() as conn:
        opps = pd.read_sql_query("SELECT * FROM opportunities ORDER BY opportunity_score DESC", conn)
        
    if not opps.empty:
        st.dataframe(
            opps[["id", "title", "frequency", "impact", "confidence", "opportunity_score"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("Opportunity Detail Explorer")
        
        selected_opp_id = st.selectbox(
            "Select an Opportunity Brief to inspect evidence and expected business value:",
            opps["id"].tolist(),
            format_func=lambda x: opps[opps["id"] == x]["title"].values[0]
        )
        
        opp_row = opps[opps["id"] == selected_opp_id].iloc[0]
        
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            st.markdown(f"### 🏆 {opp_row['title']}")
            st.markdown(f"**Problem Statement:**\n{opp_row['problem']}")
            st.markdown(f"**Evidence Summary:**\n{opp_row['evidence']}")
            st.markdown(f"**Expected Business Value:**\n{opp_row['business_value']}")
        with col_o2:
            st.markdown("### 📊 Metrics")
            st.metric("ICE Score", f"{opp_row['opportunity_score']}/100")
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.metric("Expected Impact (1-10)", opp_row['impact'])
            with sub_col2:
                st.metric("Confidence (1-10)", opp_row['confidence'])
                
            st.markdown("### 💬 Supporting Quotes:")
            quotes = json.loads(opp_row['representative_quotes'])
            for q in quotes:
                st.markdown(f"<div class='quote-box'>\"{q}\"</div>", unsafe_allow_html=True)
                
            opp_json = opp_row.to_dict()
            st.download_button(
                label="📥 Export Opportunity Brief (JSON)",
                data=json.dumps(opp_json, indent=2),
                file_name=f"instamart_opportunity_{opp_row['id']}.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("No opportunities generated yet. Run the pipeline.")

# ----- TAB 6: EXPLORER -----
with tab6:
    st.subheader("Review Search Explorer")
    st.markdown("Search customer feedback records dynamically:")
    
    search_query = st.text_input("Enter search keywords (e.g. 'dmart', 'quality', 'delivery charge'):", "")
    
    filtered_df = df
    if search_query:
        filtered_df = df[df["cleaned_content"].str.contains(search_query, case=False, na=False)]
        
    st.write(f"Showing {len(filtered_df)} matches:")
    
    for idx, row in filtered_df.iterrows():
        rating_stars = "⭐" * int(row["rating"]) if pd.notna(row["rating"]) else "Social Thread"
        st.markdown(f"""
        <div class="stCard">
            <h5><strong>{row['author']}</strong> ({row['platform']}) - <span style="color: {COLOR_ORANGE};">{rating_stars}</span></h5>
            <p style="font-size: 14px; color: {COLOR_DARK_TEXT};">{row['raw_content']}</p>
            <p style="font-size: 12px; color: {COLOR_MUTED_TEXT};">
                <strong>Segment:</strong> {row['user_segment']} | 
                <strong>Behavior:</strong> {row['shopping_behavior']} |
                <strong>Categories:</strong> {row['detected_categories']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----- TAB 7: METHODOLOGY -----
with tab7:
    st.subheader("⚙️ Swiggy Instamart AI Discovery Engine Workflow & Methodology")
    st.markdown("---")
    
    st.markdown("### 🏗️ Sequential 7-Agent Pipeline Architecture")
    
    st.markdown("""
    ```mermaid
    graph TD
        A[Agent 1: Collector] -->|Raw Reviews| B[Agent 2: Cleaner]
        B -->|Clean English text & Spam flag| C[Agent 3: Analyzer]
        C -->|AI Profile & Segment Mapping| D[Agent 4: Clusterer]
        D -->|TF-IDF + KMeans Theme ID| E[Agent 5: Synthesizer]
        E -->|UX Insights Synthesis| F[Agent 6: Validator]
        F -->|Database Validation & Quotes| G[Agent 7: PM Recommendation]
        G -->|Prioritized Product opportunities| H[Streamlit Dashboard & API]
    ```
    """, unsafe_allow_html=False)

    st.markdown("---")
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.markdown(f"""
        #### 1. How the Workflow Gathers & Analyzes Data
        - **Ingestion & Bifurcation (Agent 1: Collector)**: Automatically aggregates feedback from **6 distinct source platforms** (Reddit, Google Play Store, iOS App Store, YouTube, Twitter, and Quora). It enforces a controlled bifurcation (e.g. Reddit: 200, Play Store: 300, etc.) to compile a high-fidelity dataset of 1,000 feedback entries.
        - **Sanitization & Normalization (Agent 2: Cleaner)**:
          - Strips URLs, HTML tags, and non-ASCII emojis.
          - Flags spam, referral codes, and repetitive keyword noise.
          - Translates **Hinglish shopping slang** (e.g., *accha* -> good, *mehanga* -> expensive, *kharab* -> bad) to English.
          - Performs exact duplicate checking to filter out redundant entries.
        - **Individual Behavioral Profiling (Agent 3: Analyzer)**: Extracts sentiment, intent, specific friction barriers, triggers/motivations, and maps customers to predefined cohorts (e.g., Pet Owner, Baby Product Buyer).
        """)
        
        st.markdown(f"""
        #### 2. How Themes are Identified
        - **Vector Space Embedding (Agent 4: Clusterer)**: Converts the cleaned reviews into numerical vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization, filtering out common English stop words.
        - **Unsupervised Semantic Clustering**: Runs **K-Means clustering** (configured for 4 distinct clusters) to identify natural semantic themes in customer complaints and behaviors.
        - **AI Theme Auto-labeling**: Submits the top-distance reviews near each cluster centroid to the LLM to generate descriptive theme names, subtheme tags, and summaries.
        """)
        
    with col_w2:
        st.markdown(f"""
        #### 3. How Insights are Generated
        - **Insight Synthesis (Agent 5: Synthesizer)**: Aggregates the cluster distributions, user segment breakdown, and barrier frequencies.
        - **Contextual Prompting**: Feeds this aggregated data to a specialized PM agent to answer the **8 core PM discovery questions** regarding shopping habits, exploration blocks, and unmet customer needs.
        """)
        
        st.markdown(f"""
        #### 4. How the Quality of Insights is Validated
        - **Automated Validation Engine (Agent 6: Validator)**: For each generated insight answer, it runs a programmatic verification loop:
          - Performs **keyword-based lookup** in the database to count matching reviews and calculate the cohort density.
          - Computes a quantitative **Confidence Score** based on the density of supporting records.
          - Extracts **actual customer quotes** (supporting reviews) to verify qualitative alignment.
          - Searches for **contradicting opinions** and edge cases to surface potential exceptions.
        - **PM Recommendation (Agent 7)**: Converts validated insights into actionable features prioritized by an **ICE Scoreboard** (Impact × Confidence).
        """)
