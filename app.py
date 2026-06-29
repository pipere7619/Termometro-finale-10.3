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
    
    # Calcolo 1-2 (No Pareggio)
    diff = abs(val_c - val_o)
    perc_12 = min((diff / tot) * 200, 100.0)
    
    # Calcolo Valore (Value Betting)
    valore_1 = "SÌ" if ((perc_1x / 100) * q_1) > 1.0 else "NO"
    valore_2 = "SÌ" if ((perc_x2 / 100) * q_2) > 1.0 else "NO"
    
    st.write("### Risultati:")
    st.metric("Probabilità 1X", f"{perc_1x:.1f}%")
    st.metric("Probabilità X2", f"{perc_x2:.1f}%")
    st.metric("Probabilità 1-2 (No Pareggio)", f"{perc_12:.1f}%")
    
    st.write("---")
    st.write(f"**Analisi Valore Casa:** {valore_1} (Quota {q_1})")
    st.write(f"**Analisi Valore Ospite:** {valore_2} (Quota {q_2})")
    
    if perc_1x >= 52.0: st.success("🟢 1X GIOCABILE")
    elif perc_x2 >= 52.0: st.success("🟢 X2 GIOCABILE")
    elif perc_12 >= 40.0: st.success("🟢 1-2 (Vittoria Secca) PROBABILE")
    else: st.warning("🟡 PASSARE")
