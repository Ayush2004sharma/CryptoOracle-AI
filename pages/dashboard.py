import streamlit as st
from pathlib import Path
from base64 import b64encode
import time
import re
from html import escape
from main_runner import run_trading_pipeline


# === Helper: embed local image if exists ===
def embed_image(path: Path) -> str:
    if path.exists():
        data = path.read_bytes()
        return f"data:image/png;base64,{b64encode(data).decode()}"
    return ""

faviconimg = embed_image(Path("assets/Neulogo.png"))

# === Page configuration ===
st.set_page_config(
    page_title="NeutroFi — AI Crypto Advisor",
    page_icon=faviconimg,
    # layout="centered",
    layout="centered",
)

# === Load external CSS ===
with open("assets/form.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open("assets/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === Maps(Label -> token) ===
TRADER_MAP = {
    "New buyer": "new_buyer",
    "Existing buyer": "existing_buyer",
}

HORIZON_MAP = {
    "Short term (1-3 months)": "short_term",
    "Medium term (3-6 months)": "medium_term",
    "Long term (6+ months)": "long_term",
}

TOKEN_MAP = {
    "short-term": "short term",
    "mid-term": "medium term",
    "long-term": "long term",
}


# === Session State ===
if "show_results" not in st.session_state:
    st.session_state.show_results = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}
if "fade_class" not in st.session_state:
    st.session_state.fade_class = "form-container"

# === Reset Function ===
def reset_form():
    st.session_state.show_results = False
    st.session_state.analysis_data = None
    st.session_state.fade_class = "form-container"
    st.session_state.user_inputs = {}

# === Run Analysis Function ===
def run_analysis(coin_label: str, trader_label: str, horizon_label: str):
    # Map inputs to internal tokens
    norm_trader = TRADER_MAP.get(trader_label, "existing_buyer")
    norm_horizon = HORIZON_MAP.get(horizon_label, "short_term")

    # Trigger fade-out animation
    st.session_state.fade_class = "form-container fade-out"
    st.session_state.animating = True

    with st.spinner("🔍 Give it a minute, Neu is analysing the market for you"):
        time.sleep(0.6)  # Simulate processing delay
        data = run_trading_pipeline(
            coin = coin_label,
            trader_position = norm_trader,
            duration = norm_horizon
        )

        if not isinstance(data, dict):
            st.error(f"Unexpected backend output type: {type(data)}. Expected dict.")
            st.stop()

        st.session_state.analysis_data = data
        st.session_state.user_inputs = {
            "coin": coin_label,
            "trader": trader_label,
            "horizon": horizon_label,
        }
        st.session_state.show_results = True
        st.session_state.animating = False
        st.rerun()


# === PAGE TITLE ===
# === FORM or RESULTS ===
if not st.session_state.show_results:
    fade_class = st.session_state.fade_class if "fade_class" in st.session_state else "form-container"
    # st.markdown(f"<div class='{st.session_state.fade_class}'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
          <h1 class="title">Your Investment Preference</h1>
          <p class="subtitle">Tell Neu about your goals and risk appetite so our agents can analyse the market for you.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"<div class='{fade_class}'>", unsafe_allow_html=True)
    with st.form("analysis_form", clear_on_submit=False):
        coin_label = st.selectbox(
            "🪙 What cryptocurrency are interested in today",
            [
                "Bitcoin", "Ethereum", "Ripple", "Tether", "Binance coin", "Solana",
                "USD Coin", "Dogecoin", "TRON", "Cardano", "Hyperliquid (HYPE)", "Stellar", 
                "Sui", "Chainlink", "Hedera", "Bitcoin cash", "Avalanche", "Wrapped Bitcoin", 
                "Toncoin", "Polkadot",
            ]
        )

        trader = st.radio(
            "What describes you best?",
            ["New buyer", "Existing buyer"],
            help="Is this your first time buying this asset, or are you looking to exit a position?"
        )

        duration = st.selectbox(
            "⏳ Investment Duration",
            ["Short term (1-3 months)", "Medium term (3-6 months)", "Long term (6+ months)"],
            # help="How long do you plan to hold this asset?"
        )


        submit = st.form_submit_button("Run Analytics", use_container_width=True)
        if submit:
            run_analysis(coin_label, trader, duration)

    st.markdown("</div>", unsafe_allow_html=True)

else:
    def _coerce_text(x) -> str:
        if x is None: return ""
        try: return str(x)
        except Exception: return ""

    # === Display Results ===
    data = st.session_state.analysis_data
    inputs = st.session_state.user_inputs

    # === Results Header ===
    coin_name = st.session_state.user_inputs.get("coin", "").strip()
    if coin_name:
        st.markdown(f"#### Neu's Verdict for {coin_name}")

    final_decision = _coerce_text(data.get("final_decision", "No decision made"))
    # final_decision = data.get("final_decision", "No decision made")
    horizon_token = data.get("horizon")
    confidence = data.get("confidence")
    final_reason = data.get("final_reason", "No reason provided")


    TOKEN_TO_LABEL = {
        "short_term": "Short term (1-3 months)",
        "medium_term": "Medium term (3-6 months)",
        "long_term": "Long term (6+ months)",
    }
    horizon_token = data.get("horizon")
    horizon_label = inputs.get("horizon_label")
    # horizon_display = inputs.get("horizon_label")
    horizon_display = horizon_label or TOKEN_TO_LABEL.get(horizon_token, "N/A")

    # Confidence (try to parse as float)
    raw_conf = data.get("confidence")
    try:
        conf_val = float(raw_conf) if raw_conf is not None else None
    except Exception:
        conf_val = None

    # ---- classes for decision (buy/hold/sell/neutral) ----
    fd_norm = final_decision.strip().lower()
    if "buy" in fd_norm:
        decision_class = "status-buy"
    elif "hold" in fd_norm:
        decision_class = "status-hold"
    elif "sell" in fd_norm:
        decision_class = "status-sell"
    else:
        decision_class = "status-neutral"

    
    # ---- classes for confidence bands ----
    if conf_val is None:
        conf_class = "conf-unknown"
        conf_display = "N/A"
    else:
        conf_display = f"{conf_val:.2f}"
        if conf_val < 0.5:
            conf_class = "conf-low"
        elif conf_val < 0.7:
            conf_class = "conf-mid"
        else:
            conf_class = "conf-high"

    final_reason = _coerce_text(data.get("final_reason") or "No reason provided")

    rec_txt = escape(str(final_decision))
    dur_txt = escape(str(horizon_display))
    conf_txt = "N/A" if confidence is None else escape(str(confidence))
    reason_txt = escape(str(final_reason))


    cards_html = f"""
    <div class="decisions">
      <div class="decision-card {decision_class}">
        <h5>Final Recommendation</h5>
        <p class="result-text text-color">{escape(final_decision)}</p>
      </div>
    
      <div class="decision-card">
        <h5>Timeframe</h5>
        <p class="result-text">{escape(horizon_display)}</p>
      </div>
    
      <div class="decision-card {conf_class}">
        <h5>Confidence score</h5>
        <p class="result-text">{escape(conf_display)}</p>
      </div>
    
      <div class="decision-card">
        <h5>Reason</h5>
        <p class="result-text reason-txt">{escape(final_reason)}</p>
      </div>
    </div>
    """
    
    st.markdown(cards_html, unsafe_allow_html=True)


    SECTION_NAMES = r"(Fundamentals?|News|Sentiment|Technicals?)"
    def _canon(name: str) -> str:
        n = name.strip().lower()
        if n.startswith("fundamental"):
            return "Fundamentals"
        if n.startswith("technical"):
            return "Technicals"
        if n.startswith("news"):
            return "News"
        return "Sentiment"

    def parse_overall(raw: str):
        out = {"summaries": {}, "recs": {}, "advice": {}}
        text = (raw or "").strip()

        # --- Market Summary body ---
        ms = re.search(
            r"Market Summary:\s*(.*?)(?:\n{2,}|(?:Short|Medium|Long)[^\n]*Recommendation:|Existing Holder Advice:|New Investor Advice:|$)",
            text, re.IGNORECASE | re.DOTALL
        )
        if ms:
            body = ms.group(1).strip()
            body = re.sub(r"[•*\-]\s*", "", body)  # drop bullets

            for m in re.finditer(
                rf"{SECTION_NAMES}:\s*(.*?)(?=(?:\s*{SECTION_NAMES}:)|(?:\s*(?:Short|Medium|Long)[^\n]*Recommendation:)|\s*Existing Holder Advice:|\s*New Investor Advice:|$)",
                body, re.IGNORECASE | re.DOTALL
            ):
                name = _canon(m.group(1))
                content = re.sub(r"\s+", " ", m.group(2)).strip()
                if content:
                    out["summaries"][name] = content

        # --- Advice blocks ---
        m = re.search(r"Existing Holder Advice:\s*([A-Za-z ]+)\s*[—\-–]\s*Reason:\s*(.*?)(?=New Investor Advice:|$)",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            out["advice"]["existing"] = {
                "action": m.group(1).strip(),
                "reason": re.sub(r"\s+", " ", m.group(2)).strip()
            }

        m = re.search(r"New Investor Advice:\s*([A-Za-z ]+)\s*[—\-–]\s*Reason:\s*(.*)$",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            out["advice"]["new"] = {
                "action": m.group(1).strip(),
                "reason": re.sub(r"\s+", " ", m.group(2)).strip()
            }

        return out


    # Tab Bar for Reports
    # st.markdown(f"<div class='reports-section'>", unsafe_allow_html=True)
    tab_labels = ["News", "Fundamentals", "Technical", "Sentiment", "Overall Summary"]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        st.markdown(data["reports"]["news"]["raw"])

    with tabs[1]:
        st.markdown(data["reports"]["fundamentals"]["raw"])

    with tabs[2]:
        st.markdown(data["reports"]["technical"]["raw"])

    with tabs[3]:
        st.markdown(data["reports"]["sentiment"]["raw"])

    with tabs[4]:
        overall_raw = data["reports"]["overall"]["raw"]
        parsed = parse_overall(overall_raw)

        # Optional: wrap with a class to target CSS tweaks
        st.markdown("<div class='report-overall'>", unsafe_allow_html=True)

        # Market Summary (major header; one paragraph per section)
        st.markdown("#### Market Summary")
        for section in ["Fundamentals", "News", "Sentiment", "Technicals"]:
            if section in parsed["summaries"]:
                st.markdown(f"**{section}:** {parsed['summaries'][section]}")


    # Try Another Coin Button
    st.button("🔄 Try another coin", use_container_width=True, on_click=reset_form)
    st.markdown("</div>", unsafe_allow_html=True)





# === Footer ===
with st.container(key="footer"):
    st.markdown(
        """
        <div class='footer'>
          <hr style='border-color:rgba(255,255,255,.08); border-width:0 0 1px; margin:2rem 0'>
          <div class='disclaimer'>
            <strong>Disclaimer:</strong> NeutroFi provides information and analysis only and is <em>not</em> financial advice. Crypto assets are highly volatile.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
