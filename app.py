import streamlit as st

st.set_page_config(page_title="Termometro 10.3", layout="centered")
st.title("🌡️ Termometro 10.3")

# Filtri squadre
filtri = {"serie b": 1.2, "seconda": 1.25, "under": 1.15}

def applica_filtro(nome):
    nome = nome.lower()
    for chiave, mult in filtri.items():
        if chiave in nome: return mult
    return 1.0

col1, col2 = st.columns(2)
with col1:
    n_c = st.text_input("Squadra Casa")
    p_c = st.number_input("Punti Casa", 0.0)
    t_c = st.number_input("Tiri Casa", 0.0)
    g_c = st.number_input("Gol Casa", 0.0)
    c_c = st.number_input("Clean Sheet Casa", 0)

with col2:
    n_o = st.text_input("Squadra Ospite")
    p_o = st.number_input("Punti Ospite", 0.0)
    t_o = st.number_input("Tiri Ospite", 0.0)
    g_o = st.number_input("Gol Ospite", 0.0)
    c_o = st.number_input("Clean Sheet Ospite", 0)

if st.button("CALCOLA TUTTO"):
    def calc(p, t, g, c, nome):
        # Calcolo base della forza della squadra
        v = ((p*0.1) + (t*0.1) + (g*0.8) + 12) * applica_filtro(nome)
        return v * 1.05 if c > 3 else v
    
    val_c = calc(p_c, t_c, g_c, c_c, n_c)
    val_o = calc(p_o, t_o, g_o, c_o, n_o)
    tot = val_c + val_o
    
    # Calcolo percentuali di forza relativa
    perc_1x = (val_c / tot) * 100
    perc_x2 = (val_o / tot) * 100
    
    # Calcolo 1-2 (No Pareggio) ottimizzato:
    # La differenza assoluta viene pesata maggiormente per riflettere lo sbilanciamento
    diff = abs(val_c - val_o)
    perc_12 = (diff / tot) * 200 
    
    st.write("### Risultati:")
    st.metric("Probabilità 1X", f"{perc_1x:.1f}%")
    st.metric("Probabilità X2", f"{perc_x2:.1f}%")
    st.metric("Probabilità 1-2 (No Pareggio)", f"{min(perc_12, 100.0):.1f}%")
    
    # Soglie abbassate per testare meglio le logiche di gioco
    if perc_1x >= 52.0: st.success("🟢 1X GIOCABILE")
    elif perc_x2 >= 52.0: st.success("🟢 X2 GIOCABILE")
    elif perc_12 >= 40.0: st.success("🟢 1-2 (Vittoria Secca) PROBABILE")
    else: st.warning("🟡 PASSARE")
