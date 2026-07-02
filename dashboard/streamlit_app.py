import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="BrandPulse AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 BrandPulse AI")
st.caption("Multi-agent media intelligence platform")

# Sidebar — brand config
with st.sidebar:
    st.header("Configuration")
    brand = st.text_input("Primary Brand", value="Tesla")
    competitors_input = st.text_input("Competitors (comma separated)", value="Rivian")
    competitors = [c.strip() for c in competitors_input.split(",") if c.strip()]
    days = st.slider("Sentiment window (days)", 1, 30, 7)
    session_id = f"dashboard-{brand.lower()}"

    st.divider()
    if st.button("Run Ingestion", use_container_width=True):
        with st.spinner(f"Ingesting content for {brand}..."):
            res = requests.post(f"{API_BASE}/ingest", json={"brand": brand})
            if res.status_code == 200:
                data = res.json()
                st.success(f"Indexed {data['chunks_indexed']} new chunks")
            else:
                st.error("Ingestion failed")

# Main layout — 3 columns
col1, col2, col3 = st.columns(3)

# --- Metric: Total mentions ---
with col1:
    try:
        res = requests.get(f"{API_BASE}/brands/{brand}/sentiment?days={days}")
        sentiment_data = res.json()
        st.metric("Total Mentions", sentiment_data["total_mentions"], f"Last {days} days")
    except:
        st.metric("Total Mentions", "—")

# --- Metric: Crisis status ---
with col2:
    try:
        res = requests.get(f"{API_BASE}/brands/{brand}/crisis-check")
        crisis_data = res.json()
        if crisis_data["spike_detected"]:
            st.metric("Crisis Status", "⚠️ ALERT", f"Spike ratio: {crisis_data['spike_ratio']}x")
        else:
            st.metric("Crisis Status", "✅ Normal", f"Spike ratio: {crisis_data['spike_ratio']}x")
    except:
        st.metric("Crisis Status", "—")

# --- Metric: Brands tracked ---
with col3:
    st.metric("Brands Tracked", len(competitors) + 1, f"{brand} + {len(competitors)} competitors")

st.divider()

# --- Sentiment trend chart ---
st.subheader(f"📈 Mention Volume — {brand} (last {days} days)")
try:
    res = requests.get(f"{API_BASE}/brands/{brand}/sentiment?days={days}")
    data = res.json()
    series = data["series"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[p["date"] for p in series],
        y=[p["mention_count"] for p in series],
        mode="lines+markers",
        name=brand,
        line=dict(color="#E85D30", width=2.5),
        marker=dict(size=6)
    ))

    # Add competitor lines
    for comp in competitors:
        try:
            res_c = requests.get(f"{API_BASE}/brands/{comp}/sentiment?days={days}")
            comp_data = res_c.json()
            fig.add_trace(go.Scatter(
                x=[p["date"] for p in comp_data["series"]],
                y=[p["mention_count"] for p in comp_data["series"]],
                mode="lines+markers",
                name=comp,
                line=dict(width=2),
                marker=dict(size=6)
            ))
        except:
            pass

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Mention Count",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Could not load chart: {e}")

st.divider()

# --- Two columns: Crisis detail + Competitive snapshot ---
left, right = st.columns(2)

with left:
    st.subheader("🚨 Crisis Monitor")
    try:
        res = requests.get(f"{API_BASE}/brands/{brand}/crisis-check")
        crisis = res.json()
        st.json(crisis)
    except:
        st.error("Could not load crisis data")

with right:
    st.subheader("🏁 Competitive Snapshot")
    try:
        all_brands = [brand] + competitors
        rows = []
        for b in all_brands:
            res = requests.get(f"{API_BASE}/brands/{b}/sentiment?days={days}")
            d = res.json()
            rows.append({"Brand": b, "Mentions": d["total_mentions"]})

        fig2 = px.bar(
            rows,
            x="Brand",
            y="Mentions",
            color="Brand",
            title=f"Share of Voice — last {days} days"
        )
        fig2.update_layout(showlegend=False, height=280)
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load competitive data: {e}")

st.divider()

# --- AI Query (needs Gemini) ---
st.subheader("🤖 Ask BrandPulse AI")
st.caption("Requires Gemini API quota — will work once daily limit resets")

question = st.text_input(
    "Ask anything about your brand",
    placeholder="e.g. What are the dominant themes in Tesla coverage this week?"
)

if st.button("Ask", use_container_width=False) and question:
    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{API_BASE}/query", json={
                "question": question,
                "brand": brand,
                "competitors": competitors,
                "session_id": session_id
            })
            if res.status_code == 200:
                st.markdown(res.json()["answer"])
            else:
                st.error(f"API error: {res.text}")
        except Exception as e:
            st.error(f"Could not reach API: {e}")
