import streamlit as st

st.set_page_config(page_title="Termometro 10.3", layout="centered")
st.title("🌡️ Termometro 10.3 - 12 (1/2)")

# Filtri squadre
filtri_squadre = {"serie b": 1.2, "seconda": 1.25, "under": 1.15}

def applica_filtro(nome):
    nome = nome.lower()
    for chiave, moltiplicatore in filtri_squadre.items():
        if chiave in nome:
            return moltiplicatore
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

if st.button("CALCOLA 1-2"):
    def calc(p, t, g, c, nome):
        v = ((p*0.1) + (t*0.1) + (g*0.8) + 12) * applica_filtro(nome)
        return v * 1.05 if c > 3 else v
    
    val_c = calc(p_c, t_c, g_c, c_c, n_c)
    val_o = calc(p_o, t_o, g_o, c_o, n_o)
    tot = val_c + val_o
    
    if tot > 0:
        # Probabilità 1-2 (Vittoria di una delle due)
        # La 1-2 è alta quando il divario tra le due è netto
        diff = abs(val_c - val_o)
        perc_12 = (diff / tot) * 100
        
        st.write("### Risultato 1-2 (Escludi Pareggio):")
        st.metric("Probabilità 1-2", f"{perc_12:.1f}%")
        
        if perc_12 >= 55.0:
            st.success("🟢 1-2 MOLTO PROBABILE")
        else:
            st.warning("🟡 RISCHIOSO / PAREGGIO POSSIBILE")
