import streamlit as st

st.title("🌡️ Termometro 10.3")

# Layout a due colonne per migliorare l'estetica
col1, col2 = st.columns(2)

with col1:
    st.subheader("Casa")
    n_cs = st.text_input("Nome Casa", key="n_cs")
    p_cs = st.number_input("Punti Casa", 0.0, key="p_cs")
    t_cs = st.number_input("Tiri Casa", 0.0, key="t_cs")
    g_cs = st.number_input("Gol Casa", 0.0, key="g_cs")
    c_cs = st.number_input("Clean Sheet Casa", 0, key="c_cs")

with col2:
    st.subheader("Ospite")
    n_os = st.text_input("Nome Ospite", key="n_os")
    p_os = st.number_input("Punti Ospite", 0.0, key="p_os")
    t_os = st.number_input("Tiri Ospite", 0.0, key="t_os")
    g_os = st.number_input("Gol Ospite", 0.0, key="g_os")
    c_os = st.number_input("Clean Sheet Ospite", 0, key="c_os")

st.write("---")

if st.button("CALCOLA"):
    # Calcolo valori
    val_c = (p_cs * 0.1) + (t_cs * 0.1) + (g_cs * 0.8)
    if c_cs > 3: 
        val_c *= 1.05
    
    val_o = (p_os * 0.1) + (t_os * 0.1) + (g_os * 0.8)
    if c_os > 3: 
        val_o *= 1.05
    
    tot = val_c + val_o
    
    if tot > 0:
        res_c = (val_c / tot) * 100
        res_o = (val_o / tot) * 100
        
        # Visualizzazione risultati
        col_r1, col_r2 = st.columns(2)
        col_r1.metric(f"Probabilità 1X ({n_cs if n_cs else 'Casa'})", f"{res_c:.1f}%")
        col_r2.metric(f"Probabilità X2 ({n_os if n_os else 'Ospite'})", f"{res_o:.1f}%")
    else:
        st.warning("Inserisci dei dati validi per ottenere un calcolo.")
