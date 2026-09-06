import streamlit as st
import math

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Sniper PRO - v7.4 Pure Stats", layout="wide")

# --- STILE CSS PROFESSIONALE ---
st.markdown("""
<style>
    .verdict-box {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .btts-yes { background-color: #28a745; }
    .btts-no { background-color: #dc3545; }
    .neutral-box { background-color: #ffc107; color: #333 !important; }
    .pro-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #007bff;
        color: #333;
        margin-top: 20px;
    }
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
        margin-top: 10px;
    }
    .matrix-table th, .matrix-table td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .matrix-table th {
        background-color: #f2f2f2;
        color: #333;
    }
    .highlight-cell {
        background-color: #d4edda;
        font-weight: bold;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎯 SNIPER PRO - v7.4 PURE STATS & xG</h1>", unsafe_allow_html=True)

# --- LAYOUT INPUT DATI SQUADRE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Squadra Casa")
    h_gf = st.number_input("Gol Fatti (GF)", 0, 50, 20, key="h_gf")
    h_gs = st.number_input("Gol Subiti (GS)", 0, 50, 14, key="h_gs")
    h_cs = st.number_input("Clean Sheet (CS)", 0, 15, 3, key="h_cs")
    h_ltd = st.number_input("Lay The Draw (LTD)", 0, 15, 8, key="h_ltd")
    h_sbh = st.number_input("Gol entrambi i tempi (SBH)", 0, 15, 3, key="h_sbh")

with col2:
    st.subheader("✈️ Squadra Ospite")
    a_gf = st.number_input("Gol Fatti (GF)", 0, 50, 12, key="a_gf")
    a_gs = st.number_input("Gol Subiti (GS)", 0, 50, 15, key="a_gs")
    a_cs = st.number_input("Clean Sheet (CS)", 0, 15, 0, key="a_cs")
    a_ltd = st.number_input("Lay The Draw (LTD)", 0, 15, 6, key="a_ltd")
    a_sbh = st.number_input("Gol entrambi i tempi (SBH)", 0, 15, 2, key="a_sbh")

st.markdown("---")
analyze_btn = st.button("🚀 ESEGUI SIMULAZIONE PURAMENTE STATISTICA", type="primary", use_container_width=True)

if analyze_btn:
    # --- MOTORE MATEMATICO PURO (SENZA QUOTE) ---
    base_home_xg = max(0.3, (h_gf * 0.5 + a_gs * 0.5) / 10.0)
    base_away_xg = max(0.3, (a_gf * 0.5 + h_gs * 0.5) / 10.0)

    def poisson_prob(lmbda, k): 
        return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

    max_goals = 5
    matrix = [[0.0 for _ in range(max_goals + 1)] for _ in range(max_goals + 1)]
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    btts_prob = 0.0
    over_25_prob = 0.0
    exact_scores_list = []

    for h in range(max_goals + 1): 
        for a in range(max_goals + 1): 
            p = poisson_prob(base_home_xg, h) * poisson_prob(base_away_xg, a) * 100.0 
            matrix[h][a] = p 
            exact_scores_list.append((h, a, p)) 
            if h > a: 
                home_win_prob += p 
            elif h == a: 
                draw_prob += p 
            else: 
                away_win_prob += p 
            if h > 0 and a > 0: 
                btts_prob += p 
            if (h + a) > 2.5: 
                over_25_prob += p

    exact_scores_list.sort(key=lambda x: x[2], reverse=True)

    # Indice di Affidabilità basato solo su statistiche e xG
    attack_power = (h_gf + a_gf) * 0.50
    defense_fragility = (h_gs + a_gs) * 0.45
    tempo_dynamics = (h_sbh + a_sbh) * 2.5 + (h_ltd + a_ltd) * 1.0
    cs_resistance = (h_cs + a_cs) * 4.0
    raw_score = 35.0 + attack_power + defense_fragility + tempo_dynamics - cs_resistance
    
    final_index = (raw_score * 0.50) + (btts_prob * 0.50)
    final_index = min(max(final_index, 10.0), 95.0)

    st.markdown("---")

    # GESTIONE VERDETTI
    if final_index >= 68.0: 
        st.markdown(f'<div class="verdict-box btts-yes">✅ PRONOSTICO: GOL (ALTA FIDUCIA)<br><span style="font-size: 16px;">Indice Affidabilità Statistica: {final_index:.1f}% | Prob. BTTS (xG): {btts_prob:.1f}%</span></div>', unsafe_allow_html=True)
    elif final_index <= 38.0: 
        no_gol_percentage = 100.0 - final_index 
        st.markdown(f'<div class="verdict-box btts-no">🛡️ PRONOSTICO: NO GOL / UNDER (ALTA FIDUCIA)<br><span style="font-size: 16px;">Indice No Gol: {no_gol_percentage:.1f}% | Under 2.5 stimato: {100-over_25_prob:.1f}%</span></div>', unsafe_allow_html=True)
    else: 
        st.markdown(f'<div class="verdict-box neutral-box">⚠️ MATCH INCERTO - NESSUN BET CONSIGLIATO<br><span style="font-size: 16px;">Indice Intermedio: {final_index:.1f}% (Zona di rischio: dati bilanciati)</span></div>', unsafe_allow_html=True)

    # --- SEZIONE RISULTATI ESATTI & MATRICE ---
    st.subheader("🎯 Top 5 Risultati Esatti più Probabili")
    cols = st.columns(5)
    for i in range(5): 
        s = exact_scores_list[i] 
        with cols[i]: 
            st.metric(label=f"#{i+1} ({s[0]}-{s[1]})", value=f"{s[2]:.1f}%")

    with st.expander("📊 Visualizza Matrice Completa delle Probabilità (Casa 🏠 vs Ospiti ✈️)"): 
        table_html = "<table class='matrix-table'><tr><th>Casa \\ Ospiti</th>" 
        for a in range(max_goals + 1): 
            table_html += f"<th>{a}</th>" 
        table_html += "</tr>" 
        for h in range(max_goals + 1): 
            table_html += f"<tr><th>{h}</th>" 
            for a in range(max_goals + 1): 
                val = matrix[h][a] 
                if h == exact_scores_list[0][0] and a == exact_scores_list[0][1]: 
                    table_html += f"<td class='highlight-cell'>{val:.1f}%</td>" 
                else: 
                    table_html += f"<td>{val:.1f}%</td>" 
            table_html += "</tr>" 
        table_html += "</table>" 
        st.markdown(table_html, unsafe_allow_html=True)

    # Sintesi Mercati Principali
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Stima Segno 1", f"{home_win_prob:.1f}%")
    m2.metric("Stima X", f"{draw_prob:.1f}%")
    m3.metric("Stima Segno 2", f"{away_win_prob:.1f}%")
    m4.metric("Stima Over 2.5", f"{over_25_prob:.1f}%")

    # Box Diagnostica
    st.markdown(f'''
    <div class="pro-box"> 
        🔍 <b>DIAGNOSTICA PURAMENTE STATISTICA:</b><br> 
        • Expected Goals (xG) Casa: <b>{base_home_xg:.2f}</b> | xG Ospite: <b>{base_away_xg:.2f}</b><br> 
        • Modello calcolato senza l'influenza delle quote dei bookmaker.<br> 
        • Il risultato esatto favorito dal modello matematico è il <b>{exact_scores_list[0][0]}-{exact_scores_list[0][1]}</b> ({exact_scores_list[0][2]:.1f}%). 
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("📌 Inserisci i dati delle squadre e avvia la simulazione basata interamente sulle statistiche e sugli xG.")
