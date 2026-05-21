import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.optimize import minimize
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Simulación financiera",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
# ESTILOS — TERMINAL FINANCIERO
# ═══════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;600;700;800&family=Barlow:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

:root{
    --bg:#050b14; --sf:#091120; --s2:#0d1829; --s3:#111f35;
    --bd:#1a2744; --bh:#234070;
    --cy:#00c8ff; --cd:rgba(0,200,255,.13); --cg:0 0 22px rgba(0,200,255,.2);
    --gn:#00e676; --gd:rgba(0,230,118,.11);
    --am:#ffab00; --ad:rgba(255,171,0,.11);
    --rd:#ff4757; --rdd:rgba(255,71,87,.11);
    --tx:#cdd9f0; --ts:#6882a8; --td:#2e4166;
    --fh:'Barlow Condensed',sans-serif;
    --fb:'Barlow',sans-serif;
    --fm:'JetBrains Mono',monospace;
}

html,body,[class*="css"],.stApp{
    background-color:var(--bg)!important;
    font-family:var(--fb);color:var(--tx);
}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bh);border-radius:3px}

section[data-testid="stSidebar"]{
    background:var(--sf)!important;
    border-right:1px solid var(--bd)!important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaption p{
    font-family:var(--fm)!important;font-size:11px!important;color:var(--ts)!important;
}

.stButton>button{
    background:linear-gradient(135deg,#001f30,#003a55)!important;
    color:var(--cy)!important;
    border:1px solid rgba(0,200,255,.45)!important;
    font-family:var(--fh)!important;font-size:13px!important;
    font-weight:700!important;letter-spacing:3px!important;
    text-transform:uppercase!important;border-radius:2px!important;
    box-shadow:0 0 14px rgba(0,200,255,.1)!important;
    transition:all .2s ease!important;
}
.stButton>button:hover{
    box-shadow:0 0 28px rgba(0,200,255,.38)!important;
    transform:translateY(-1px)!important;
}

[data-testid="stMetric"]{
    background:var(--s2)!important;
    border:1px solid var(--bd)!important;
    border-top:2px solid var(--cy)!important;
    border-radius:3px!important;padding:14px 16px!important;
    transition:box-shadow .2s;
}
[data-testid="stMetric"]:hover{box-shadow:var(--cg)!important}
[data-testid="stMetricLabel"]>div{
    font-family:var(--fm)!important;font-size:9px!important;
    color:var(--ts)!important;text-transform:uppercase!important;letter-spacing:1.5px!important;
}
[data-testid="stMetricValue"]>div{
    font-family:var(--fm)!important;font-size:20px!important;
    color:var(--tx)!important;font-weight:600!important;
}

.stTabs [data-baseweb="tab-list"]{
    background:var(--sf)!important;border-bottom:1px solid var(--bd)!important;gap:0!important;
}
.stTabs [data-baseweb="tab"]{
    font-family:var(--fm)!important;font-size:10px!important;color:var(--ts)!important;
    text-transform:uppercase!important;letter-spacing:1.5px!important;
    padding:10px 20px!important;border-bottom:2px solid transparent!important;
    background:transparent!important;
}
.stTabs [aria-selected="true"]{
    color:var(--cy)!important;border-bottom-color:var(--cy)!important;
    background:var(--cd)!important;
}

.stTextInput input{
    background:var(--s3)!important;border:1px solid var(--bd)!important;
    color:var(--tx)!important;font-family:var(--fm)!important;
    font-size:12px!important;border-radius:2px!important;
}
.stTextInput input:focus{
    border-color:var(--cy)!important;
    box-shadow:0 0 0 1px rgba(0,200,255,.3)!important;
}

.stProgress>div>div{background:linear-gradient(90deg,var(--cy),var(--gn))!important;}

.stMarkdown table{width:100%;border-collapse:collapse;font-family:var(--fm);font-size:12px}
.stMarkdown th{background:var(--s3);color:var(--cy);font-size:10px;
    letter-spacing:2px;text-transform:uppercase;padding:8px 12px;
    border-bottom:1px solid var(--bh)}
.stMarkdown td{padding:8px 12px;border-bottom:1px solid var(--bd);color:var(--ts)}
.stMarkdown tr:hover td{background:var(--s3);color:var(--tx)}

details>summary{
    font-family:var(--fm)!important;font-size:10px!important;
    letter-spacing:1px!important;color:var(--ts)!important;
    background:var(--s2)!important;border-radius:3px!important;
    padding:10px 16px!important;
}

#MainMenu{visibility:hidden}footer{visibility:hidden}
header[data-testid="stHeader"]{
    background:rgba(5,11,20,.95)!important;
    border-bottom:1px solid var(--bd)!important;
    backdrop-filter:blur(8px)!important;
}

/* ── Banner ─────────────────────── */
.banner{
    background:linear-gradient(145deg,#050b14 0%,#071628 55%,#050b14 100%);
    border:1px solid var(--bd);border-left:3px solid var(--cy);
    border-radius:3px;padding:30px 38px 24px;position:relative;overflow:hidden;
}
.banner::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,var(--cy) 35%,transparent)}
.b-live{position:absolute;top:14px;right:18px;font-family:var(--fm);
    font-size:9px;color:var(--gn);letter-spacing:2px;
    border:1px solid rgba(0,230,118,.4);padding:2px 8px;border-radius:2px;
    animation:blk 1.8s ease-in-out infinite}
@keyframes blk{0%,100%{opacity:1}50%{opacity:.3}}
.b-code{font-family:var(--fm);font-size:9px;color:var(--ts);
    letter-spacing:3px;text-transform:uppercase;margin-bottom:6px}
.banner h1{font-family:var(--fh)!important;font-size:50px!important;
    font-weight:800!important;color:#fff!important;letter-spacing:6px!important;
    text-transform:uppercase!important;margin:0 0 4px!important;line-height:1!important}
.b-sub{font-family:var(--fm);font-size:10px;color:var(--cy);
    letter-spacing:3px;text-transform:uppercase;margin-bottom:10px}
.b-tag{font-family:var(--fb);font-size:13px;color:var(--ts);font-style:italic}

/* ── Ticker tape ────────────────── */
.tkr{background:var(--sf);border:1px solid var(--bd);
    overflow:hidden;padding:5px 0;margin:12px 0 28px}
.tkr-t{display:flex;white-space:nowrap;animation:rn 22s linear infinite;
    font-family:var(--fm);font-size:11px}
@keyframes rn{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.ti{display:inline-flex;align-items:center;gap:8px;
    padding:2px 24px;border-right:1px solid var(--bd)}
.tsm{color:var(--cy);font-weight:600;letter-spacing:1px}
.tpx{color:var(--tx)}
.tup{color:var(--gn)}
.tdn{color:var(--rd)}

/* ── Section header ─────────────── */
.sh{display:flex;align-items:center;gap:12px;margin:36px 0 18px;
    padding-bottom:10px;border-bottom:1px solid var(--bd)}
.sh-n{font-family:var(--fm);font-size:10px;color:var(--cy);
    background:var(--cd);border:1px solid var(--bh);
    padding:3px 9px;border-radius:2px;letter-spacing:2px}
.sh-t{font-family:var(--fh);font-size:22px;font-weight:700;
    color:var(--tx);text-transform:uppercase;letter-spacing:3px}
.sh-s{margin-left:auto;font-family:var(--fm);font-size:9px;
    color:var(--td);letter-spacing:2px;text-transform:uppercase}

/* ── Sub-header ─────────────────── */
.sub-h{font-family:var(--fh);font-size:14px;font-weight:700;
    color:var(--ts);letter-spacing:3px;text-transform:uppercase;
    margin:22px 0 10px;border-left:2px solid var(--cy);padding-left:10px}

/* ── Badge ──────────────────────── */
.bdg{display:inline-block;font-family:var(--fm);font-size:10px;
    font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
    padding:2px 9px;border-radius:2px}
.b-g{background:rgba(0,200,255,.16);border:1px solid var(--cy);color:var(--cy)}
.b-h{background:rgba(255,171,0,.16);border:1px solid var(--am);color:var(--am)}
.b-m{background:rgba(255,71,87,.16);border:1px solid var(--rd);color:var(--rd)}

/* ── Info panel ─────────────────── */
.ip{background:var(--sf);border:1px solid var(--bd);
    border-left:3px solid var(--cy);border-radius:2px;
    padding:14px 18px;font-family:var(--fm);font-size:11px;
    color:var(--ts);line-height:1.75;margin:10px 0}
.ip.g{border-left-color:var(--gn)}
.ip.a{border-left-color:var(--am)}
.ip.r{border-left-color:var(--rd)}

/* ── Decision card ──────────────── */
.dc{border-radius:3px;padding:16px 20px;margin:6px 0}
.dc.ep{background:rgba(0,230,118,.05);border:1px solid rgba(0,230,118,.22);
    border-left:3px solid var(--gn)}
.dc.ab{background:rgba(255,71,87,.05);border:1px solid rgba(255,71,87,.22);
    border-left:3px solid var(--rd)}
.dc.hl{background:rgba(0,200,255,.05);border:1px solid rgba(0,200,255,.22);
    border-left:3px solid var(--cy)}
.dc-h{font-family:var(--fh);font-size:15px;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}
.dc.ep .dc-h{color:var(--gn)}
.dc.ab .dc-h{color:var(--rd)}
.dc.hl .dc-h{color:var(--cy)}
.dc-b{font-family:var(--fm);font-size:11px;color:var(--ts);line-height:1.65}

/* ── ENPV value card ────────────── */
.vc{background:var(--s2);border:1px solid var(--bd);
    border-top:2px solid var(--gn);border-radius:4px;
    padding:22px 24px;text-align:center;transition:box-shadow .2s}
.vc:hover{box-shadow:var(--cg)}
.vc.dim{border-top-color:var(--ts)}
.vc.cy{border-top-color:var(--cy)}
.vc-lb{font-family:var(--fm);font-size:9px;color:var(--ts);
    text-transform:uppercase;letter-spacing:2px;margin-bottom:8px}
.vc-v{font-family:var(--fh);font-size:38px;font-weight:800;
    color:var(--gn);letter-spacing:2px;line-height:1;margin-bottom:5px}
.vc-v.dim{color:var(--ts)}
.vc-v.cy{color:var(--cy)}
.vc-s{font-family:var(--fm);font-size:10px;color:var(--td)}

/* ── Ticker row ─────────────────── */
.tk-row{display:flex;align-items:center;gap:10px;margin:10px 0 18px}
.tk-sym{font-family:var(--fh);font-size:20px;font-weight:700;
    color:var(--tx);letter-spacing:2px}
.tk-sep{font-family:var(--fm);font-size:10px;color:var(--td)}
.tk-lbl{font-family:var(--fm);font-size:10px;color:var(--ts)}

/* ── Footer ─────────────────────── */
.ftr{background:var(--sf);border-top:1px solid var(--bd);
    padding:12px 24px;font-family:var(--fm);font-size:9px;color:var(--td);
    display:flex;justify-content:space-between;
    letter-spacing:1.5px;text-transform:uppercase;margin-top:44px}
</style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════
N_SIMS = 1000
DT     = 1 / 252
COLORS = {
    "GBM":    "#00c8ff",
    "Heston": "#ffab00",
    "Merton": "#ff4757",
    "Real":   "#00e676",
}
BAND_O = {
    "GBM":    "rgba(0,200,255,.07)",
    "Heston": "rgba(255,171,0,.07)",
    "Merton": "rgba(255,71,87,.07)",
}
BAND_I = {
    "GBM":    "rgba(0,200,255,.16)",
    "Heston": "rgba(255,171,0,.16)",
    "Merton": "rgba(255,71,87,.16)",
}
LINE_C = ["#00c8ff", "#ffab00", "#ff4757", "#00e676"]
FILL_C = ["rgba(0,200,255,.05)", "rgba(255,171,0,.05)",
          "rgba(255,71,87,.05)", "rgba(0,230,118,.05)"]
R_LIBRE  = 0.0525
N_PER_OP = 4
DT_OP    = 1 / 12
CAP_BASE = 100_000
CAP_EXP  = 50_000
SALVAGE  = 0.92
SECTOR_MAP = {
    "AAPL":"Tecnología","MSFT":"Tecnología","NVDA":"Tecnología",
    "AMZN":"Consumo",   "TSLA":"Consumo",
    "JPM": "Financiero","BAC": "Financiero",
    "JNJ": "Salud",     "PFE": "Salud",
    "XOM": "Energía",   "CVX": "Energía",
    "GE":  "Industrial","CAT": "Industrial",
}


# ═══════════════════════════════════════════════════════
# HELPERS DE LAYOUT
# ═══════════════════════════════════════════════════════
def H(n, title, sub=""):
    s = f'<span class="sh-s">{sub}</span>' if sub else ""
    return (f'<div class="sh"><span class="sh-n">{n:02d}</span>'
            f'<span class="sh-t">{title}</span>{s}</div>')

def badge(m):
    cls = {"GBM": "b-g", "Heston": "b-h", "Merton": "b-m"}.get(m, "b-g")
    return f'<span class="bdg {cls}">{m}</span>'

def ip_html(text, color=""):
    return f'<div class="ip {color}">{text}</div>'

def dc_html(kind, title, body):
    cls = {"expand": "ep", "abandon": "ab", "hold": "hl"}.get(kind, "hl")
    return (f'<div class="dc {cls}">'
            f'<div class="dc-h">{title}</div>'
            f'<div class="dc-b">{body}</div>'
            f'</div>')

def vc_html(label, value, sub, color=""):
    return (f'<div class="vc {color}">'
            f'<div class="vc-lb">{label}</div>'
            f'<div class="vc-v {color}">{value}</div>'
            f'<div class="vc-s">{sub}</div>'
            f'</div>')

def sub_h(title):
    return f'<div class="sub-h">{title}</div>'

def ticker_html(datos_d):
    items = []
    for t, df in datos_d.items():
        cl  = df["Close"].squeeze()
        cur = float(cl.iloc[-1])
        prv = float(cl.iloc[-2])
        pct = (cur - prv) / prv * 100
        cls = "tup" if pct >= 0 else "tdn"
        arr = "▲" if pct >= 0 else "▼"
        items.append(
            f'<span class="ti">'
            f'<span class="tsm">{t}</span>'
            f'<span class="tpx">${cur:.2f}</span>'
            f'<span class="{cls}">{arr} {pct:+.2f}%</span>'
            f'</span>'
        )
    body = "".join(items) * 4
    return f'<div class="tkr"><div class="tkr-t">{body}</div></div>'

def _hex_rgba(hx, a):
    hx = hx.lstrip('#')
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

def _pl(title="", h=360):
    """Shared Plotly dark-terminal layout."""
    return dict(
        title=dict(text=title,
                   font=dict(family="Barlow Condensed", size=14, color="#4a6a98"),
                   x=0.01),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(9,17,32,.97)",
        font=dict(family="JetBrains Mono", size=9, color="#6882a8"),
        height=h,
        margin=dict(l=20, r=14, t=44, b=20),
        xaxis=dict(gridcolor="#1a2744", zeroline=False, linecolor="#1a2744",
                   tickfont=dict(size=8, color="#3a5280")),
        yaxis=dict(gridcolor="#1a2744", zeroline=False, linecolor="#1a2744",
                   tickfont=dict(size=8, color="#3a5280")),
        legend=dict(orientation="h", y=-0.22, bgcolor="rgba(0,0,0,0)",
                    font=dict(size=9, color="#6882a8")),
        hoverlabel=dict(bgcolor="#0d1829", bordercolor="#1a2744",
                        font=dict(family="JetBrains Mono", size=11, color="#cdd9f0")),
    )


# ═══════════════════════════════════════════════════════
# FUNCIONES DE DATOS
# ═══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def descargar_datos(tickers: list, periodo: str = "2y") -> dict:
    import time
    yf.set_tz_cache_location("/tmp/yfinance_cache")
    datos = {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            df = tk.history(period=periodo, auto_adjust=True)
            if df.empty:
                df = yf.download(
                    t, period=periodo,
                    auto_adjust=True,
                    progress=False,
                    repair=True
                )
            if len(df) > 50:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df = df[["Close"]].dropna()
                df.index = pd.to_datetime(df.index)
                datos[t] = df
        except Exception:
            pass
        time.sleep(1)  # pausa entre tickers
    return datos

def calcular_retornos(precios: pd.DataFrame) -> pd.Series:
    close = precios["Close"].squeeze()
    return np.log(close / close.shift(1)).dropna()

# MODELO 1 — GBM
# ═══════════════════════════════════════════════════════
def estimar_gbm(retornos):
    return retornos.mean() / DT, retornos.std() / np.sqrt(DT)

def simular_gbm(S0, mu, sigma, T_dias, n_sims=N_SIMS):
    paths = np.zeros((T_dias, n_sims))
    paths[0] = S0
    for t in range(1, T_dias):
        Z = np.random.standard_normal(n_sims)
        paths[t] = paths[t-1] * np.exp((mu - 0.5*sigma**2)*DT + sigma*np.sqrt(DT)*Z)
    return paths


# ═══════════════════════════════════════════════════════
# MODELO 2 — HESTON
# ═══════════════════════════════════════════════════════
def estimar_heston(retornos):
    sigma = retornos.std() / np.sqrt(DT)
    v0    = sigma**2
    return retornos.mean() / DT, v0, 2.0, v0, 0.3, -0.5

def simular_heston(S0, mu, v0, kappa, theta, xi, rho, T_dias, n_sims=N_SIMS):
    paths = np.zeros((T_dias, n_sims))
    vt    = np.zeros((T_dias, n_sims))
    paths[0] = S0; vt[0] = v0
    for t in range(1, T_dias):
        Z1 = np.random.standard_normal(n_sims)
        Z2 = rho*Z1 + np.sqrt(1 - rho**2)*np.random.standard_normal(n_sims)
        vp = np.maximum(vt[t-1], 0)
        vt[t]    = np.maximum(vp + kappa*(theta - vp)*DT + xi*np.sqrt(vp*DT)*Z2, 1e-8)
        paths[t] = paths[t-1] * np.exp((mu - 0.5*vp)*DT + np.sqrt(vp*DT)*Z1)
    return paths


# ═══════════════════════════════════════════════════════
# MODELO 3 — MERTON JUMP-DIFFUSION
# ═══════════════════════════════════════════════════════
def estimar_merton(retornos):
    mu    = retornos.mean() / DT
    sigma = retornos.std()  / np.sqrt(DT)
    saltos = retornos[retornos.abs() > 3 * retornos.std()]
    lam   = len(saltos) / (len(retornos) * DT)
    mu_j  = saltos.mean() if len(saltos) > 0 else 0.0
    sig_j = saltos.std()  if len(saltos) > 1 else 0.01
    return mu, sigma, lam, mu_j, sig_j

def simular_merton(S0, mu, sigma, lam, mu_j, sig_j, T_dias, n_sims=N_SIMS):
    paths = np.zeros((T_dias, n_sims))
    paths[0] = S0
    for t in range(1, T_dias):
        Z  = np.random.standard_normal(n_sims)
        Nt = np.random.poisson(lam * DT, n_sims)
        Y  = np.random.normal(mu_j, sig_j, n_sims)
        paths[t] = paths[t-1] * np.exp((mu - 0.5*sigma**2)*DT + sigma*np.sqrt(DT)*Z + Y*Nt)
    return paths


# ═══════════════════════════════════════════════════════
# BACKTESTING
# ═══════════════════════════════════════════════════════
def calcular_rmse(observado, simulado_promedio):
    n = min(len(observado), len(simulado_promedio))
    return np.sqrt(np.mean((observado[:n] - simulado_promedio[:n])**2))

def backtest_accion(ticker, precios):
    ret   = calcular_retornos(precios)
    px    = precios["Close"].squeeze().values
    T_te  = 21
    T_tr  = len(px) - T_te
    r_tr  = ret.iloc[:T_tr]
    te    = px[T_tr:]
    S0    = px[T_tr - 1]

    mu_g, sig_g = estimar_gbm(r_tr)
    p_g  = simular_gbm(S0, mu_g, sig_g, T_te + 1)
    rm_g = calcular_rmse(te, p_g[1:].mean(axis=1))

    mu_h, v0, kappa, theta, xi, rho = estimar_heston(r_tr)
    p_h  = simular_heston(S0, mu_h, v0, kappa, theta, xi, rho, T_te + 1)
    rm_h = calcular_rmse(te, p_h[1:].mean(axis=1))

    mu_m, sig_m, lam, mu_j, sig_j = estimar_merton(r_tr)
    p_m  = simular_merton(S0, mu_m, sig_m, lam, mu_j, sig_j, T_te + 1)
    rm_m = calcular_rmse(te, p_m[1:].mean(axis=1))

    rmses = {"GBM": rm_g, "Heston": rm_h, "Merton": rm_m}
    return {
        "rmses": rmses,
        "ganador": min(rmses, key=rmses.get),
        "test_precios": te,
        "pred_gbm":    p_g[1:].mean(axis=1),
        "pred_heston": p_h[1:].mean(axis=1),
        "pred_merton": p_m[1:].mean(axis=1),
        "params": {
            "gbm":    (mu_g, sig_g),
            "heston": (mu_h, v0, kappa, theta, xi, rho),
            "merton": (mu_m, sig_m, lam, mu_j, sig_j),
        },
        "T_train": T_tr,
    }


# ═══════════════════════════════════════════════════════
# PROYECCIÓN A 1 MES
# ═══════════════════════════════════════════════════════
def proyectar_accion(ticker, precios, bt):
    S0 = float(precios["Close"].squeeze().iloc[-1])
    g  = bt["ganador"]
    p  = bt["params"]
    T  = 21
    if g == "GBM":
        mu, sig = p["gbm"]
        paths = simular_gbm(S0, mu, sig, T + 1)
    elif g == "Heston":
        mu, v0, kappa, theta, xi, rho = p["heston"]
        paths = simular_heston(S0, mu, v0, kappa, theta, xi, rho, T + 1)
    else:
        mu, sig, lam, mu_j, sig_j = p["merton"]
        paths = simular_merton(S0, mu, sig, lam, mu_j, sig_j, T + 1)
    fin = paths[-1]
    return {
        "S0": S0,
        "p5":  float(np.percentile(fin,  5)),
        "p50": float(np.percentile(fin, 50)),
        "p95": float(np.percentile(fin, 95)),
        "paths": paths,
        "ganador": g,
    }


# ═══════════════════════════════════════════════════════
# GRÁFICOS PLOTLY — REDISEÑADOS
# ═══════════════════════════════════════════════════════
def fig_precios_historicos(datos, tickers):
    fig = go.Figure()
    for i, t in enumerate(tickers):
        if t not in datos:
            continue
        df  = datos[t]
        col = LINE_C[i % 4]
        fc  = FILL_C[i % 4]
        fig.add_trace(go.Scatter(
            x=df.index, y=df["Close"].squeeze(), name=t,
            line=dict(color=col, width=1.5),
            fill="tozeroy", fillcolor=fc,
            hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br><b>$%{{y:.2f}}</b><extra></extra>",
        ))
    L = _pl("Precio histórico de cierre — 2 años", 420)
    L["xaxis"]["showgrid"] = False
    fig.update_layout(**L)
    return fig

def fig_retornos(retornos, ticker):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=retornos.index, y=retornos.values,
        marker_color=np.where(retornos.values >= 0, "#00e676", "#ff4757"),
        name="Retorno log",
        hovertemplate="%{x|%d %b %Y}<br><b>%{y:.4f}</b><extra></extra>",
    ))
    L = _pl(f"Retornos log — {ticker}", 310)
    L["yaxis"]["tickformat"] = ".2%"
    L["xaxis"]["showgrid"] = False
    fig.update_layout(**L)
    return fig

def fig_simulaciones(paths, precios_test, titulo, color, S0_idx, precios_full):
    fig     = go.Figure()
    band_fc = _hex_rgba(color, 0.10)
    for i in range(min(80, paths.shape[1])):
        fig.add_trace(go.Scatter(
            y=paths[:, i], mode="lines",
            line=dict(color=color, width=0.3), opacity=0.10,
            showlegend=False, hoverinfo="skip",
        ))
    p5   = np.percentile(paths,  5, axis=1)
    p95  = np.percentile(paths, 95, axis=1)
    dias = np.arange(paths.shape[0])
    fig.add_trace(go.Scatter(
        x=np.concatenate([dias, dias[::-1]]),
        y=np.concatenate([p95, p5[::-1]]),
        fill="toself", fillcolor=band_fc,
        line=dict(color="rgba(0,0,0,0)"),
        name="Banda 5–95%", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        y=paths.mean(axis=1), mode="lines",
        line=dict(color=color, width=2.2),
        name="Promedio",
        hovertemplate="Día %{x}<br>$%{y:.2f}<extra></extra>",
    ))
    if precios_test is not None:
        fig.add_trace(go.Scatter(
            y=np.concatenate([[paths[0, 0]], precios_test]),
            mode="lines",
            line=dict(color="#00e676", width=1.8, dash="dot"),
            name="Real",
            hovertemplate="Día %{x}<br>$%{y:.2f}<extra></extra>",
        ))
    fig.update_layout(**_pl(titulo, 340))
    return fig

def fig_rmse_comparacion(tabla_rmse):
    fig = go.Figure()
    for m, c in [("GBM", "#00c8ff"), ("Heston", "#ffab00"), ("Merton", "#ff4757")]:
        fig.add_trace(go.Bar(
            name=m, x=tabla_rmse["Acción"].tolist(),
            y=tabla_rmse[f"RMSE {m}"].values,
            marker=dict(color=c, opacity=0.82, line=dict(width=0)),
            hovertemplate=f"<b>{m}</b><br>%{{x}}<br>RMSE $%{{y:.4f}}<extra></extra>",
        ))
    L = _pl("RMSE por modelo y acción — backtesting 21 días", 390)
    L["barmode"]      = "group"
    L["bargap"]       = 0.25
    L["bargroupgap"]  = 0.06
    fig.update_layout(**L)
    return fig

def fig_proyeccion(proy, ticker):
    paths = proy["paths"]
    col   = COLORS.get(proy["ganador"], "#00c8ff")
    bo    = BAND_O.get(proy["ganador"], "rgba(0,200,255,.07)")
    bi    = BAND_I.get(proy["ganador"], "rgba(0,200,255,.16)")
    dias  = np.arange(paths.shape[0])
    p5, p25, p50, p75, p95 = [np.percentile(paths, q, axis=1) for q in [5, 25, 50, 75, 95]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.concatenate([dias, dias[::-1]]),
        y=np.concatenate([p95, p5[::-1]]),
        fill="toself", fillcolor=bo,
        line=dict(color="rgba(0,0,0,0)"),
        name="P5–P95", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=np.concatenate([dias, dias[::-1]]),
        y=np.concatenate([p75, p25[::-1]]),
        fill="toself", fillcolor=bi,
        line=dict(color="rgba(0,0,0,0)"),
        name="P25–P75", hoverinfo="skip",
    ))
    for i in range(min(50, paths.shape[1])):
        fig.add_trace(go.Scatter(
            y=paths[:, i], mode="lines",
            line=dict(color=col, width=0.3), opacity=0.07,
            showlegend=False, hoverinfo="skip",
        ))
    fig.add_trace(go.Scatter(
        y=p50, mode="lines",
        line=dict(color=col, width=2.5),
        name="Mediana P50",
        hovertemplate="Día %{x}<br>$%{y:.2f}<extra></extra>",
    ))
    fig.add_hline(
        y=proy["S0"], line_dash="dot", line_color="#2e4166", line_width=1,
        annotation_text=f"  S₀ ${proy['S0']:.2f}",
        annotation_font=dict(family="JetBrains Mono", size=9, color="#6882a8"),
    )
    L = _pl(f"Proyección 21 días — {ticker} · {proy['ganador']}", 370)
    L["xaxis"]["title"] = dict(text="Día bursátil", font=dict(size=9, color="#3a5280"))
    L["yaxis"]["title"] = dict(text="USD",           font=dict(size=9, color="#3a5280"))
    fig.update_layout(**L)
    return fig


# ═══════════════════════════════════════════════════════
# RECOMENDACIÓN EJECUTIVA
# ═══════════════════════════════════════════════════════
def generar_recomendacion(tabla_proy, tabla_rmse):
    mejor_upside = max(tabla_proy, key=lambda r: (r["p50"] - r["S0"]) / r["S0"])
    menor_riesgo = min(tabla_proy, key=lambda r: r["p95"] - r["p5"])
    mayor_riesgo = max(tabla_proy, key=lambda r: r["p95"] - r["p5"])
    upsides = [(r["p50"] - r["S0"]) / r["S0"] for r in tabla_proy]
    rangos  = [r["p95"] - r["p5"]             for r in tabla_proy]
    scores  = [u / (ra + 1e-9) for u, ra in zip(upsides, rangos)]
    total   = sum(max(s, 0) for s in scores) or 1
    pesos   = [max(s, 0) / total * 100 for s in scores]
    return {
        "mejor_upside": mejor_upside["ticker"],
        "menor_riesgo": menor_riesgo["ticker"],
        "mayor_riesgo": mayor_riesgo["ticker"],
        "pesos": {r["ticker"]: round(p, 1) for r, p in zip(tabla_proy, pesos)},
    }


# ═══════════════════════════════════════════════════════
# OPCIONES REALES — FUNCIONES
# ═══════════════════════════════════════════════════════
def _vol_mu_portfolio(tickers_ok, resultados_bt, pesos_dict):
    sigma_p = mu_p = 0.0
    for t in tickers_ok:
        bt = resultados_bt[t]
        g  = bt["ganador"]
        if g == "GBM":
            mu, sig = bt["params"]["gbm"]
        elif g == "Heston":
            mu, v0, *_ = bt["params"]["heston"]
            sig = np.sqrt(v0)
        else:
            mu, sig, *_ = bt["params"]["merton"]
        w = pesos_dict.get(t, 100 / len(tickers_ok)) / 100
        sigma_p += w * sig
        mu_p    += w * mu
    return sigma_p, mu_p

def _arbol_binomial(V0, sigma, r=R_LIBRE, dt=DT_OP, n=N_PER_OP):
    u    = np.exp(sigma * np.sqrt(dt))
    d    = 1.0 / u
    p_rn = float(np.clip((np.exp(r * dt) - d) / (u - d), 1e-4, 1 - 1e-4))
    A    = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(i + 1):
            A[i, j] = V0 * (u**j) * (d**(i - j))
    return A, u, d, p_rn

def _backward_opciones(A, p, r=R_LIBRE, dt=DT_OP,
                        cap_exp=CAP_EXP, salvage=SALVAGE, n=N_PER_OP):
    disc = np.exp(-r * dt)
    V    = np.zeros((n + 1, n + 1))
    D    = np.full((n + 1, n + 1), "", dtype=object)
    for j in range(n + 1):
        Vn   = A[n, j]
        opts = {"Continuar": Vn, "Expandir": 1.5*Vn - cap_exp, "Abandonar": Vn*salvage}
        best = max(opts, key=opts.get)
        V[n, j] = opts[best]; D[n, j] = best
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            Vij  = A[i, j]
            Vc   = disc * (p * V[i+1, j+1] + (1-p) * V[i+1, j])
            opts = {"Continuar": Vc, "Expandir": 1.5*Vij - cap_exp, "Abandonar": Vij*salvage}
            best = max(opts, key=opts.get)
            V[i, j] = opts[best]; D[i, j] = best
    return V, D

def _backward_pasivo(A, p, r=R_LIBRE, dt=DT_OP, n=N_PER_OP):
    disc = np.exp(-r * dt)
    V    = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        V[n, j] = A[n, j]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            V[i, j] = disc * (p * V[i+1, j+1] + (1-p) * V[i+1, j])
    return V

def _fig_arbol_opciones(A, V_opc, D_opc, n=N_PER_OP):
    COL   = {"Continuar": "#00c8ff", "Expandir": "#00e676", "Abandonar": "#ff4757"}
    fig   = go.Figure()
    shown = set()
    for i in range(n):
        for j in range(i + 1):
            x0, y0 = i, j - i / 2
            for dj in (1, 0):
                xi, yi = i + 1, (j + dj) - (i + 1) / 2
                fig.add_trace(go.Scatter(
                    x=[x0, xi], y=[y0, yi], mode="lines",
                    line=dict(color="#1a2744", width=1.5),
                    showlegend=False, hoverinfo="skip",
                ))
    for i in range(n + 1):
        for j in range(i + 1):
            dec = D_opc[i, j]; Vp = A[i, j]; Vo = V_opc[i, j]
            col = COL.get(dec, "#9ca3af"); yn = j - i / 2
            sl  = dec not in shown; shown.add(dec)
            fig.add_trace(go.Scatter(
                x=[i], y=[yn], mode="markers",
                marker=dict(size=54, color=col, opacity=0.85,
                            line=dict(color="#050b14", width=2)),
                name=dec, legendgroup=dec, showlegend=sl,
                hovertemplate=(
                    f"<b>Mes {i} · {dec}</b><br>"
                    f"V portafolio: ${Vp:,.0f}<br>"
                    f"ENPV nodo:    ${Vo:,.0f}<extra></extra>"
                ),
            ))
            fig.add_annotation(
                x=i, y=yn, showarrow=False,
                text=(f"<b>${Vp/1e3:.1f}k</b><br>"
                      f"<span style='font-size:8px;opacity:.7'>{dec[:3].upper()}</span>"),
                font=dict(size=9, color="#f0f0f0", family="JetBrains Mono"),
            )
    L = _pl("Árbol Binomial CRR — Opciones Reales Americanas", 530)
    L["xaxis"].update(
        title="Mes", tickvals=list(range(n + 1)),
        ticktext=[f"Mes {i}" for i in range(n + 1)],
        showgrid=False, zeroline=False,
    )
    L["yaxis"].update(showgrid=False, zeroline=False, showticklabels=False)
    L["legend"].update(orientation="h", y=-0.08)
    fig.update_layout(**L)
    return fig


# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 4px 14px;border-bottom:1px solid #1a2744;margin-bottom:18px'>
        <div style='font-family:JetBrains Mono,monospace;font-size:9px;
                    color:#2e4166;letter-spacing:3px;text-transform:uppercase;
                    margin-bottom:5px'>TERMINAL · CONFIG</div>
        <div style='font-family:Barlow Condensed,sans-serif;font-size:22px;
                    font-weight:700;color:#cdd9f0;letter-spacing:2px'>
            ⚙ PARÁMETROS
        </div>
    </div>
    """, unsafe_allow_html=True)

    acciones_default = ["AAPL", "JNJ", "XOM", "TSLA"]
    input_tickers = st.text_input(
        "TICKERS (separados por coma)",
        value=", ".join(acciones_default),
        help="Yahoo Finance tickers — máximo 4",
    )
    tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()][:4]

    n_sims = st.slider("SIMULACIONES MC", 500, 2000, 1000, step=100)
    N_SIMS = n_sims

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    correr = st.button("▶ EJECUTAR ANÁLISIS", use_container_width=True, type="primary")

    st.markdown("""
    <div style='margin-top:22px;padding-top:14px;border-top:1px solid #1a2744;
                font-family:JetBrains Mono,monospace;font-size:9px;color:#2e4166;
                letter-spacing:1px;line-height:1.9'>
        UNIVERSIDAD EXTERNADO DE COLOMBIA<br>
        VALORACIÓN DE ACTIVOS · 2025<br>
        GBM · HESTON · MERTON · CRR
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# BANNER PRINCIPAL
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="banner">
    <span class="b-live">● LIVE</span>
    <div class="b-code">MESA DE DINERO · TERMINAL DE RIESGO CUANTITATIVO · v2.0</div>
    <h1>Proyecto de Simulación Financiera</h1>
    <div class="b-sub">GBM · Heston · Merton Jump-Diffusion · Opciones Reales · Árbol Binomial CRR</div>
    <div class="b-tag">El futuro no se predice, se simula — y se decide con opciones reales.</div>
</div>
""", unsafe_allow_html=True)

if not correr:
    st.markdown(ip_html(
        "👈 &nbsp; Configura los tickers en el panel izquierdo y presiona "
        "<strong style='color:#00c8ff'>▶ EJECUTAR ANÁLISIS</strong>",
    ), unsafe_allow_html=True)
    st.stop()

if len(tickers) < 1:
    st.error("Ingresa al menos 1 ticker válido.")
    st.stop()


# ═══════════════════════════════════════════════════════
# DESCARGA DE DATOS
# ═══════════════════════════════════════════════════════
with st.spinner("Conectando con Yahoo Finance..."):
    datos = descargar_datos(tickers)

tickers_ok = [t for t in tickers if t in datos]
if not tickers_ok:
    st.error("No se pudieron descargar datos. Verifica los tickers.")
    st.stop()

st.markdown(ticker_html(datos), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SECCIÓN 1: DATOS HISTÓRICOS
# ═══════════════════════════════════════════════════════
st.markdown(H(1, "DATOS HISTÓRICOS", "PRECIOS · 2 AÑOS"), unsafe_allow_html=True)
st.plotly_chart(fig_precios_historicos(datos, tickers_ok), use_container_width=True)

with st.expander("▼  RETORNOS LOGARÍTMICOS DIARIOS"):
    cols = st.columns(len(tickers_ok))
    for i, t in enumerate(tickers_ok):
        with cols[i]:
            ret = calcular_retornos(datos[t])
            st.plotly_chart(fig_retornos(ret, t),
                            use_container_width=True)
# ═══════════════════════════════════════════════════════
# SECCIÓN 2: BACKTESTING
# ═══════════════════════════════════════════════════════
st.markdown(H(2, "BACKTESTING", "ÚLTIMO MES · 21 DÍAS"), unsafe_allow_html=True)

resultados_bt   = {}
resultados_proy = []

prog = st.progress(0)
for idx, t in enumerate(tickers_ok):
    with st.spinner(f"Calibrando modelos · {t}..."):
        bt = backtest_accion(t, datos[t])
        resultados_bt[t] = bt
    prog.progress((idx + 1) / len(tickers_ok))
prog.empty()

tabs = st.tabs([f"  {t}  " for t in tickers_ok])
for i, t in enumerate(tickers_ok):
    bt = resultados_bt[t]
    with tabs[i]:
        st.markdown(
            f'<div class="tk-row">'
            f'<span class="tk-sym">{t}</span>'
            f'<span class="tk-sep">·</span>'
            f'<span class="tk-lbl">MODELO GANADOR</span>'
            f'{badge(bt["ganador"])}</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("RMSE GBM",    f"${bt['rmses']['GBM']:.4f}")
        c2.metric("RMSE Heston", f"${bt['rmses']['Heston']:.4f}")
        c3.metric("RMSE Merton", f"${bt['rmses']['Merton']:.4f}")

        S0 = datos[t]["Close"].squeeze().values[bt["T_train"] - 1]
        col1, col2, col3 = st.columns(3)
        with col1:
            mu_g, sig_g = bt["params"]["gbm"]
            st.plotly_chart(fig_simulaciones(
                simular_gbm(S0, mu_g, sig_g, 22),
                bt["test_precios"], f"GBM — {t}", COLORS["GBM"], bt["T_train"], datos[t]),
                use_container_width=True)
        with col2:
            mu_h, v0, kappa, theta, xi, rho = bt["params"]["heston"]
            st.plotly_chart(fig_simulaciones(
                simular_heston(S0, mu_h, v0, kappa, theta, xi, rho, 22),
                bt["test_precios"], f"Heston — {t}", COLORS["Heston"], bt["T_train"], datos[t]),
                use_container_width=True)
        with col3:
            mu_m, sig_m, lam, mu_j, sig_j = bt["params"]["merton"]
            st.plotly_chart(fig_simulaciones(
                simular_merton(S0, mu_m, sig_m, lam, mu_j, sig_j, 22),
                bt["test_precios"], f"Merton — {t}", COLORS["Merton"], bt["T_train"], datos[t]),
                use_container_width=True)


# ═══════════════════════════════════════════════════════
# SECCIÓN 3: TABLA RMSE
# ═══════════════════════════════════════════════════════
st.markdown(H(3, "TABLA RMSE COMPARATIVA", "3 MODELOS · BACKTESTING"), unsafe_allow_html=True)

filas_rmse = []
for t in tickers_ok:
    bt = resultados_bt[t]
    filas_rmse.append({
        "Acción":         t,
        "Sector":         SECTOR_MAP.get(t, "—"),
        "RMSE GBM":       round(bt["rmses"]["GBM"],    4),
        "RMSE Heston":    round(bt["rmses"]["Heston"], 4),
        "RMSE Merton":    round(bt["rmses"]["Merton"], 4),
        "Modelo ganador": bt["ganador"],
    })
tabla_rmse = pd.DataFrame(filas_rmse)
st.dataframe(
    tabla_rmse.style.highlight_min(
        subset=["RMSE GBM", "RMSE Heston", "RMSE Merton"],
        axis=1, color="#0d2118"),
    use_container_width=True, hide_index=True)
st.plotly_chart(fig_rmse_comparacion(tabla_rmse), use_container_width=True)


# ═══════════════════════════════════════════════════════
# SECCIÓN 4: PROYECCIÓN A 1 MES
# ═══════════════════════════════════════════════════════
st.markdown(H(4, "PROYECCIÓN", "PRÓXIMOS 21 DÍAS BURSÁTILES"), unsafe_allow_html=True)

for t in tickers_ok:
    proy = proyectar_accion(t, datos[t], resultados_bt[t])
    proy["ticker"] = t
    resultados_proy.append(proy)

cols_p = st.columns(len(tickers_ok))
for i, proy in enumerate(resultados_proy):
    t   = proy["ticker"]
    var = (proy["p50"] - proy["S0"]) / proy["S0"] * 100
    with cols_p[i]:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">'
            f'<span class="tk-sym">{t}</span>{badge(proy["ganador"])}</div>',
            unsafe_allow_html=True,
        )
        st.metric("Precio actual",   f"${proy['S0']:.2f}")
        st.metric("P50 esperado",    f"${proy['p50']:.2f}", delta=f"{var:+.1f}%")
        st.metric("Rango inf. (P5)",  f"${proy['p5']:.2f}")
        st.metric("Rango sup. (P95)", f"${proy['p95']:.2f}")

st.markdown("<br>", unsafe_allow_html=True)
#for proy in resultados_proy:
#    st.plotly_chart(fig_proyeccion(proy, proy["ticker"]), use_container_width=True)

filas_proy = []
for proy in resultados_proy:
    t = proy["ticker"]
    filas_proy.append({
        "Acción":              t,
        "Modelo":              proy["ganador"],
        "Precio actual":       f"${proy['S0']:.2f}",
        "P5% (mín esperado)":  f"${proy['p5']:.2f}",
        "P50% (esperado)":     f"${proy['p50']:.2f}",
        "P95% (máx esperado)": f"${proy['p95']:.2f}",
        "Var. esperada":       f"{(proy['p50']-proy['S0'])/proy['S0']*100:+.1f}%",
    })
st.dataframe(pd.DataFrame(filas_proy), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════
# SECCIÓN 5: RECOMENDACIÓN EJECUTIVA
# ═══════════════════════════════════════════════════════
st.markdown(H(5, "RECOMENDACIÓN EJECUTIVA", "ASIGNACIÓN DE PORTAFOLIO"), unsafe_allow_html=True)

rec = generar_recomendacion(resultados_proy, tabla_rmse)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(dc_html("expand",
        f"📈  MAYOR UPSIDE · {rec['mejor_upside']}",
        "Mayor retorno esperado (P50) relativo al precio actual. "
        "Mejor ratio upside/riesgo del portafolio."),
        unsafe_allow_html=True)
with c2:
    st.markdown(dc_html("hold",
        f"🛡  MENOR RIESGO · {rec['menor_riesgo']}",
        "Menor diferencial P95−P5. Incertidumbre proyectada "
        "más baja — posición defensiva."),
        unsafe_allow_html=True)
with c3:
    st.markdown(dc_html("abandon",
        f"⚠️  MAYOR RIESGO · {rec['mayor_riesgo']}",
        "Mayor diferencial P95−P5. Volatilidad elevada; "
        "mayor potencial de pérdidas extremas."),
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Pie donut
pesos_df = pd.DataFrame([
    {"Acción": t, "Peso (%)": p} for t, p in rec["pesos"].items()
])
fig_pie = go.Figure(go.Pie(
    labels=pesos_df["Acción"],
    values=pesos_df["Peso (%)"],
    marker=dict(colors=LINE_C[:len(pesos_df)],
                line=dict(color="#050b14", width=2)),
    textfont=dict(family="JetBrains Mono", size=11, color="#cdd9f0"),
    hovertemplate="<b>%{label}</b><br>Peso: %{value:.1f}%<extra></extra>",
    hole=0.45,
))
fig_pie.add_annotation(
    text="PORTAFOLIO",
    font=dict(family="Barlow Condensed", size=12, color="#6882a8"),
    showarrow=False,
)
L_pie = _pl("Asignación sugerida de portafolio", 320)
L_pie["showlegend"] = True
fig_pie.update_layout(**L_pie)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown(ip_html(
    "<strong style='color:#ffab00'>NOTA EJECUTIVA:</strong> "
    "Esta aplicación genera escenarios probabilísticos, no predicciones determinísticas. "
    "Los modelos GBM, Heston y Merton calibran volatilidad histórica y el modelo con menor "
    "RMSE en backtesting se usa para la proyección. Los rangos P5–P95 representan el intervalo "
    "de confianza bajo condiciones históricas similares. "
    "<strong>Rentabilidades pasadas no garantizan resultados futuros.</strong>", "a"
), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# SECCIÓN 6: ESTRATEGIA DE OPCIONES REALES
# ═══════════════════════════════════════════════════════
st.markdown(H(6, "OPCIONES REALES", "ÁRBOL BINOMIAL CRR · ESTRATEGIA AMERICANA"),
            unsafe_allow_html=True)

st.markdown(ip_html(
    "<strong style='color:#00c8ff'>MARCO CONCEPTUAL:</strong> "
    "Las <em>opciones reales</em> aplican la teoría de derivados financieros a decisiones "
    "estratégicas de inversión. El portafolio de <strong>$100,000</strong> es el activo "
    "subyacente, y Don Rigoberto posee tres opciones americanas sobre él: "
    "<strong>Expandir</strong> (desplegar $50K adicionales si el precio sube), "
    "<strong>Continuar</strong> (mantener la posición), y "
    "<strong>Abandonar</strong> (liquidar al 92% si cae). "
    "El árbol CRR calibra <em>u</em> y <em>d</em> con la σ ponderada del modelo "
    "ganador de cada acción."
), unsafe_allow_html=True)

with st.expander("▼  FÓRMULAS Y SUPUESTOS DEL ÁRBOL CRR"):
    st.markdown(r"""
**Parámetros Cox-Ross-Rubinstein:**

| Símbolo | Fórmula | Descripción |
|---------|---------|-------------|
| u | $e^{\,\sigma_p \sqrt{\Delta t}}$ | Factor de subida mensual |
| d | $1/u$ | Factor de bajada mensual |
| $\hat{p}$ | $(e^{r_f \Delta t} - d)\,/\,(u - d)$ | Probabilidad risk-neutral |

**Decisión en cada nodo** — máximo de tres opciones:

| Opción | Valor | Se activa cuando |
|--------|-------|-----------------|
| **Expandir** | $1.5 \times V_{actual} - \$50{,}000$ | $V > \$100{,}000$ |
| **Continuar** | $e^{-r\Delta t}[\hat{p}\cdot V_{\uparrow} + (1-\hat{p})\cdot V_{\downarrow}]$ | Siempre disponible |
| **Abandonar** | $V_{actual} \times 0.92$ | $0.92 \cdot V > V_{continuar}$ |

**ENPV = NPV pasivo + Prima de opciones** — la prima cuantifica el valor monetario de la flexibilidad estratégica.
""")

# ── Cálculo ────────────────────────────────────────────
pesos_dict         = rec["pesos"]
sigma_p, mu_p      = _vol_mu_portfolio(tickers_ok, resultados_bt, pesos_dict)
sigma_p            = max(sigma_p, 0.05)
A_op, u_op, d_op, p_op = _arbol_binomial(CAP_BASE, sigma_p)
V_opc, D_opc       = _backward_opciones(A_op, p_op)
V_pas              = _backward_pasivo(A_op, p_op)
enpv               = float(V_opc[0, 0])
npv_base           = float(V_pas[0, 0])
prima_opc          = enpv - npv_base
alpha_anual        = mu_p - R_LIBRE

# ── Parámetros del árbol ───────────────────────────────
st.markdown(sub_h("PARÁMETROS DEL ÁRBOL"), unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("σ portafolio",       f"{sigma_p:.1%}")
c2.metric("Factor subida (u)",  f"{u_op:.4f}")
c3.metric("Factor bajada (d)",  f"{d_op:.4f}")
c4.metric("Prob. risk-neutral", f"{p_op:.3f}")
c5.metric("Alpha μ − rₓ",       f"{alpha_anual:.1%}")

# ── ENPV Breakdown ─────────────────────────────────────
st.markdown(sub_h("VALOR PRESENTE NETO EXTENDIDO (ENPV)"), unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(vc_html(
        "NPV Pasivo (sin flexibilidad)",
        f"${npv_base:,.0f}",
        "Valor descontado sin opciones", "dim"
    ), unsafe_allow_html=True)
with col_b:
    st.markdown(vc_html(
        "ENPV (con opciones reales)",
        f"${enpv:,.0f}",
        "Backward induction — árbol CRR"
    ), unsafe_allow_html=True)
with col_c:
    st.markdown(vc_html(
        "Prima de opciones reales",
        f"+${prima_opc:,.0f}",
        "Valor monetario de la flexibilidad", "cy"
    ), unsafe_allow_html=True)

# ── Árbol visual ────────────────────────────────────────
st.markdown(sub_h("ÁRBOL DE DECISIONES ÓPTIMAS"), unsafe_allow_html=True)
st.plotly_chart(_fig_arbol_opciones(A_op, V_opc, D_opc), use_container_width=True)

# ── Escenarios terminales ──────────────────────────────
st.markdown(sub_h("ESCENARIOS TERMINALES — MES 4"), unsafe_allow_html=True)
filas_term = []
for j in range(N_PER_OP + 1):
    Vt  = A_op[N_PER_OP, j]
    dec = D_opc[N_PER_OP, j]
    ret = (Vt - CAP_BASE) / CAP_BASE
    if dec == "Expandir":
        vf   = 1.5 * Vt - CAP_EXP
        nota = f"Escala a ${1.5*Vt/1e3:.1f}k − $50k inversión"
    elif dec == "Abandonar":
        vf   = Vt * SALVAGE
        nota = f"Recuperar ${vf/1e3:.1f}k (8% costo transacción)"
    else:
        vf   = Vt
        nota = "Mantener posición"
    filas_term.append({
        "Subidas":           j,
        "V portafolio":      f"${Vt:,.0f}",
        "Retorno acumulado": f"{ret:+.1%}",
        "Decisión óptima":   dec,
        "Valor final neto":  f"${vf:,.0f}",
        "Nota":              nota,
    })
st.dataframe(pd.DataFrame(filas_term), use_container_width=True, hide_index=True)

# ── Reglas de decisión ─────────────────────────────────
st.markdown(sub_h("REGLAS DE ACCIÓN POR MES"), unsafe_allow_html=True)

meses_exp = [i for i in range(N_PER_OP + 1)
             if "Expandir"  in [D_opc[i, j] for j in range(i + 1)]]
meses_abn = [i for i in range(N_PER_OP + 1)
             if "Abandonar" in [D_opc[i, j] for j in range(i + 1)]]

col_r1, col_r2 = st.columns(2)
with col_r1:
    if meses_exp:
        st.markdown(dc_html("expand",
            "📈  EXPANDIR — DESPLEGAR $50,000",
            f"Activar si portafolio supera <strong>$100,000</strong> en "
            f"meses: {', '.join(str(m) for m in meses_exp)}.<br>"
            f"NPV neto de expansión = 0.5×V − $50,000 → "
            f"call implícito con strike K = $100,000."),
            unsafe_allow_html=True)
    else:
        st.markdown(dc_html("hold",
            "CONTINUAR — SIN EXPANSIÓN ÓPTIMA",
            "La volatilidad actual no genera nodos de expansión rentables. "
            "Mantener la posición en todos los escenarios."),
            unsafe_allow_html=True)

with col_r2:
    if meses_abn:
        st.markdown(dc_html("abandon",
            "🔴  ABANDONAR — LIQUIDAR AL 92%",
            f"Cortar pérdidas si portafolio cae bajo umbral en "
            f"meses: {', '.join(str(m) for m in meses_abn)}.<br>"
            f"Recuperar {SALVAGE:.0%} del valor antes de pérdidas adicionales."),
            unsafe_allow_html=True)
    else:
        st.markdown(dc_html("hold",
            "CONTINUAR — SIN ABANDONO ÓPTIMO",
            "En todos los escenarios es preferible continuar que liquidar. "
            "El costo de transacción del 8% no justifica el abandono."),
            unsafe_allow_html=True)

st.markdown(ip_html(
    f"<strong style='color:#00e676'>INTERPRETACIÓN EJECUTIVA:</strong> "
    f"La <em>prima de opciones reales</em> de <strong>${prima_opc:,.0f}</strong> "
    f"es el valor de no comprometer los $50,000 hoy. Mantener la reserva equivale "
    f"a poseer un <em>call americano</em> sobre el portafolio con strike $100K y un "
    f"<em>put de piso</em> al {SALVAGE:.0%}. El árbol CRR — calibrado con "
    f"σ<sub>p</sub>&nbsp;=&nbsp;{sigma_p:.1%} — revela el mes óptimo para desplegar "
    f"capital o cortar pérdidas, convirtiendo la incertidumbre en ventaja estratégica "
    f"cuantificable.", "g"
), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="ftr">
    <span>Universidad Externado de Colombia · Valoración de Activos · 2025</span>
    <span>GBM · Heston · Merton · Opciones Reales · Árbol CRR</span>
    <span>El futuro no se predice — se simula.</span>
</div>
""", unsafe_allow_html=True)
