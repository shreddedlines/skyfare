import streamlit as st
import joblib
import json
import numpy as np
from datetime import date, time

st.set_page_config(
    page_title="SKYFARE — Flight Intelligence",
    page_icon="✈",
    layout="wide",
)

@st.cache_resource
def load_model():
    model = joblib.load("flight_price_model.pkl")
    with open("model_meta.json") as f:
        meta = json.load(f)
    return model, meta

model, meta = load_model()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@200;300;400&family=Barlow+Condensed:wght@300;400;500&display=swap');

:root {
    --bg:     #0c0f13;
    --border: rgba(255,255,255,0.10);
    --cream:  #d4cfc6;
    --cream2: #a09890;
    --sage:   #8fa89a;
    --sage2:  #6d8a7a;
    --display:'Bebas Neue', sans-serif;
    --body:   'Barlow', sans-serif;
    --cond:   'Barlow Condensed', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }

html, body, .stApp {
    background: var(--bg) !important;
    font-family: var(--body) !important;
    color: var(--cream);
}
.stApp {
    background:
        radial-gradient(ellipse 140% 70% at 50% -10%, rgba(70,90,110,0.55) 0%, transparent 60%),
        radial-gradient(ellipse 80%  50% at 85%  40%, rgba(50,65,85,0.3)  0%, transparent 55%),
        linear-gradient(170deg, #161c26 0%, #0c0f13 50%, #06080b 100%) !important;
}

#MainMenu, footer, header, .stDeployButton,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"] { display: none !important; }

.block-container { max-width: 100% !important; padding: 0 !important; }

/* ── NAV ── */
.nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 4rem; height: 68px;
    background: rgba(8,10,14,0.85); border-bottom: 1px solid var(--border);
    backdrop-filter: blur(16px);
    position: sticky; top: 0; z-index: 100;
}
.nav-left {
    font-family: var(--display); font-size: 1.35rem;
    letter-spacing: 0.18em; color: var(--cream); opacity: 0.8;
}
.nav-center {
    position: absolute; left: 50%; transform: translateX(-50%);
    display: flex; gap: 3rem;
    font-family: var(--cond); font-size: 0.72rem; font-weight: 300;
    letter-spacing: 2.5px; text-transform: uppercase; color: var(--cream2);
}
.nav-right {
    font-family: var(--cond); font-size: 0.72rem; font-weight: 300;
    letter-spacing: 2.5px; text-transform: uppercase; color: var(--cream2);
    display: flex; align-items: center; gap: 2.5rem;
}

/* ── HERO ── */
.hero {
    height: 100vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: var(--cond); font-size: 0.72rem; font-weight: 300;
    letter-spacing: 4px; text-transform: uppercase; color: var(--cream2);
    margin-bottom: 1.5rem;
}
.hero-wordmark {
    font-family: var(--display);
    font-size: clamp(5rem, 18vw, 22rem);
    line-height: 0.88; letter-spacing: 0.1em; color: var(--cream); opacity: 0.9;
    text-shadow: 0 0 120px rgba(143,168,154,0.13), 0 2px 40px rgba(0,0,0,0.6);
    margin-bottom: 0.18em; user-select: none;
}
.hero-sub {
    font-family: var(--cond);
    font-size: clamp(0.7rem, 1.8vw, 1.2rem); font-weight: 300;
    letter-spacing: 0.52em; text-transform: uppercase; color: var(--cream2);
}
.scroll-arrow {
    position: absolute; bottom: 2.5rem; left: 50%; transform: translateX(-50%);
    font-family: var(--cond); font-size: 0.62rem; letter-spacing: 3px;
    text-transform: uppercase; color: var(--sage2);
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    animation: floatDown 2.5s ease-in-out infinite;
}
@keyframes floatDown {
    0%,100% { opacity: 0.4; transform: translateX(-50%) translateY(0); }
    50%      { opacity: 0.9; transform: translateX(-50%) translateY(7px); }
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(143,168,154,0.32), transparent);
}

/* ── VERTICAL RULE ── */
.v-rule {
    position: fixed; right: 2.5rem; top: 50%; transform: translateY(-50%);
    width: 1px; height: 110px;
    background: linear-gradient(to bottom, transparent, rgba(212,207,198,0.25), transparent);
    pointer-events: none;
}

/* ── FORM ── */
.form-wrap { background: rgba(8,10,14,0.75); padding: 5rem 5rem 5.5rem; }
.form-section-head { margin-bottom: 3.5rem; }
.form-eyebrow {
    font-family: var(--cond); font-size: 0.68rem; letter-spacing: 4px;
    text-transform: uppercase; color: var(--sage); margin-bottom: 0.5rem;
}
.form-title {
    font-family: var(--display);
    font-size: clamp(2.8rem, 4.5vw, 5rem);
    letter-spacing: 0.07em; color: var(--cream); line-height: 1; opacity: 0.88;
}
.field-group-head {
    font-family: var(--cond); font-size: 0.95rem; font-weight: 500;
    letter-spacing: 3px; text-transform: uppercase; color: var(--sage);
    border-bottom: 1px solid rgba(143,168,154,0.16);
    padding-bottom: 0.8rem; margin-bottom: 1.75rem;
}

/* ── INPUTS ── */
.stSelectbox label, .stDateInput label,
.stTimeInput label, .stNumberInput label {
    font-family: var(--cond) !important; font-size: 0.88rem !important;
    font-weight: 500 !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; color: var(--cream) !important;
    margin-bottom: 6px !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 3px !important; color: var(--cream) !important;
    font-family: var(--body) !important; font-weight: 300 !important;
    font-size: 1.05rem !important;
}
.stSelectbox > div > div:focus-within {
    background: rgba(143,168,154,0.06) !important;
    border-color: rgba(143,168,154,0.4) !important;
    box-shadow: 0 0 0 2px rgba(143,168,154,0.1) !important;
}
.stDateInput > div > div > input,
.stTimeInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 3px !important; color: var(--cream) !important;
    font-family: var(--body) !important; font-weight: 300 !important;
    font-size: 1.05rem !important;
}
.stDateInput > div > div > input:focus,
.stTimeInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    background: rgba(143,168,154,0.06) !important;
    border-color: rgba(143,168,154,0.4) !important;
    box-shadow: 0 0 0 2px rgba(143,168,154,0.1) !important;
    outline: none !important;
}
.stSelectbox svg { color: var(--cream2) !important; }

[data-baseweb="popover"] {
    background: #10141c !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 5px !important;
    box-shadow: 0 24px 64px rgba(0,0,0,0.75) !important;
}
[data-baseweb="menu"] li {
    color: var(--cream2) !important; font-family: var(--body) !important;
    font-size: 1rem !important; font-weight: 300 !important; padding: 11px 18px !important;
}
[data-baseweb="menu"] li:hover {
    background: rgba(143,168,154,0.09) !important; color: var(--cream) !important;
}

/* ── CALCULATE BUTTON ── */
div.stButton > button {
    width: 100% !important;
    background: transparent !important; color: var(--cream) !important;
    border: 1px solid rgba(212,207,198,0.35) !important;
    border-radius: 100px !important; padding: 15px 2rem !important;
    font-family: var(--cond) !important; font-size: 1rem !important;
    font-weight: 500 !important; letter-spacing: 3px !important;
    text-transform: uppercase !important; box-shadow: none !important;
    transition: all 0.25s ease !important; margin-top: 0.5rem !important;
}
div.stButton > button:hover {
    background: rgba(143,168,154,0.1) !important;
    border-color: rgba(143,168,154,0.55) !important; color: #e8f0ec !important;
}
div.stButton > button:active {
    background: rgba(143,168,154,0.18) !important; transform: scale(0.99) !important;
}

/* ── RESULT ── */
.result-wrap { padding: 0 5rem 6rem; background: rgba(8,10,14,0.75); }
.result-top-divider {
    height: 1px; margin-bottom: 4rem;
    background: linear-gradient(90deg, transparent, rgba(143,168,154,0.32), transparent);
}
.price-display { text-align: center; padding: 3.5rem 2rem 3rem; position: relative; }
.price-display::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 55% 65% at 50% 50%, rgba(143,168,154,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.price-eyebrow {
    font-family: var(--cond); font-size: 0.7rem; letter-spacing: 4px;
    text-transform: uppercase; color: var(--sage); margin-bottom: 1rem;
}
.price-amount {
    font-family: var(--display);
    font-size: clamp(4rem, 13vw, 15rem);
    letter-spacing: 0.04em; line-height: 0.9; color: var(--cream); opacity: 0.92;
    text-shadow: 0 0 80px rgba(143,168,154,0.18), 0 4px 60px rgba(0,0,0,0.5);
}
.price-currency {
    font-size: 0.28em; vertical-align: top; margin-top: 0.3em;
    color: var(--sage); opacity: 0.8;
}
.price-route {
    font-family: var(--cond); font-size: 0.82rem; letter-spacing: 3px;
    text-transform: uppercase; color: var(--cream2); margin-top: 1.25rem;
}
.result-strip {
    display: grid; grid-template-columns: repeat(5, 1fr);
    border: 1px solid var(--border); border-radius: 2px; overflow: hidden;
    margin: 0 auto; max-width: 860px;
}
.result-cell {
    padding: 1.75rem 1.25rem; border-right: 1px solid var(--border); text-align: center;
}
.result-cell:last-child { border-right: none; }
.result-cell-label {
    font-family: var(--cond); font-size: 0.62rem; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--sage2); margin-bottom: 0.5rem;
}
.result-cell-val {
    font-family: var(--cond); font-size: 1.15rem;
    font-weight: 300; color: var(--cream); letter-spacing: 0.3px;
}
.model-strip {
    text-align: center; margin-top: 3.5rem; padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-family: var(--cond); font-size: 0.6rem;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: rgba(160,152,144,0.35);
}
div[data-testid="stAlert"] {
    background: rgba(143,168,154,0.06) !important;
    border: 1px solid rgba(143,168,154,0.22) !important;
    border-radius: 3px !important; color: var(--sage) !important;
    font-family: var(--cond) !important; font-size: 0.85rem !important;
    letter-spacing: 1px !important; box-shadow: none !important;
}

/* ── MOBILE RESPONSIVE ── */
@media (max-width: 768px) {
    .nav { padding: 0 1.2rem; }
    .nav-center { display: none; }
    .nav-right { display: none; }
    .v-rule { display: none; }

    .hero { padding: 0 1.2rem; }
    .hero-eyebrow { font-size: 0.6rem; letter-spacing: 2px; }
    .hero-wordmark { font-size: clamp(4rem, 22vw, 8rem); }
    .hero-sub { font-size: 0.65rem; letter-spacing: 0.25em; }

    .form-wrap { padding: 2.5rem 1.2rem 3rem; }
    .form-title { font-size: clamp(2rem, 10vw, 3rem); }

    .result-wrap { padding: 0 1.2rem 3rem; }
    .result-strip {
        grid-template-columns: repeat(2, 1fr);
        max-width: 100%;
    }
    .result-strip .result-cell:nth-child(2) { border-right: none; }
    .result-strip .result-cell:nth-child(5) {
        grid-column: span 2;
        border-right: none;
        border-top: 1px solid var(--border);
    }
    .result-cell { padding: 1.2rem 0.8rem; }

    .price-amount { font-size: clamp(3.5rem, 18vw, 7rem); }
    .price-route { font-size: 0.7rem; letter-spacing: 1.5px; }

    .model-strip { font-size: 0.55rem; letter-spacing: 1.5px; padding: 1.5rem 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav">
    <div class="nav-left">SKYFARE</div>
    <div class="nav-center">
        <span>Routes</span>
        <span>How It Works</span>
        <span>About</span>
    </div>
    <div class="nav-right">
        <span>India Domestic</span>
        <span>EN</span>
    </div>
</div>
<div class="v-rule"></div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">India Domestic · Machine Learning · 10,683 Flights</div>
    <div class="hero-wordmark">SKYFARE</div>
    <div class="hero-sub">F l i g h t &nbsp;&nbsp; I n t e l l i g e n c e</div>
    <div class="scroll-arrow">
        <span>scroll</span>
        <span>↓</span>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── FORM ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="form-wrap">
    <div class="form-section-head">
        <div class="form-eyebrow">— Enter Details</div>
        <div class="form-title">YOUR FLIGHT</div>
    </div>
""", unsafe_allow_html=True)

_, col, _ = st.columns([0.4, 7.2, 0.4])
with col:
    st.markdown('<div class="field-group-head">Route &amp; Airline</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        source = st.selectbox("From", sorted(meta["sources_list"]))
    with c2:
        destination = st.selectbox("To", sorted(meta["dest_all"]))
    with c3:
        airline = st.selectbox("Airline", sorted(meta["airlines_all"]))
    with c4:
        stops = st.selectbox("Stops", ["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"])

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="field-group-head">Schedule &amp; Duration</div>', unsafe_allow_html=True)
    c5, c6, c7, c8, c9 = st.columns(5)
    with c5:
        journey_date = st.date_input("Date", value=date.today())
    with c6:
        dep_time = st.time_input("Departure", value=time(6, 0))
    with c7:
        arr_time = st.time_input("Arrival", value=time(9, 0))
    with c8:
        dur_hours = st.number_input("Hrs", min_value=0, max_value=24, value=2)
    with c9:
        dur_mins = st.number_input("Mins", min_value=0, max_value=59, value=45)

    st.markdown('<br>', unsafe_allow_html=True)
    predict = st.button("Calculate Fare  →")

st.markdown('</div>', unsafe_allow_html=True)

# ── RESULT ────────────────────────────────────────────────────────────────────
if predict:
    if source == destination:
        _, ec, _ = st.columns([0.4, 7.2, 0.4])
        with ec:
            st.error("Origin and destination cannot be the same.")
    else:
        airline_enc = meta["dict_airlines"].get(airline, 0)
        dest_key    = "Delhi" if destination == "New Delhi" else destination
        dest_enc    = meta["dict_dest"].get(dest_key, 0)
        stops_enc   = meta["stop_map"].get(stops, 0)

        features = {
            "Airline":             airline_enc,
            "Destination":         dest_enc,
            "Total_Stops":         stops_enc,
            "Journey_day":         journey_date.day,
            "Journey_month":       journey_date.month,
            "Dep_Time_hour":       dep_time.hour,
            "Dep_Time_minute":     dep_time.minute,
            "Arrival_Time_hour":   arr_time.hour,
            "Arrival_Time_minute": arr_time.minute,
            "Duration_hours":      int(dur_hours),
            "Duration_mins":       int(dur_mins),
        }
        for sc in meta["source_cols"]:
            features[sc] = 1 if source == sc.replace("Source_", "") else 0

        row        = [features[col] for col in meta["feature_cols"]]
        prediction = model.predict([row])[0]
        price_fmt  = f"{int(round(prediction)):,}"
        dur_str    = f"{int(dur_hours)}h {int(dur_mins)}m"
        date_str   = journey_date.strftime("%d %b %Y")
        dep_str    = dep_time.strftime("%H:%M")
        arr_str    = arr_time.strftime("%H:%M")

        st.markdown(f"""
        <div class="divider"></div>
        <div class="result-wrap">
            <div class="result-top-divider"></div>
            <div class="price-display">
                <div class="price-eyebrow">— Estimated Fare</div>
                <div class="price-amount"><span class="price-currency">₹</span>{price_fmt}</div>
                <div class="price-route">{source} &nbsp;/&nbsp; {destination} &nbsp;·&nbsp; {airline}</div>
            </div>
            <div class="result-strip">
                <div class="result-cell">
                    <div class="result-cell-label">From</div>
                    <div class="result-cell-val">{source}</div>
                </div>
                <div class="result-cell">
                    <div class="result-cell-label">To</div>
                    <div class="result-cell-val">{destination}</div>
                </div>
                <div class="result-cell">
                    <div class="result-cell-label">Departure</div>
                    <div class="result-cell-val">{dep_str}</div>
                </div>
                <div class="result-cell">
                    <div class="result-cell-label">Duration</div>
                    <div class="result-cell-val">{dur_str}</div>
                </div>
                <div class="result-cell">
                    <div class="result-cell-label">Stops</div>
                    <div class="result-cell-val">{stops}</div>
                </div>
            </div>
            <div class="model-strip">
                Random Forest Regressor &nbsp;·&nbsp; R² 0.80 &nbsp;·&nbsp;
                MAE ₹1,171 &nbsp;·&nbsp; 10,683 Training Flights &nbsp;·&nbsp; by Kshitish
            </div>
        </div>
        """, unsafe_allow_html=True)
