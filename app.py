import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(
    page_title="Kalkulator Gabarita Staklene Ograde",
    page_icon="📐",
    layout="centered"
)

# Moderni CSS stilovi
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📐 Kalkulator Gabarita Staklene Ograde")

if 'korak' not in st.session_state:
    st.session_state.korak = 1

if 'h1' not in st.session_state:
    st.session_state.h1 = 160.0
if 'lk' not in st.session_state:
    st.session_state.lk = 300.0
if 'h2' not in st.session_state:
    st.session_state.h2 = 80.0

def proracun(h1, lk, h2):
    if lk == 0:
        return None
    sin_a = h2 / lk
    cos_a = math.sqrt(max(0, 1 - sin_a**2))

    w1 = lk * cos_a
    h1_gab = h1 + h2

    w2 = lk + h1 * sin_a
    h2_gab = h1 * cos_a

    p_staklo_m2 = (h1 * w1) / 10000.0
    p1_m2 = (w1 * h1_gab) / 10000.0
    p2_m2 = (w2 * h2_gab) / 10000.0

    return {
        "w1": w1,
        "h1_gab": h1_gab,
        "p1_m2": p1_m2,
        "w2": w2,
        "h2_gab": h2_gab,
        "p2_m2": p2_m2,
        "p_staklo_m2": p_staklo_m2,
        "sin_a": sin_a,
        "cos_a": cos_a,
    }

# Navigacioni meni preko dugmića
col_nav1, col_nav2, col_nav3 = st.columns(3)
with col_nav1:
    if st.button("1. Unos"):
        st.session_state.korak = 1
with col_nav2:
    if st.button("2. Slučaj 1"):
        st.session_state.korak = 2
with col_nav3:
    if st.button("3. Slučaj 2"):
        st.session_state.korak = 3

st.divider()

# KORAK 1: UNOS MERA
if st.session_state.korak == 1:
    st.subheader("Unesite dimenzije staklene ograde (u cm)")
    
    with st.form(key='dim_form'):
        val_h1 = st.number_input("Visina stakla (h1)", value=float(st.session_state.h1), min_value=1.0, step=1.0)
        val_lk = st.number_input("Kosa stranica (lk)", value=float(st.session_state.lk), min_value=1.0, step=1.0)
        val_h2 = st.number_input("Visinska razlika (h2)", value=float(st.session_state.h2), min_value=0.0, step=1.0)
        
        submit_button = st.form_submit_button(label="Sačuvaj i Prikaži Slučaj 1 →")
        
        if submit_button:
            if val_lk <= val_h2:
                st.error("Kosa stranica (lk) mora biti veća od visinske razlike (h2).")
            else:
                st.session_state.h1 = val_h1
                st.session_state.lk = val_lk
                st.session_state.h2 = val_h2
                st.session_state.korak = 2
                st.rerun()

    # Tehnička skica sa kotama za unos
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_aspect('equal')
    ax.axis('off')
    
    ox, oy = 2.5, 3.5
    dx = 4.5
    h1_p = 2.8
    h2_p = 1.4
    off = 0.6
    
    t1 = (ox, oy)
    t2 = (ox + dx, oy - h2_p)
    t3 = (ox + dx, oy - h2_p - h1_p)
    t4 = (ox, oy - h1_p)
    
    ax.add_patch(patches.Polygon([t1, t2, t3, t4], closed=True, facecolor="#F8FAFC", edgecolor="#0F172A", linewidth=2))
    
    # Kotne linije
    ax.annotate('', xy=(ox - off, oy), xytext=(ox - off, oy - h1_p), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(ox - off - 0.3, oy - h1_p/2, f"h1 = {st.session_state.h1:.0f}", fontweight='bold', fontsize=10, ha='center', va='center', rotation=90)
    
    ax.annotate('', xy=(ox + dx + off, oy), xytext=(ox + dx + off, oy - h2_p), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(ox + dx + off + 0.3, oy - h2_p/2, f"h2 = {st.session_state.h2:.0f}", fontweight='bold', fontsize=10, ha='center', va='center', rotation=90)
    
    ax.annotate('', xy=(t4[0], t4[1] + off), xytext=(t3[0], t3[1] + off), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text((t4[0]+t3[0])/2, t4[1] + off + 0.3, f"lk = {st.session_state.lk:.0f}", fontweight='bold', fontsize=10, ha='center', va='center')

    ax.set_xlim(-1, ox + dx + 2)
    ax.set_ylim(oy - h1_p - h2_p - 1.5, oy + 1.5)
    st.pyplot(fig)

# KORAK 2: SLUČAJ 1 (ORTOGONALNI)
elif st.session_state.korak == 2:
    res = proracun(st.session_state.h1, st.session_state.lk, st.session_state.h2)
    skart = res['p1_m2'] - res['p_staklo_m2']
    
    st.subheader("Slučaj 1 — Ortogonalni pripremak")
    st.info(f"Površina pripremka: **P1 = {res['p1_m2']:.3f} m²**  |  Škarta: **{skart:.3f} m²**")
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_aspect('equal')
    ax.axis('off')
    
    ox, oy = 2.5, 3.5
    dx = 4.5
    h1_p = 2.8
    h2_p = 1.4
    off = 0.6
    
    t1 = (ox, oy)
    t2 = (ox + dx, oy - h2_p)
    t3 = (ox + dx, oy - h2_p - h1_p)
    t4 = (ox, oy - h1_p)
    
    ax.add_patch(patches.Rectangle((ox, oy - h1_p - h2_p), dx, h1_p + h2_p, linewidth=1.5, edgecolor='#334155', facecolor='#F1F5F9', linestyle='--'))
    ax.add_patch(patches.Polygon([t1, t2, t3, t4], closed=True, facecolor="#0EA5E9", alpha=0.15, edgecolor="#0284C7", linewidth=2))
    
    # Kote gabarita
    ax.annotate('', xy=(ox - off, oy), xytext=(ox - off, oy - h1_p - h2_p), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(ox - off - 0.4, oy - (h1_p+h2_p)/2, f"h1_gab = {res['h1_gab']:.1f}", fontweight='bold', fontsize=10, ha='center', va='center', rotation=90)
    
    ax.annotate('', xy=(ox, oy + off), xytext=(ox + dx, oy + off), arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
    ax.text(ox + dx/2, oy + off + 0.3, f"w1 = {res['w1']:.1f}", fontweight='bold', fontsize=10, ha='center', va='center')
    
    ax.text(ox + dx/2, oy - (h1_p + h2_p)/2, f"P = {res['p_staklo_m2']:.3f} m²", fontweight='bold', fontsize=11, ha='center', va='center', color='#0F172A')

    ax.set_xlim(-1, ox + dx + 2)
    ax.set_ylim(oy - h1_p - h2_p - 1.5, oy + 1.5)
    st.pyplot(fig)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Nazad"):
            st.session_state.korak = 1
            st.rerun()
    with c2:
        if st.button("Sledeći →"):
            st.session_state.korak = 3
            st.rerun()

# KORAK 3: SLUČAJ 2 (ZAOKRENUTI)
elif st.session_state.korak == 3:
    res = proracun(st.session_state.h1, st.session_state.lk, st.session_state.h2)
    skart = res['p2_m2'] - res['p_staklo_m2']
    
    st.subheader("Slučaj 2 — Zaokrenuti pripremak")
    st.info(f"Površina pripremka: **P2 = {res['p2_m2']:.3f} m²**  |  Škarta: **{skart:.3f} m²**")
    
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_aspect('equal')
    ax.axis('off')
    
    ox, oy = 2.5, 3.2
    dx = 4.5
    h1_p = 2.6
    h2_p = 1.3
    
    t1 = (ox, oy)
    t2 = (ox + dx, oy - h2_p)
    t3 = (ox + dx, oy - h2_p - h1_p)
    t4 = (ox, oy - h1_p)
    
    len_u = math.hypot(dx, -h2_p)
    ux, uy = dx / len_u, -h2_p / len_u
    proj_w_extra = h1_p * (h2_p / len_u)
    
    g2 = (t2[0] + proj_w_extra * ux, t2[1] + proj_w_extra * uy)
    g4 = (t4[0] - proj_w_extra * ux, t4[1] - proj_w_extra * uy)
    
    ax.plot([t1[0], g4[0]], [t1[1], g4[1]], 'k--', linewidth=1.2)
    ax.plot([t4[0], g4[0]], [t4[1], g4[1]], 'k--', linewidth=1.2)
    ax.plot([t2[0], g2[0]], [t2[1], g2[1]], 'k--', linewidth=1.2)
    ax.plot([t3[0], g2[0]], [t3[1], g2[1]], 'k--', linewidth=1.2)
    
    ax.add_patch(patches.Polygon([t1, t2, t3, t4], closed=True, facecolor="#0EA5E9", alpha=0.15, edgecolor="#0284C7", linewidth=2))
    
    angle_deg = math.degrees(math.atan2(-uy, ux))
    ax.text(ox + dx/2, oy - (h1_p + h2_p)/2, f"P = {res['p_staklo_m2']:.3f} m²", fontweight='bold', fontsize=11, ha='center', va='center', color='#0F172A')
    ax.text((t1[0]+g2[0])/2, (t1[1]+g2[1])/2 - 0.4, f"w2 = {res['w2']:.1f}", fontweight='bold', fontsize=10, ha='center', va='center', rotation=angle_deg)
    ax.text((t3[0]+g2[0])/2 + 0.3, (t3[1]+g2[1])/2, f"h2_gab = {res['h2_gab']:.1f}", fontweight='bold', fontsize=10, ha='center', va='center', rotation=angle_deg+90)

    ax.set_xlim(-1, ox + dx + 2.5)
    ax.set_ylim(oy - h1_p - h2_p - 1.5, oy + 1.5)
    st.pyplot(fig)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Nazad"):
            st.session_state.korak = 2
            st.rerun()
    with c2:
        if st.button("↺ Izmena"):
            st.session_state.korak = 1
            st.rerun()
