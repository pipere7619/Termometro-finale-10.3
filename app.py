import streamlit as st

st.set_page_config(page_title="Sniper PRO - Visione Completa", page_icon="🎯")
st.title("🎯 Sniper PRO - Analisi e BTTS")

# --- INPUT STATISTICO ---
st.subheader("1. Inserimento Dati Statistici")
col1, col2 = st.columns(2)

with col1:
    f_casa = st.number_input("Gol Fatti Casa", min_value=0.0, step=0.1)
    s_casa = st.number_input("Gol Subiti Casa", min_value=0.0, step=0.1)
    q_1x = st.number_input("Quota 1X", min_value=1.0, step=0.01)

with col2:
    f_ospite = st.number_input("Gol Fatti Ospite", min_value=0.0, step=0.1)
    s_ospite = st.number_input("Gol Subiti Ospite", min_value=0.0, step=0.1)
    q_x2 = st.number_input("Quota X2", min_value=1.0, step=0.01)

if st.button("CALCOLA STRATEGIA COMPLETA"):
    # Calcolo Indici
    ind_casa = f_casa / (s_casa + 0.1)
    ind_ospite = f_ospite / (s_ospite + 0.1)
    diff = abs(ind_casa - ind_ospite)

    st.divider()
    st.subheader("📊 Analisi Operativa")

    # Logica Direzionale
    if diff < 0.25:
        direzione = "1X / X2 (Equilibrio)"
        suggerimento = "Situazione di equilibrio statistico."
    elif ind_casa > ind_ospite:
        direzione = "1X"
        suggerimento = "Vantaggio statistico per la casa."
    else:
        direzione = "X2"
        suggerimento = "Vantaggio statistico per l'ospite."

    st.success(f"✅ ESITO PRINCIPALE: {direzione}")
    st.write(f"**Analisi:** {suggerimento}")

    # Visione Logica (Anomalie vs Conferme)
    st.subheader("🧠 Visione Logica")
    if (direzione == "1X" and q_1x < q_x2) or (direzione == "X2" and q_x2 < q_1x):
        st.info("🔹 **Conferma:** Mercato allineato alla statistica.")
    elif diff < 0.3:
        st.warning("🔹 **Stallo:** Mercato incerto, procedere con cautela.")
    else:
        st.error("🔹 **Anomalia:** Il mercato sta sfidando i dati.")

    # --- STRUTTURA ANALISI AVANZATA BTTS ---
    st.divider()
    st.subheader("🎯 Analisi Avanzata BTTS (Fine Partita)")

    # Calcolo di un indice di propensione al BTTS incrociato
    spinta_btts = (f_casa * s_ospite) + (f_ospite * s_casa)

    if spinta_btts > 2.5:
        st.success("🔥 **BTTS ALTAMENTE PROBABILE**")
        st.write(f"Indice di spinta incrociato ({spinta_btts:.2f}): Entrambe le squadre spingono forte e concedono spazi dietro.")
    elif spinta_btts > 1.8:
        st.info("⚖️ **BTTS MODERATO / DA VALUTARE**")
        st.write(f"Indice di spinta ({spinta_btts:.2f}): Situazione di incertezza, verificare le quote e le motivazioni della partita.")
    else:
        st.warning("⚠️ **BTTS SCONSIGLIATO (Rischio No-Goal)**")
        st.write(f"Indice di spinta basso ({spinta_btts:.2f}): Una delle due difese tende a chiudere la saracinesca o gli attacchi sono poco prolifici.")

    # Alternativa Conservativa di appoggio
    st.info("🔹 **OPZIONE 3: Under 3.5 Totale**")
    st.write("Opzione conservativa di copertura per bilanciare la giocata sul BTTS o sulla singola.")

    st.divider()
    st.caption(f"Delta statistico: {diff:.2f} | Sniper PRO v.2026")
