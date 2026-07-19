import streamlit as st
from pipeLine import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔎",
    layout="wide",
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔎 Research Assistant")
    st.markdown(
        "This app runs a 4-agent pipeline:\n\n"
        "1. **Search Agent** – finds recent sources\n"
        "2. **Reader Agent** – scrapes the best URL\n"
        "3. **Writer Agent** – drafts the report\n"
        "4. **Critic Agent** – reviews the report\n"
    )
    st.divider()
    show_intermediate = st.checkbox("Show intermediate agent steps", value=True)
    st.caption("Powered by LangChain / LangGraph agents")

# ---------- Main ----------
st.title("Multi-Agent Research Assistant")
st.write("Enter a topic below and let the agents research, write, and critique a report for you.")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("research_form"):
    topic = st.text_input("Research topic", placeholder="e.g. Impact of quantum computing on cryptography")
    submitted = st.form_submit_button("Run Research Pipeline", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        status_box = st.status("Starting research pipeline...", expanded=True)
        try:
            status_box.write("🔍 **Step 1** — Search agent is gathering information...")
            # Run the full pipeline (all 4 steps happen inside run_research_pipeline)
            state = run_research_pipeline(topic)

            status_box.write("📄 **Step 2** — Reader agent scraped the top source.")
            status_box.write("✍️ **Step 3** — Writer agent drafted the report.")
            status_box.write("🧐 **Step 4** — Critic agent reviewed the report.")
            status_box.update(label="Pipeline complete ✅", state="complete", expanded=False)

            st.session_state.history.insert(0, {"topic": topic, "state": state})

        except Exception as e:
            status_box.update(label="Pipeline failed ❌", state="error")
            st.error(f"Something went wrong while running the pipeline:\n\n{e}")

# ---------- Display results ----------
if st.session_state.history:
    latest = st.session_state.history[0]
    state = latest["state"]

    st.divider()
    st.subheader(f"Results for: *{latest['topic']}*")

    tab_report, tab_feedback, tab_steps = st.tabs(["📑 Final Report", "🧐 Critic Feedback", "🧩 Agent Steps"])

    with tab_report:
        st.markdown(state.get("report", "_No report generated._"))
        st.download_button(
            "Download report as .md",
            data=str(state.get("report", "")),
            file_name=f"{latest['topic'][:40].strip().replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.markdown(state.get("feedback", "_No feedback generated._"))

    with tab_steps:
        if show_intermediate:
            with st.expander("Step 1 — Search Results", expanded=False):
                st.write(state.get("search_result", ""))
            with st.expander("Step 2 — Scraped Content", expanded=False):
                st.write(state.get("scraped_content", ""))
        else:
            st.info("Enable 'Show intermediate agent steps' in the sidebar to view raw agent outputs.")

    # ---------- Past runs ----------
    if len(st.session_state.history) > 1:
        st.divider()
        st.subheader("Previous runs")
        for i, run in enumerate(st.session_state.history[1:], start=1):
            with st.expander(f"{run['topic']}"):
                st.markdown(run["state"].get("report", "_No report available._"))
else:
    st.info("No research run yet. Enter a topic above and click **Run Research Pipeline**.")