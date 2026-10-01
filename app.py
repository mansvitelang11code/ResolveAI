import streamlit as st

st.set_page_config(
    page_title="ResolveAI",
    page_icon="🤖"
)
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }
    .status {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    background-color: #e8f5e9;
    color: #2e7d32;
    font-weight: 600;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================= KNOWLEDGE BASE =================

knowledge_base = {
    "network": {
        "keywords": ["wifi", "wi-fi", "internet", "network"],
        "diagnosis": "Network connectivity problem detected.",
        "actions": [
            "Check whether WiFi is turned ON.",
            "Reconnect to the network.",
            "Restart the WiFi adapter.",
            "Restart the laptop if required."
        ]
    },

    "performance": {
        "keywords": ["slow", "lag", "hang", "freeze"],
        "diagnosis": "Computer performance problem detected.",
        "actions": [
            "Close unnecessary applications.",
            "Check available storage.",
            "Restart the computer.",
            "Check system performance if the issue continues."
        ]
    },

    "vpn": {
        "keywords": ["vpn", "remote access"],
        "diagnosis": "VPN / remote access problem detected.",
        "actions": [
            "Check internet connection.",
            "Reconnect to VPN.",
            "Restart the VPN application."
        ]
    }
}


# ================= AGENT =================

def resolve_issue(problem):

    text = problem.lower()

    # Agent selects the relevant knowledge
    selected_issue = None

    for issue, data in knowledge_base.items():
        for keyword in data["keywords"]:
            if keyword in text:
                selected_issue = issue
                break

        if selected_issue:
            break

    # Unknown issue
    if selected_issue is None:
        return {
            "category": "Unknown IT Issue",
            "priority": "High",
            "diagnosis": "The agent could not identify the issue confidently.",
            "actions": [
                "Collect more information from the employee.",
                "Create an IT support ticket."
            ],
            "decision": "ESCALATE TO HUMAN IT SUPPORT"
        }

    data = knowledge_base[selected_issue]

    # VPN gets escalation decision
    if selected_issue == "vpn":
        decision = "ESCALATE TO HUMAN IT SUPPORT"
        priority = "High"
    else:
        decision = "AUTONOMOUS RESOLUTION POSSIBLE"
        priority = "Medium"

    return {
        "category": selected_issue.upper(),
        "priority": priority,
        "diagnosis": data["diagnosis"],
        "actions": data["actions"],
        "decision": decision
    }


# ================= USER INTERFACE =================

st.title("🤖 ResolveAI")
st.markdown('<div class="status">🟢 Agent Online</div>', unsafe_allow_html=True)
st.info("🎫 Triage  →  🧠 Knowledge  →  🔍 Diagnosis  →  🛠️ Action  →  ✅ Resolve")
st.caption("Autonomous IT support • Triage → Diagnosis → Troubleshooting → Resolution")
st.subheader(
    "AI IT Service Desk Autonomous Resolution Agent"
)

st.write(
    "ResolveAI analyzes employee IT problems, "
    "selects relevant knowledge, diagnoses the issue, "
    "recommends actions and decides whether to resolve "
    "or escalate the problem."
)
st.subheader("💬 What can I help you fix?")
problem = st.text_area(
    


    "📝 Enter your IT problem",
    placeholder="Example: My WiFi is not connecting."
)
st.info("🤖 Agent ready — describe your IT issue and I’ll analyze it.")
if st.button("🚀 Analyze & Resolve"):

    if problem.strip() == "":
        st.warning("Please enter an IT problem.")

    else:

        result = resolve_issue(problem)

        st.success("Agent Analysis Completed!")
        st.subheader("🤖 AI Resolution Report")
        st.divider()
        st.write("### 🎫 Ticket Triage")
        st.write("**Category:**", result["category"])
        st.write("**Priority:**", result["priority"])

        st.write("### 🔍 Diagnosis")
        st.write(result["diagnosis"])

        st.write("### 🛠️ Recommended Actions")

        for number, action in enumerate(result["actions"], 1):
            st.write(f"**{number}.** {action}")

        st.write("### 🤖 Agent Decision")

        if "ESCALATE" in result["decision"]:
            st.error("🚨 " + result["decision"])
        else:
            st.success("✅ " + result["decision"])