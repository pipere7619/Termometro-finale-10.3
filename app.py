import streamlit as st

st.set_page_config(page_title="Termometro 10.5 Pro", layout="centered")
st.title("🌡️ Termometro 10.5 Pro")
st.subheader("Analisi Pre-Match con Solidità Difensiva")

# Input Dati (Utilizzare sempre le Medie AVG delle ultime 10 partite)
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Casa")
    p_c = st.number_input("Punti (Totali)", 0.0)
    tp_c = st.number_input("Media Tiri in Porta (AVG)", 0.0)
    g_c = st.number_input("Media Gol Fatti (AVG)", 0.0)
    cs_c = st.number_input("Media Clean Sheet (AVG)", 0.0)
    q_1 = st.number_input("Quota 1", 1.0, 10.0, 2.0)

with col2:
    st.markdown("### Ospite")
    p_o = st.number_input("Punti (Totali)", 0.0)
    tp_o = st.number_input("Media Tiri in Porta (AVG)", 0.0)
    g_o = st.number_input("Media Gol Fatti (AVG)", 0.0)
    cs_o = st.number_input("Media Clean Sheet (AVG)", 0.0)
    q_2 = st.number_input("Quota 2", 1.0, 10.0, 2.0)

q_x = st.number_input("Quota Pareggio (X)", 1.0, 10.0, 3.2)

if st.button("CALCOLA CON SOLIDITÀ"):
    # Calcolo Forza: Punti (0.5), Tiri (3.0), Gol (5.0), Clean Sheet (8.0)
    f_c = (p_c * 0.05) + (tp_c * 3.0) + (g_c * 5.0) + (cs_c * 8.0)
    f_o = (p_o * 0.05) + (tp_o * 3.0) + (g_o * 5.0) + (cs_o * 8.0)
    
    # Rapporto di forza
    tot = f_c + f_o
    diff_forza = abs(f_c - f_o) / tot
    
    # La X è supportata se c'è solidità (bonus CS)
    bonus_x = (cs_c + cs_o) * 2.0 
    
    # Penalità di Forza: se le squadre sono sbilanciate, la X viene penalizzata
    penalita_pareggio = max(0.0, (diff_forza - 0.15) * 150.0)
    
    # Calcolo finale probabilità X
    perc_x = max(5.0, (30.0 + bonus_x) - penalita_pareggio)
    
    # Calcolo Valore (Soglia 1.15)
    valore_x = "SÌ" if ((perc_x / 100) * q_x) > 1.15 else "NO"
    
    st.write("---")
    st.metric("Probabilità Pareggio (X)", f"{perc_x:.1f}%")
    st.write(f"**Valore Pareggio:** {valore_x}")
    
    # Feedback visivo
    if perc_x > 25.0 and valore_x == "SÌ":
        st.success("🟢 PAREGGIO (X) AD ALTO VALORE")
    elif diff_forza > 0.3:
        st.warning("⚠️ Partita sbilanciata: il pareggio è altamente improbabile.")
    else:
        st.info("⚪ Analisi neutra: nessuna indicazione forte sulla X.")
