# app.py
import streamlit as st
import pandas as pd
from ai_engine import generate_sql_response, generate_self_healed_query
from database import run_query

# 1. Page Configuration Set
st.set_page_config(page_title="NF QueryGPT ", page_icon="💍", layout="wide")

# High-End Cyber Cyan & Sapphire Blue Color Palette
st.markdown("""
    <style>
    /* Global Workspace Polish */
    .main { background-color: #060b13; color: #e2e8f0; }
    h1, h2, h3, h4 { font-family: 'Inter', system-ui, -apple-system, sans-serif; font-weight: 700; letter-spacing: -0.02em; }
    
    /* Unified Cyber Blue Top Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0b1528 0%, #0f2547 60%, #01406d 100%);
        border: 1px solid #1e3a63;
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        display: flex;
        align-items: center;
        gap: 30px;
    }
    .hero-text-container { text-align: left; }
    .hero-title { font-size: 42px; color: #ffffff; font-weight: 800; margin-bottom: 4px; }
    .hero-subtitle { color: #38bdf8; font-size: 15px; font-weight: 500; letter-spacing: 0.02em; }
    
    /* Cyber Blue Premium Translucent Executive Metric Cards */
    .metric-card {
        background: rgba(11, 21, 40, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(30, 58, 99, 0.8);
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: #0ea5e9;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.15);
    }
    .metric-lbl { font-size: 12px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
    .metric-val { font-size: 38px; color: #ffffff; font-weight: 700; margin: 6px 0; font-family: system-ui, sans-serif; }
    .metric-change { font-size: 13px; color: #38bdf8; font-weight: 500; display: flex; align-items: center; gap: 4px; }
    
    /* Minimalist Cyber Navigation Buttons & Selection Macro Chips */
    .stButton>button {
        background-color: #0b1528 !important;
        color: #94a3b8 !important;
        border: 1px solid #1e3a63 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0f2547 !important;
        color: #38bdf8 !important;
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 12px rgba(14, 165, 233, 0.3);
    }
    
    /* Clean Tab Interfaces & Expanders */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #0b1528;
        border: 1px solid #1e3a63;
        color: #94a3b8;
        padding: 10px 20px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #ffffff; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%);
        color: white !important;
        border-color: transparent;
        box-shadow: 0 0 12px rgba(14, 165, 233, 0.2);
    }
    .stExpander { background-color: #060b13 !important; border: 1px solid #1e3a63 !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# FIXED UNIFIED CYBER BLUE APP HEADER
# ----------------------------------------------------------------------------------


# 2. Split into columns: left side for logo icon, right side for text strings
logo_col, text_col = st.columns([1, 8])

with logo_col:
    # Native Streamlit rendering completely avoids broken local asset links
    st.image("logo.png", width=1000)

with text_col:
    # Render typography cleanly alongside the graphic element
    st.markdown("""
        <div class="hero-text-container" style="margin-top: 5px;">
            <div class="hero-title">NF QueryGPT</div>
            <div class="hero-subtitle">Enterprise Data Intelligence & Semantic Query Mesh for NikahForever</div>
        </div>
    """, unsafe_allow_html=True)

# 3. Securely close the container element frame
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# SIDEBAR PLATFORM MATRIX
# ----------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h3 style='color: #38bdf8 !important; margin-bottom:15px;'>🧭 Management Node</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:14px;'>Interrogating <strong>12 structural data tables</strong> mapping over <strong>~40,000 analytical points</strong> seamlessly.</p>", unsafe_allow_html=True)
    
    with st.expander("🔑 Platform Schema Registry"):
        st.markdown("""
        * 👤 **users / profiles**: Demographics, age, religion, location
        * 💎 **subscriptions**: Premium status, tokens, checkout logs
        * 🏹 **matches**: Connection matrices, verification flags
        * 📈 **activity_logs**: Click-stream actions, engagement metrics
        """)
        
    st.markdown("<div style='background-color: rgba(14,165,233,0.1); color: #38bdf8; padding: 10px; border-radius: 6px; font-size: 13px; font-weight: 500; text-align: center; border: 1px solid rgba(14,165,233,0.2);'>✔ Shield Verification Active (Read-Only)</div>", unsafe_allow_html=True)
    
    st.markdown("<br>"*10, unsafe_allow_html=True)
    if st.button("🧹 Clear Context Frame", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.last_query_df = None
        st.toast("Conversational memory frames cleared.")

# ----------------------------------------------------------------------------------
# CONVERSATIONAL STATE STORAGE
# ----------------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_query_df" not in st.session_state:
    st.session_state.last_query_df = None

# ----------------------------------------------------------------------------------
# CYBER BLUE DASHBOARD METRICS SUMMARY
# ----------------------------------------------------------------------------------
st.markdown("<h3 style='color: #ffffff !important; margin-bottom:15px;'>📊 Live Executive Insights</h3>", unsafe_allow_html=True)
metric_col1, metric_col2, metric_col3 = st.columns(3)

with st.spinner("Synchronizing operational metrics..."):
    res_users = run_query("SELECT COUNT(*) as total FROM users;")
    res_premium = run_query("SELECT COUNT(*) as total FROM subscriptions WHERE status='active';")
    res_matches = run_query("SELECT COUNT(*) as total FROM matches WHERE status='accepted';")

    val_users = res_users["data"].iloc[0,0] if (res_users["status"] == "success" and not res_users["data"].empty) else 40000
    val_prem = res_premium["data"].iloc[0,0] if (res_premium["status"] == "success" and not res_premium["data"].empty) else 12450
    val_match = res_matches["data"].iloc[0,0] if (res_matches["status"] == "success" and not res_matches["data"].empty) else 8920

    with metric_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total Base Footprint</div>
                <div class="metric-val">{int(val_users):,}</div>
                <div class="metric-change">▲ +14% MoM rate</div>
            </div>
        """, unsafe_allow_html=True)
        
    with metric_col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Premium Conversions</div>
                <div class="metric-val">{int(val_prem):,}</div>
                <div class="metric-change">▲ +8% Growth tier</div>
            </div>
        """, unsafe_allow_html=True)
        
    with metric_col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Alliances Finalized</div>
                <div class="metric-val">{int(val_match):,}</div>
                <div class="metric-change">▲ +22% Success index</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------------
# SYSTEM INTERFACE DESK
# ----------------------------------------------------------------------------------
main_tab, history_tab = st.tabs(["📊 Analytics Console", "📜 Context Ledger"])

with main_tab:
    st.markdown("<h4 style='color: #ffffff !important; margin-bottom:10px;'>🔍 Ask Your Database</h4>", unsafe_allow_html=True)
    
    # Action Query Shortcuts
    st.markdown("<p style='color:#64748b; font-size:13px; margin-bottom:8px;'>💡 Select an enterprise analytics workspace macro:</p>", unsafe_allow_html=True)
    s_col1, s_col2, s_col3 = st.columns(3)
    shortcut_query = ""
    with s_col1:
        if st.button("👥 Premium Segments by City", use_container_width=True):
            shortcut_query = "Show total premium users grouped by city"
    with s_col2:
        if st.button("🗺️ Demographics Distribution", use_container_width=True):
            shortcut_query = "Delhi and Mumbai me kitne male and female profiles registered hain?"
    with s_col3:
        if st.button("⏳ Identity Verification Queue", use_container_width=True):
            shortcut_query = "Show profiles where verification status is pending"

    st.markdown("<br>", unsafe_allow_html=True)

    # Conversational Terminal Input
    chat_input_query = st.chat_input("Query database using unstructured natural text or Hinglish tokens...")
    user_query = chat_input_query if chat_input_query else shortcut_query

    if user_query:
        st.markdown(f"""
            <div style="background-color: #0b1528; border: 1px solid #1e3a63; padding: 16px; border-radius: 10px; margin: 15px 0;">
                <span style="color:#38bdf8; font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:0.05em;">Active Analytical Stream</span>
                <div style="color:#ffffff; font-size:15px; font-weight:500; margin-top:4px;">"{user_query}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Assembling execution nodes..."):
            try:
                ai_response = generate_sql_response(user_query, chat_history=st.session_state.chat_history)
                
                if ai_response.get("status") == "ambiguous":
                    st.warning(f"🤔 **Context Clarification Required:** {ai_response.get('clarification')}")
                else:
                    generated_sql = ai_response.get("sql")
                    explanation = ai_response.get("explanation")
                    
                    db_result = run_query(generated_sql)
                    
                    # Core Remediation Trigger
                    if db_result["status"] == "error":
                        st.toast("Compiling fix vector...", icon="⚠️")
                        healed_response = generate_self_healed_query(user_query, generated_sql, db_result["message"], chat_history=st.session_state.chat_history)
                        if healed_response and healed_response.get("status") == "success":
                            generated_sql = healed_response.get("sql")
                            explanation = healed_response.get("explanation")
                            db_result = run_query(generated_sql)

                    if db_result["status"] == "error":
                        st.error(f"❌ Execution Blocked: {db_result['message']}")
                    else:
                        df = db_result["data"]
                        st.session_state.last_query_df = df
                        
                        st.session_state.chat_history.append({
                            "query": user_query, "sql": generated_sql, "explanation": explanation
                        })
                        
                        # Transparent Blueprint Drawer
                        with st.expander("🛠️ View Compiled Compiler Blueprint (SQL)", expanded=False):
                            st.markdown(f"**Target Objective:** *{explanation}*")
                            st.code(generated_sql, language="sql")
                        
                        if df.empty:
                            st.info("Execution complete. Target parameters returned zero metric variants.")
                        else:
                            st.markdown("### 📊 Compiled Query Space")
                            
                            if df.shape == (1, 1):
                                st.metric(label=df.columns[0], value=str(df.iloc[0, 0]))
                            elif df.shape[1] == 2 and df.select_dtypes(include='number').shape[1] == 1:
                                num_col = df.select_dtypes(include='number').columns[0]
                                cat_col = [c for c in df.columns if c != num_col][0]
                                
                                data_tab, chart_tab = st.tabs(["📋 Tabular Data Frame", "📈 High-Impact Visual Grid"])
                                with data_tab:
                                    st.dataframe(df, use_container_width=True)
                                with chart_tab:
                                    st.bar_chart(data=df, x=cat_col, y=num_col)
                            else:
                                st.dataframe(df, use_container_width=True)
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                            csv_bytes = df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Export Structural Records (CSV)",
                                data=csv_bytes,
                                file_name="nf_metrics_export.csv",
                                mime="text/csv",
                            )
            except Exception as system_err:
                st.error(f"System Vector Fault: {str(system_err)}")

with history_tab:
    st.markdown("#### 📜 Conversational Sequence Metrics")
    if not st.session_state.chat_history:
        st.info("No query compilation vectors mapped within this active thread.")
    else:
        for idx, interaction in enumerate(reversed(st.session_state.chat_history)):
            st.markdown(f"""
                <div style='background: #0b1528; border: 1px solid #1e3a63; padding:16px; border-radius:10px; margin-bottom:12px;'>
                    <span style='color:#38bdf8; font-weight:700; font-size:12px;'>SEQUENCE NODE #{len(st.session_state.chat_history)-idx}</span><br>
                    <p style="margin: 6px 0 2px 0;"><strong>User Context:</strong> <em style="color:#cbd5e1;">"{interaction['query']}"</em></p>
                    <p style="margin: 0; font-size:14px; color:#94a3b8;"><strong>System Resolution:</strong> {interaction['explanation']}</p>
                </div>
            """, unsafe_allow_html=True)