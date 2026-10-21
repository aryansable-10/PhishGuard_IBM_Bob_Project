"""
PhishGuard - Educational Phishing URL Analyzer
================================================
HOW TO RUN:
  pip install streamlit
  streamlit run app.py

DISCLAIMER: Educational estimate only. Does NOT visit or fetch URLs.
"""

import re
import streamlit as st

# ──────────────────────────────────────────────
# Page config  (must be FIRST Streamlit call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="PhishGuard – URL Threat Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════
# GLOBAL CSS  — heroic dark-cyber theme
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #020409 !important;
    color: #e2e8f0;
    font-family: 'Inter', system-ui, sans-serif;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* hide streamlit menu / footer */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e40af; border-radius: 3px; }

/* ══════════════════════════════════════
   HERO BANNER
══════════════════════════════════════ */
.hero {
    position: relative;
    width: 100%;
    min-height: 520px;
    background: linear-gradient(135deg, #020917 0%, #050d24 40%, #0a0624 100%);
    border-bottom: 1px solid #1e293b;
    overflow: hidden;
    display: flex;
    align-items: center;
    padding: 0 4rem;
    margin-bottom: 0;
}

/* animated dot-grid background */
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(circle, #1e40af22 1px, transparent 1px);
    background-size: 32px 32px;
    animation: gridMove 8s linear infinite;
    pointer-events: none;
}
@keyframes gridMove {
    0%   { background-position: 0 0; }
    100% { background-position: 32px 32px; }
}

/* sweeping glow */
.hero::after {
    content: '';
    position: absolute;
    top: -40%;
    left: -10%;
    width: 60%;
    height: 180%;
    background: radial-gradient(ellipse, #1e3a8a18 0%, transparent 70%);
    animation: glowPulse 6s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes glowPulse {
    0%   { opacity: .6; transform: translateX(0); }
    100% { opacity: 1;  transform: translateX(6%); }
}

.hero-left {
    position: relative;
    z-index: 10;
    max-width: 580px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #0f1f4a;
    border: 1px solid #1e40af55;
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 1.4rem;
}
.hero-badge .dot {
    width: 7px; height: 7px;
    background: #22d3ee;
    border-radius: 50%;
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; } 50% { opacity:0.2; }
}

.hero h1 {
    font-size: clamp(2.4rem, 4vw, 3.6rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1px;
    color: #f1f5f9;
    margin-bottom: 1rem;
}
.hero h1 span.accent {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 1.05rem;
    color: #94a3b8;
    line-height: 1.7;
    margin-bottom: 2rem;
    font-weight: 400;
}

.hero-stats {
    display: flex;
    gap: 2rem;
}
.stat-item { display: flex; flex-direction: column; }
.stat-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: #3b82f6;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 3px;
}

/* ── Hero right – SVG phishing visual ── */
.hero-right {
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    width: 420px;
}

/* ══════════════════════════════════════
   MAIN CONTENT AREA
══════════════════════════════════════ */
.main-wrap {
    max-width: 1100px;
    margin: 0 auto;
    padding: 3rem 2rem 4rem;
}

/* section label */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.6rem;
}
.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}
.section-sub {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 2rem;
}

/* ── Scan card ── */
.scan-card {
    background: linear-gradient(145deg, #0d1526, #0a1020);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.scan-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #1e40af, #0ea5e9, #1e40af);
    background-size: 200%;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

.scan-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
}

/* Streamlit input styling */
[data-testid="stTextInput"] input {
    background: #060c1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px #3b82f610 !important;
}
[data-testid="stTextInput"] label { display: none !important; }

/* ── Analyze button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8, #0ea5e9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
[data-testid="stButton"] > button:hover {
    opacity: .9 !important;
    transform: translateY(-1px) !important;
}

/* ── Result card ── */
.result-card {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-low    { background: #031a0e; border: 1px solid #166534; }
.result-medium { background: #1a1203; border: 1px solid #854d0e; }
.result-high   { background: #1a0303; border: 1px solid #991b1b; }

.risk-pill {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    border-radius: 999px;
    padding: 8px 20px;
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}
.pill-low    { background: #052e16; color: #4ade80; border: 1px solid #166534; }
.pill-medium { background: #1c1003; color: #fbbf24; border: 1px solid #92400e; }
.pill-high   { background: #1f0606; color: #f87171; border: 1px solid #991b1b; }

/* score bar */
.score-bar-wrap {
    margin: 1rem 0 1.4rem;
}
.score-bar-track {
    background: #0f172a;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    border: 1px solid #1e293b;
}
.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s ease;
}
.fill-low    { background: linear-gradient(90deg, #16a34a, #4ade80); }
.fill-medium { background: linear-gradient(90deg, #b45309, #fbbf24); }
.fill-high   { background: linear-gradient(90deg, #991b1b, #f87171); }
.score-txt {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 5px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Finding items ── */
.finding {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    background: #05091a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.5;
}
.finding-warn { border-left: 3px solid #ef4444; }
.finding-pass { border-left: 3px solid #22c55e; }
.finding-icon { font-size: 1rem; margin-top: 1px; flex-shrink: 0; }

/* ── Threat intel grid ── */
.intel-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.intel-card {
    background: #0a0f1e;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.intel-card:hover {
    border-color: #3b82f655;
    transform: translateY(-2px);
}
.intel-icon-wrap {
    width: 44px; height: 44px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
}
.ic-blue   { background: #0f2044; }
.ic-red    { background: #200a0a; }
.ic-yellow { background: #1a1203; }
.intel-card h4 {
    font-size: 0.88rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
}
.intel-card p {
    font-size: 0.78rem;
    color: #64748b;
    line-height: 1.5;
}

/* ── Example URLs ── */
.example-block {
    background: #060c1a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.example-block h4 {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}
.ex-low    { color: #4ade80; }
.ex-medium { color: #fbbf24; }
.ex-high   { color: #f87171; }
.url-code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #7dd3fc;
    background: #020917;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    word-break: break-all;
    margin-bottom: 0.3rem;
}

/* ── Tips ── */
.tips-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}
.tip-card {
    background: #070e20;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
}
.tip-num {
    font-size: 1.8rem;
    font-weight: 900;
    color: #1e3a8a;
    line-height: 1;
    margin-bottom: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
}
.tip-card h4 {
    font-size: 0.88rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.4rem;
}
.tip-card p {
    font-size: 0.8rem;
    color: #64748b;
    line-height: 1.5;
}

/* ── Disclaimer ── */
.disclaimer-bar {
    background: #050c1e;
    border: 1px solid #1e3a8a33;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    text-align: center;
    font-size: 0.78rem;
    color: #475569;
    margin-top: 3rem;
}
.disclaimer-bar b { color: #64748b; }

/* ── Footer ── */
.pg-footer {
    text-align: center;
    font-size: 0.72rem;
    color: #1e293b;
    padding: 2rem 0 1rem;
    letter-spacing: 1px;
}

/* hide Streamlit default padding */
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; }
div[data-testid="stVerticalBlock"] > div:has(> [data-testid="stMarkdownContainer"]) { padding: 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# DATA  – URL analysis engine
# ══════════════════════════════════════════════
URL_SHORTENERS = {
    "bit.ly","tinyurl.com","t.co","goo.gl","ow.ly","buff.ly",
    "rebrand.ly","is.gd","clck.ru","shorte.st","adf.ly","bc.vc",
    "cutt.ly","shorturl.at","tiny.cc","rb.gy",
}

def analyze_url(url: str) -> dict:
    """Text-only phishing signal detector. Never fetches the URL."""
    warnings, passed = [], []
    score = 0
    low = url.lower().strip()

    # 1. Raw IP address
    if re.search(r"https?://(\d{1,3}\.){3}\d{1,3}", low):
        warnings.append(("🔴", "Raw IP Address",
            "Legitimate services use domain names, not bare IP addresses. "
            "Attackers use IPs to bypass domain-reputation filters."))
        score += 40
    else:
        passed.append(("✅", "No raw IP address detected."))

    # 2. URL shortener
    try:
        domain = re.split(r"https?://", low)[-1].split("/")[0]
        base   = ".".join(domain.split(".")[-2:])
        if base in URL_SHORTENERS or domain in URL_SHORTENERS:
            warnings.append(("🔴", "URL Shortener Detected",
                "Short links mask the real destination, a common phishing tactic."))
            score += 30
        else:
            passed.append(("✅", "No known URL-shortening service found."))
    except Exception:
        pass

    # 3. Long URL
    if len(url) > 75:
        warnings.append(("🟡", f"Excessive URL Length ({len(url)} chars)",
            "Attackers pad URLs with random characters to confuse users and bypass filters."))
        score += 15
    else:
        passed.append(("✅", "URL length is within normal range."))

    # 4. Excessive subdomains
    try:
        dom = re.split(r"https?://", low)[-1].split("/")[0]
        if dom.count(".") > 3:
            warnings.append(("🟡", f"Suspicious Subdomains ({dom.count('.')} dots)",
                "Phishers embed trusted brand names as subdomains: 'paypal.com.evil.net'."))
            score += 20
        else:
            passed.append(("✅", "Subdomain depth looks normal."))
    except Exception:
        pass

    # 5. @ symbol
    if "@" in url:
        warnings.append(("🔴", "'@' Symbol in URL",
            "Browsers ignore everything before '@'. 'paypal.com@evil.com' resolves to evil.com."))
        score += 35
    else:
        passed.append(("✅", "No '@' redirection trick found."))

    # 6. Missing HTTPS
    if not low.startswith("https://"):
        warnings.append(("🟡", "Missing HTTPS",
            "HTTP traffic is unencrypted. Credentials entered here can be intercepted."))
        score += 15
    else:
        passed.append(("✅", "HTTPS encryption is present."))

    # 7. Phishing keywords
    keywords = ["login","signin","verify","update","secure","account",
                "banking","confirm","password","webscr","wallet","reset"]
    found = [k for k in keywords if k in low]
    if found:
        warnings.append(("🟡", f"Phishing Keywords: {', '.join(found)}",
            "These terms are hallmarks of credential-harvesting and fake login pages."))
        score += 10 * len(found)
    else:
        passed.append(("✅", "No common phishing keywords found."))

    score = min(score, 100)
    risk  = "Low" if score < 40 else ("Medium" if score < 70 else "High")
    return {"warnings": warnings, "passed": passed, "score": score, "risk": risk}


# ══════════════════════════════════════════════
# HERO BANNER  (pure HTML/CSS + inline SVG)
# ══════════════════════════════════════════════
HERO_SVG = """
<svg viewBox="0 0 420 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;filter:drop-shadow(0 0 30px #1e40af44);">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a1628"/>
      <stop offset="100%" stop-color="#06091a"/>
    </linearGradient>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1d4ed8"/>
      <stop offset="100%" stop-color="#0ea5e9"/>
    </linearGradient>
    <linearGradient id="hookGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#b91c1c"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background panel -->
  <rect width="420" height="340" rx="20" fill="url(#bg)" stroke="#1e293b" stroke-width="1"/>

  <!-- Decorative grid lines -->
  <g stroke="#1e293b" stroke-width="0.5" opacity="0.6">
    <line x1="0" y1="85" x2="420" y2="85"/>
    <line x1="0" y1="170" x2="420" y2="170"/>
    <line x1="0" y1="255" x2="420" y2="255"/>
    <line x1="105" y1="0" x2="105" y2="340"/>
    <line x1="210" y1="0" x2="210" y2="340"/>
    <line x1="315" y1="0" x2="315" y2="340"/>
  </g>

  <!-- ── PHISHING HOOK illustration ── -->
  <!-- fishing line -->
  <line x1="300" y1="10" x2="300" y2="95" stroke="#475569" stroke-width="1.5" stroke-dasharray="4,3"/>
  <!-- hook curve -->
  <path d="M300 95 Q300 140 270 140 Q240 140 240 115" stroke="url(#hookGrad)" stroke-width="3" fill="none" stroke-linecap="round"/>
  <!-- hook barb -->
  <path d="M240 115 L233 128 M240 115 L252 124" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round"/>
  <!-- bait = envelope -->
  <g transform="translate(276,62)" filter="url(#glow)">
    <rect width="48" height="34" rx="4" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.2"/>
    <polyline points="0,0 24,18 48,0" fill="none" stroke="#60a5fa" stroke-width="1.4"/>
    <text x="8" y="28" font-size="9" fill="#93c5fd" font-family="monospace">GET PRIZE</text>
  </g>

  <!-- ── SHIELD (center) ── -->
  <g transform="translate(150,100)" filter="url(#glow)">
    <path d="M60 0 L120 22 L120 75 Q120 115 60 135 Q0 115 0 75 L0 22 Z"
          fill="url(#shieldGrad)" opacity="0.15" stroke="url(#shieldGrad)" stroke-width="1.5"/>
    <path d="M60 12 L108 30 L108 75 Q108 108 60 124 Q12 108 12 75 L12 30 Z"
          fill="none" stroke="#3b82f6" stroke-width="1" opacity="0.5"/>
    <!-- checkmark -->
    <polyline points="36,68 52,84 84,54" fill="none" stroke="#22d3ee" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- ── FAKE EMAIL card ── -->
  <g transform="translate(20,160)">
    <rect width="170" height="110" rx="8" fill="#0d1526" stroke="#1e293b" stroke-width="1"/>
    <rect width="170" height="26" rx="8" fill="#1e293b"/>
    <rect width="170" height="18" rx="0" fill="#1e293b" y="8"/>
    <text x="10" y="19" font-size="8.5" fill="#64748b" font-family="monospace">FROM: support@paypa1.com</text>
    <text x="10" y="44" font-size="8" fill="#94a3b8" font-family="sans-serif">Your account has been</text>
    <text x="10" y="57" font-size="8" fill="#94a3b8" font-family="sans-serif">suspended. Click below</text>
    <text x="10" y="70" font-size="8" fill="#94a3b8" font-family="sans-serif">to verify immediately.</text>
    <!-- CTA button -->
    <rect x="10" y="82" width="150" height="20" rx="4" fill="#1d4ed8"/>
    <text x="85" y="96" font-size="9" fill="white" text-anchor="middle" font-weight="bold">Verify Account Now</text>
    <!-- red X overlay -->
    <line x1="0" y1="0" x2="170" y2="110" stroke="#ef444466" stroke-width="2"/>
    <line x1="170" y1="0" x2="0" y2="110" stroke="#ef444466" stroke-width="2"/>
  </g>

  <!-- ── FAKE URL bar ── -->
  <g transform="translate(20,285)">
    <rect width="380" height="36" rx="6" fill="#0a0e1a" stroke="#1e293b" stroke-width="1"/>
    <text x="12" y="23" font-size="9.5" fill="#64748b" font-family="monospace">http://</text>
    <text x="52" y="23" font-size="9.5" fill="#f87171" font-family="monospace">paypal.secure-update.xyz/login?</text>
    <text x="265" y="23" font-size="9.5" fill="#94a3b8" font-family="monospace">verify=true</text>
    <!-- danger badge -->
    <rect x="338" y="8" width="50" height="18" rx="4" fill="#7f1d1d" stroke="#ef4444" stroke-width="0.8"/>
    <text x="363" y="21" font-size="8" fill="#fca5a5" text-anchor="middle" font-weight="bold">DANGER</text>
  </g>

  <!-- ── Floating warning nodes ── -->
  <circle cx="28" cy="50" r="5" fill="#ef444433" stroke="#ef4444" stroke-width="1"/>
  <text x="37" y="54" font-size="8" fill="#ef4444" font-family="monospace">PHISH</text>

  <circle cx="340" cy="200" r="5" fill="#f59e0b33" stroke="#f59e0b" stroke-width="1"/>
  <text x="350" y="204" font-size="8" fill="#f59e0b" font-family="monospace">WARN</text>

  <circle cx="370" cy="50" r="5" fill="#22c55e33" stroke="#22c55e" stroke-width="1"/>
  <text x="340" y="44" font-size="8" fill="#22c55e" font-family="monospace">SCAN</text>
</svg>
"""

st.markdown(f"""
<div class="hero">
  <div class="hero-left">
    <div class="hero-badge">
      <span class="dot"></span>
      Active Threat Intelligence
    </div>
    <h1>Detect Phishing<br><span class="accent">Before It Strikes</span></h1>
    <p class="hero-sub">
      PhishGuard analyzes URL patterns against known phishing indicators —
      IP abuse, domain spoofing, shortlink traps, and more.
      100% client-side. Zero network requests.
    </p>
    <div class="hero-stats">
      <div class="stat-item">
        <span class="stat-num">7</span>
        <span class="stat-lbl">Signal Checks</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">0ms</span>
        <span class="stat-lbl">Network Calls</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">100%</span>
        <span class="stat-lbl">Privacy Safe</span>
      </div>
    </div>
  </div>
  <div class="hero-right">
    {HERO_SVG}
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

# ── Threat intel cards ──
st.markdown("""
<div style="margin:2.5rem 0 1rem">
  <div class="section-label">Threat Vectors</div>
  <div class="section-title">What PhishGuard Detects</div>
  <div class="section-sub">Seven heuristic checks run instantly against the URL text.</div>
</div>
<div class="intel-grid">
  <div class="intel-card">
    <div class="intel-icon-wrap ic-red">🎣</div>
    <h4>IP Address Abuse</h4>
    <p>Attackers host phishing pages on raw IPs to bypass domain-name blacklists.</p>
  </div>
  <div class="intel-card">
    <div class="intel-icon-wrap ic-yellow">🔗</div>
    <h4>URL Shorteners</h4>
    <p>Short links hide the real destination, making it impossible to assess risk at a glance.</p>
  </div>
  <div class="intel-card">
    <div class="intel-icon-wrap ic-blue">🕵️</div>
    <h4>Domain Spoofing</h4>
    <p>Excessive subdomains and look-alike domain names impersonate trusted brands.</p>
  </div>
  <div class="intel-card">
    <div class="intel-icon-wrap ic-red">⚠️</div>
    <h4>Credential Keywords</h4>
    <p>Terms like "login", "verify", "password" signal credential-harvesting pages.</p>
  </div>
  <div class="intel-card">
    <div class="intel-icon-wrap ic-yellow">🔓</div>
    <h4>Missing HTTPS</h4>
    <p>Unencrypted HTTP connections expose all data including passwords in transit.</p>
  </div>
  <div class="intel-card">
    <div class="intel-icon-wrap ic-blue">@</div>
    <h4>@ Redirection Trick</h4>
    <p>Browsers ignore everything before "@" — paypal.com@evil.com goes to evil.com.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Scan section ──
st.markdown("""
<div style="margin-bottom:0.5rem">
  <div class="section-label">URL Scanner</div>
  <div class="section-title">Analyze a Suspicious URL</div>
  <div class="section-sub">Paste any URL below. PhishGuard will never visit or fetch it.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="scan-card">', unsafe_allow_html=True)
st.markdown('<div class="scan-label">🔍 Enter URL to scan</div>', unsafe_allow_html=True)

url_input   = st.text_input("URL", placeholder="https://example.com/page", label_visibility="collapsed")
analyze_btn = st.button("⚡  Run Threat Analysis", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Analysis result ──
if analyze_btn:
    raw = url_input.strip()
    if not raw:
        st.markdown("""
        <div style="background:#111827;border:1px solid #374151;border-radius:10px;
                    padding:1rem 1.4rem;color:#9ca3af;font-size:0.9rem;margin-bottom:1rem;">
          ⚠️ &nbsp; Please enter a URL before running the analysis.
        </div>""", unsafe_allow_html=True)
    elif not re.match(r"https?://", raw, re.IGNORECASE):
        st.markdown("""
        <div style="background:#1a0303;border:1px solid #991b1b;border-radius:10px;
                    padding:1rem 1.4rem;color:#fca5a5;font-size:0.9rem;margin-bottom:1rem;">
          ❌ &nbsp; URL must begin with <code>http://</code> or <code>https://</code>
        </div>""", unsafe_allow_html=True)
    else:
        result = analyze_url(raw)
        risk, score = result["risk"], result["score"]

        pill_cls   = {"Low": "pill-low", "Medium": "pill-medium", "High": "pill-high"}[risk]
        result_cls = {"Low": "result-low", "Medium": "result-medium", "High": "result-high"}[risk]
        fill_cls   = {"Low": "fill-low", "Medium": "fill-medium", "High": "fill-high"}[risk]
        icon       = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}[risk]

        st.markdown(f"""
        <div class="result-card {result_cls}">
          <div class="risk-pill {pill_cls}">
            {icon} &nbsp; {risk} Risk
          </div>
          <div style="font-size:0.82rem;color:#475569;font-family:'JetBrains Mono',monospace;
                      margin-bottom:0.6rem;word-break:break-all;">
            Scanned: {raw[:90]}{'…' if len(raw) > 90 else ''}
          </div>
          <div class="score-bar-wrap">
            <div style="display:flex;justify-content:space-between;
                        font-size:0.72rem;color:#475569;margin-bottom:4px;">
              <span>Suspicion Score</span><span style="font-family:'JetBrains Mono',monospace">{score}/100</span>
            </div>
            <div class="score-bar-track">
              <div class="score-bar-fill {fill_cls}" style="width:{score}%"></div>
            </div>
          </div>
        """, unsafe_allow_html=True)

        if result["warnings"]:
            st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#ef4444;"
                        "letter-spacing:1px;text-transform:uppercase;margin-bottom:0.6rem;'>"
                        "⚠ Indicators Found</div>", unsafe_allow_html=True)
            for icon_w, title, desc in result["warnings"]:
                st.markdown(f"""
                <div class="finding finding-warn">
                  <span class="finding-icon">{icon_w}</span>
                  <div><b style="color:#f1f5f9">{title}</b><br>
                  <span style="color:#64748b">{desc}</span></div>
                </div>""", unsafe_allow_html=True)

        if result["passed"]:
            st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#22c55e;"
                        "letter-spacing:1px;text-transform:uppercase;"
                        "margin:1rem 0 0.6rem;'>✓ Checks Passed</div>", unsafe_allow_html=True)
            for icon_p, desc in result["passed"]:
                st.markdown(f"""
                <div class="finding finding-pass">
                  <span class="finding-icon">{icon_p}</span>
                  <span style="color:#94a3b8">{desc}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # close result-card

# ── Example URLs ──
st.markdown("""
<div style="margin:2.5rem 0 0.8rem">
  <div class="section-label">Test Cases</div>
  <div class="section-title">Example URLs to Try</div>
  <div class="section-sub">Copy any URL below, paste it into the scanner above.</div>
</div>
""", unsafe_allow_html=True)

examples = [
    ("Low",    "ex-low",    "https://www.github.com/security",
     "Clean domain, HTTPS, no suspicious patterns."),
    ("Medium", "ex-medium", "http://secure-login.paypal.com.update-info.xyz/verify",
     "Missing HTTPS, domain spoofing, phishing keyword."),
    ("High",   "ex-high",   "http://192.168.1.1/login?user=admin&password=confirm",
     "Raw IP, missing HTTPS, credential keywords."),
    ("High",   "ex-high",   "https://bit.ly/3xAb12c@evil-phish.com/banking",
     "URL shortener + @ redirection trick + banking keyword."),
]
for risk_lbl, css_cls, url, note in examples:
    st.markdown(f"""
    <div class="example-block">
      <h4 class="{css_cls}">{risk_lbl} Risk Example</h4>
      <div class="url-code">{url}</div>
      <div style="font-size:0.75rem;color:#475569;margin-top:0.3rem">{note}</div>
    </div>""", unsafe_allow_html=True)

# ── Protection tips ──
st.markdown("""
<div style="margin:2.5rem 0 0.8rem">
  <div class="section-label">Stay Protected</div>
  <div class="section-title">5 Rules for Handling Suspicious Links</div>
</div>
<div class="tips-grid">
  <div class="tip-card">
    <div class="tip-num">01</div>
    <h4>Hover Before Clicking</h4>
    <p>Hold your cursor over any link to preview its real destination in the browser status bar before clicking.</p>
  </div>
  <div class="tip-card">
    <div class="tip-num">02</div>
    <h4>Inspect the Domain</h4>
    <p>Watch for look-alike domains: <code style="color:#7dd3fc">paypa1.com</code> uses a "1" instead of "l".</p>
  </div>
  <div class="tip-card">
    <div class="tip-num">03</div>
    <h4>HTTPS ≠ Safe</h4>
    <p>HTTPS only encrypts data in transit. Phishing sites also use HTTPS — it is not a trust indicator.</p>
  </div>
  <div class="tip-card">
    <div class="tip-num">04</div>
    <h4>Scan with VirusTotal</h4>
    <p>Paste suspicious links into <a href="https://www.virustotal.com" target="_blank" style="color:#60a5fa">virustotal.com</a> or Google Safe Browsing for a deeper check.</p>
  </div>
  <div class="tip-card">
    <div class="tip-num">05</div>
    <h4>Type, Don't Click</h4>
    <p>When in doubt, manually type the website address directly into your browser's address bar.</p>
  </div>
  <div class="tip-card">
    <div class="tip-num">06</div>
    <h4>Enable 2FA Everywhere</h4>
    <p>Even if credentials are stolen via phishing, two-factor authentication blocks unauthorized access.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Disclaimer ──
st.markdown("""
<div class="disclaimer-bar">
  ⚠️ &nbsp; <b>Educational Estimate Only.</b> &nbsp;
  PhishGuard inspects URL text patterns only. It does <b>not</b> visit, fetch, or verify any website content.<br>
  This tool <b>cannot guarantee</b> a URL is safe or malicious. Always use professional security tools for real threat detection.
</div>
""", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="pg-footer">
  PHISHGUARD &nbsp;·&nbsp; EDUCATIONAL CYBERSECURITY TOOL &nbsp;·&nbsp; BUILT WITH STREAMLIT
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-wrap
