import streamlit as st
import streamlit.components.v1 as components
import time

# Simulated tools and emojis/icons
TOOLS = {
    "ToolA": lambda x: f"Response from ToolA to '{x}'",
    "ToolB": lambda x: f"Response from ToolB to '{x}'",
    "ToolC": lambda x: f"Response from ToolC to '{x}'",
}

TOOL_ICONS = {
    "ToolA": "🧠",
    "ToolB": "🛠️",
    "ToolC": "🔍"
}

# Run the toolchain
def process_query(query):
    history = []
    input_ = query
    for tool_name, tool_func in TOOLS.items():
        time.sleep(0.5)
        response = tool_func(input_)
        history.append({
            "tool": tool_name,
            "input": input_,
            "response": response
        })
        input_ = response
    return history

# Mermaid.js generator
def generate_mermaid(history, initial_query):
    lines = ["graph LR"]
    prev = f"Query[\"{initial_query}\"]"
    for i, step in enumerate(history):
        tool_node = f"Tool{i}[{step['tool']}]"
        resp_node = f"Resp{i}[\"{step['response']}\"]"
        lines.append(f"{prev} --> {tool_node}")
        lines.append(f"{tool_node} --> {resp_node}")
        prev = resp_node
    return "\n".join(lines)

# Streamlit UI
st.set_page_config(page_title="Tool Chain Visualizer", layout="wide")
st.title("🔧 Tool Chain Visualizer")

# Sidebar view selector
view_option = st.sidebar.radio(
    "📊 Select Visualization Mode",
    ("Mermaid.js", "Timeline", "Expander", "Grid", "Tabs", "Chat-style")
)

query = st.text_input("Enter your query:")

if st.button("Run"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        history = process_query(query)

        # ---- Mermaid.js View ----
        if view_option == "Mermaid.js":
            st.subheader("📊 Mermaid.js Diagram")
            mermaid_code = generate_mermaid(history, query)
            components.html(f"""
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <div class="mermaid">{mermaid_code}</div>
            <script>mermaid.initialize({{startOnLoad:true}});</script>
            """, height=500, scrolling=True)

        # ---- Timeline View ----
        elif view_option == "Timeline":
            st.subheader("🕓 Timeline View")
            for i, step in enumerate(history):
                st.markdown(f"""
                #### Step {i+1}: `{step['tool']}`
                - **Input:** `{step['input']}`
                - **Response:** `{step['response']}`
                """)

        # ---- Expander View ----
        elif view_option == "Expander":
            st.subheader("📂 Expander View")
            for i, step in enumerate(history):
                with st.expander(f"{step['tool']} (Step {i+1})"):
                    st.code(step['input'], language='text')
                    st.success(step['response'])

        # ---- Grid View ----
        elif view_option == "Grid":
            st.subheader("📊 Grid View")
            for i, step in enumerate(history):
                cols = st.columns(2)
                cols[0].markdown(f"#### {TOOL_ICONS.get(step['tool'], '🔧')} {step['tool']} Input")
                cols[0].code(step['input'], language='text')
                cols[1].markdown("#### 🧾 Response")
                cols[1].success(step['response'])

        # ---- Tabs View ----
        elif view_option == "Tabs":
            st.subheader("🧭 Tabs View")
            tabs = st.tabs([f"{TOOL_ICONS.get(h['tool'], '🔧')} {h['tool']}" for h in history])
            for tab, h in zip(tabs, history):
                with tab:
                    st.code(h["input"], language="text")
                    st.success(h["response"])

        # ---- Chat-style View ----
        elif view_option == "Chat-style":
            st.subheader("💬 Chat-style View")
            st.chat_message("user").write(query)
            for h in history:
                avatar = TOOL_ICONS.get(h["tool"], "🤖")
                with st.chat_message("assistant", avatar=avatar):
                    st.markdown(f"**{h['tool']}**")
                    st.markdown(f"**Input:** `{h['input']}`")
                    st.success(f"**Response:** {h['response']}")

        with st.expander("📜 Full JSON Trace"):
            st.json(history)
