import streamlit as st

# --- MOTORE DI CALCOLO ---
def analisi_sniper_pro_master(gf_c, gs_c, gf_o, gs_o, competizione, q1, qx, q2):
    rischio = (gs_c + gs_o)
    media_gol = (gf_c + gf_o + gs_c + gs_o) / 2
    rating = 5
    messaggi = []
    is_coppa = any(x in competizione.lower() for x in ["champions", "conference", "qualificazione", "europa", "coppa"])
    
    if is_coppa:
        rischio *= 1.3
        rating -= 2
        messaggi.append("⚠️ Coppa: Rischio aumentato.")
    if rischio < 2.0 and media_gol > 2.8:
        messaggi.append("⚠️ Conflitto: Segno X sconsigliato.")
        rating -= 1
    if rischio > 2.5:
        rating -= 2
    
    rating = max(1, min(5, rating))
    prob_1 = (1 / q1) * 100
    return rischio, media_gol, rating, messaggi, prob_1

# --- INTERFACCIA UI OTTIMIZZATA ---
st.title("Sniper PRO: Master V2")

comp = st.text_input("Competizione", "Campionato")

# Input ordinati per Casa e Ospite
col_casa, col_ospite = st.columns(2)

with col_casa:
    st.subheader("🏠 Casa")
    gf_c = st.number_input("Gol Fatti Casa", value=2.0, step=0.1)
    gs_c = st.number_input("Gol Subiti Casa", value=1.0, step=0.1)

with col_ospite:
    st.subheader("✈️ Ospite")
    gf_o = st.number_input("Gol Fatti Ospite", value=1.5, step=0.1)
    gs_o = st.number_input("Gol Subiti Ospite", value=1.2, step=0.1)

# Quote su una riga
c3, c4, c5 = st.columns(3)
q1 = c3.number_input("Q1", value=2.50, step=0.01)
qx = c4.number_input("QX", value=3.40, step=0.01)
q2 = c5.number_input("Q2", value=2.35, step=0.01)

if st.button("Analizza Partita", use_container_width=True):
    rischio, media, rating, avvisi, prob_1 = analisi_sniper_pro_master(gf_c, gs_c, gf_o, gs_o, comp, q1, qx, q2)
    
    # Risultati
    r1, r2 = st.columns(2)
    r1.write(f"### {'⭐' * rating}")
    r2.metric("Rischio", f"{rischio:.2f}")
    
    st.metric("Probabilità Mercato (1)", f"{prob_1:.1f}%")
    
    for avviso in avvisi:
        st.warning(avviso)
        
    s1, s2 = st.columns(2)
    if rating >= 3:
        s1.success("✅ 1X / DC")
        s2.success("✅ GOAL")
    else:
        s1.error("🚫 NO 1X2")
        s2.info("✅ SOLO GOAL")
