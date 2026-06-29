import streamlit as st

st.set_page_config(page_title="Termometro 10.3 Pro", layout="centered")
st.title("🌡️ Termometro 10.3 Pro")

# Filtri squadre
filtri = {"serie b": 1.2, "seconda": 1.25, "under": 1.15}

def applica_filtro(nome):
    nome = nome.lower()
    for chiave, mult in filtri.items():
        if chiave in nome: return mult
    return 1.0

# Input Dati
col1, col2 = st.columns(2)
with col1:
    st.subheader("Casa")
    n_c = st.text_input("Squadra Casa")
    p_c = st.number_input("Punti Casa", 0.0)
    t_c = st.number_input("Tiri Casa", 0.0)
    g_c = st.number_input("Gol Casa", 0.0)
    c_c = st.number_input("Clean Sheet Casa", 0)
    q_1 = st.number_input("Quota 1", 1.0, 10.0, 2.0)

with col2:
    st.subheader("Ospite")
    n_o = st.text_input("Squadra Ospite")
    p_o = st.number_input("Punti Ospite", 0.0)
    t_o = st.number_input("Tiri Ospite", 0.0)
    g_o = st.number_input("Gol Ospite", 0.0)
    c_o = st.number_input("Clean Sheet Ospite", 0)
    q_2 = st.number_input("Quota 2", 1.0, 10.0, 2.0)

q_x = st.number_input("Quota Pareggio (X)", 1.0, 10.0, 3.2)

if st.button("CALCOLA TUTTO"):
    def calc(p, t, g, c, nome):
        v = ((p*0.1) + (t*0.1) + (g*0.8) + 12) * applica_filtro(nome)
        return v * 1.05 if c > 3 else v
    
    val_c = calc(p_c, t_c, g_c, c_c, n_c)
    val_o = calc(p_o, t_o, g_o, c_o, n_o)
    tot = val_c + val_o
    
    # Percentuali forza relativa
    perc_1x = (val_c / tot) * 100
    perc_x2 = (val_o / tot) * 100
    
    # Calcolo 1-2 (No Pareggio) e Pareggio stimato
    diff = abs(val_c - val_o)
    perc_12 = min((diff / tot) * 200, 100.0)
    perc_x = 100 - perc_12
    
    # Calcolo Valore (Value Betting)
    valore_1 = "SÌ" if ((perc_1x / 100) * q_1) > 1.05 else "NO"
    valore_x = "SÌ" if ((perc_x / 100) * q_x) > 1.05 else "NO"
    valore_2 = "SÌ" if ((perc_x2 / 100) * q_2) > 1.05 else "NO"
    
    st.write("### Risultati:")
    st.metric("Probabilità 1X", f"{perc_1x:.1f}%")
    st.metric("Probabilità Pareggio (Stima)", f"{perc_x:.1f}%")
    st.metric("Probabilità X2", f"{perc_x2:.1f}%")
    
    st.write("---")
    st.write(f"**Valore 1:** {valore_1} | **Valore X:** {valore_2} | **Valore 2:** {valore_2}")
    
    if perc_1x >= 52.0 and valore_1 == "SÌ": st.success("🟢 1X GIOCABILE (VALORE)")
    elif perc_x2 >= 52.0 and valore_2 == "SÌ": st.success("🟢 X2 GIOCABILE (VALORE)")
    elif perc_x < 60.0 and q_x >= 3.40: st.success("🟢 PAREGGIO (X) AD ALTO VALORE")
    else: st.warning("🟡 PASSARE")
