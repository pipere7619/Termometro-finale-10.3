import streamlit as st

st.set_page_config(page_title="Termometro 10.3", layout="centered")
st.title("🌡️ Termometro 10.3")

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

if st.button("CALCOLA"):
    def calc(p, t, g, c):
        # Aggiungiamo il valore fisso 12 nel calcolo base
        v = (p*0.1) + (t*0.1) + (g*0.8) + 12
        return v * 1.05 if c > 3 else v
    
    val_c = calc(p_c, t_c, g_c, c_c)
    val_o = calc(p_o, t_o, g_o, c_o)
    tot = val_c + val_o
    
    if tot > 0:
        perc_c = (val_c/tot)*100
        perc_o = (val_o/tot)*100
        
        st.write("### Risultato:")
        st.metric(f"1X {n_c}", f"{perc_c:.1f}%")
        st.metric(f"X2 {n_o}", f"{perc_o:.1f}%")
        
        if perc_c >= 54.0: st.success("🟢 GIOCABILE: 1X")
        elif perc_o >= 54.0: st.success("🟢 GIOCABILE: X2")
        else: st.warning("🟡 PASSARE")
