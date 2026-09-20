import math
import streamlit as st

st.set_page_config(page_title="Sniper PRO - v9.8 57 Up", layout="wide")

st.markdown(
    """
<style>
.verdict-box { padding: 15px; border-radius: 8px; margin-bottom: 10px; font-weight: bold; }
.btts-yes { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
.btts-no { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
.neutral-box { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
.flash-box-red { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; padding: 15px; border-radius: 8px; margin-top: 15px; }
.flash-box-yellow { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; padding: 15px; border-radius: 8px; margin-top: 15px; }
.flash-box-green { background-color: #e2f0d9; color: #274e13; border: 1px solid #b7e1cd; padding: 15px; border-radius: 8px; margin-top: 15px; }
.pro-box { padding: 15px; border-radius: 8px; background-color: #e2e3e5; color: #383d41; margin-top: 15px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<h2 style="text-align: center;">🎯 SNIPER PRO - v9.8 57% IN SU HT</h2>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
  st.subheader("🏠 Squadra Casa")
  h_gf = st.number_input("Gol Fatti Totali (90')", 0, 50, 22, key="h_gf")
  h_gs = st.number_input("Gol Subiti Totali (90')", 0, 50, 15, key="h_gs")
  h_ht_gf = st.number_input("Gol Fatti nel 1° Tempo", 0, 25, 2, key="h_ht_gf")
  h_ht_gs = st.number_input("Gol Subiti nel 1° Tempo", 0, 25, 1, key="h_ht_gs")

with col2:
  st.subheader("✈️ Squadra Ospite")
  a_gf = st.number_input("Gol Fatti Totali (90')", 0, 50, 16, key="a_gf")
  a_gs = st.number_input("Gol Subiti Totali (90')", 0, 50, 18, key="a_gs")
  a_ht_gf = st.number_input("Gol Fatti nel 1° Tempo", 0, 25, 1, key="a_ht_gf")
  a_ht_gs = st.number_input("Gol Subiti nel 1° Tempo", 0, 25, 2, key="a_ht_gs")

st.markdown("---")
analyze_btn = st.button(
    "🚀 ESEGUI SIMULAZIONE 57 UP", type="primary", use_container_width=True
)

if analyze_btn:
  # 1. Motore 90 Minuti (Match Completo)
  base_home_xg = max(0.3, (h_gf * 0.5 + a_gs * 0.5) / 9.0)
  base_away_xg = max(0.3, (a_gf * 0.5 + h_gs * 0.5) / 9.0)


  def poisson_prob(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)


  max_goals = 5
  matrix = [
      [0.0 for _ in range(max_goals + 1)] for _ in range(max_goals + 1)
  ]
  home_win_prob = 0.0
  draw_prob = 0.0
  away_win_prob = 0.0
  btts_match_prob = 0.0
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
        btts_match_prob += p
      if (h + a) > 2.5:
        over_25_prob += p

  exact_scores_list.sort(key=lambda x: x[2], reverse=True)

  # 2. Motore 1° Tempo
  final_h_xg = max(0.12, (h_ht_gf * 0.5 + h_ht_gs * 0.5) / 3.8)
  final_a_xg = max(0.12, (a_ht_gf * 0.5 + a_ht_gs * 0.5) / 3.8)

  p_zero_ht = (math.exp(-final_h_xg) * math.exp(-final_a_xg)) * 100.0
  over_05_ht_prob = 100.0 - p_zero_ht

  raw_btts_ht = (
      (1.0 - math.exp(-final_h_xg)) * (1.0 - math.exp(-final_a_xg)) * 100.0
  )
  btts_ht_prob = min(max(raw_btts_ht, 5.0), 95.0)

  st.markdown("---")

  # Verdetto Match 90'
  if home_win_prob >= 52.0:
    st.markdown(
        f'<div class="verdict-box btts-yes">🏠 PRONOSTICO 90\': VITTORIA CASA'
        f" (1) — Probabilità: {home_win_prob:.1f}%</div>",
        unsafe_allow_html=True,
    )
  elif away_win_prob >= 52.0:
    st.markdown(
        f'<div class="verdict-box btts-yes">✈️ PRONOSTICO 90\': VITTORIA OSPITE'
        f" (2) — Probabilità: {away_win_prob:.1f}%</div>",
        unsafe_allow_html=True,
    )
  elif btts_match_prob >= 62.0:
    st.markdown(
        f'<div class="verdict-box btts-yes">✅ PRONOSTICO 90\': GOL / BTTS'
        f" INTERO MATCH — Probabilità: {btts_match_prob:.1f}%</div>",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f'<div class="verdict-box neutral-box">⚠️ MATCH EQUILIBRATO / 90\' INCERTO'
        f' (X o Under prudente)</div>',
        unsafe_allow_html=True,
    )

  # Verdetto BTTS 1° Tempo - SOGLIA DA 57% IN SU
  if btts_ht_prob >= 57.0:
    st.markdown(
        f"""
        <div class="flash-box-green">
            🟢 <b>BTTS 1° TEMPO TARGET 57% IN SU:</b><br>
            • Probabilità stimata: <span style="font-size:18px;"><b>{btts_ht_prob:.1f}%</b></span> (Over 0.5 HT: {over_05_ht_prob:.1f}%)<br>
            • <i>Soglia del 57% raggiunta o superata. Semaforo verde!</i>
        </div>
        """,
        unsafe_allow_html=True,
    )
  elif 45.0 <= btts_ht_prob < 57.0:
    st.markdown(
        f"""
        <div class="flash-box-yellow">
            🟡 <b>ZONA GRIGIA (45% - 56.9%):</b><br>
            • Probabilità stimata: <span style="font-size:18px;"><b>{btts_ht_prob:.1f}%</b></span> (Over 0.5 HT: {over_05_ht_prob:.1f}%)<br>
            • <i>Valore interessante ma sotto la soglia minima del 57%.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"""
        <div class="flash-box-red">
            🛡️ <b>SOTTO SOGLIA (< 45%):</b><br>
            • Probabilità stimata: <span style="font-size:18px;"><b>{btts_ht_prob:.1f}%</b></span> (Rischio 0-0 HT: {p_zero_ht:.1f}%)<br>
            • <i>Valore basso, scartato.</i>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.subheader("🎯 Top 5 Risultati Esatti (90')")
  cols = st.columns(5)
  for i in range(5):
    s = exact_scores_list[i]
    with cols[i]:
      st.metric(label=f"#{i+1} ({s[0]}-{s[1]})", value=f"{s[2]:.1f}%")

  st.markdown("---")
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Segno 1", f"{home_win_prob:.1f}%")
  m2.metric("Segno X", f"{draw_prob:.1f}%")
  m3.metric("Segno 2", f"{away_win_prob:.1f}%")
  m4.metric("Over 2.5", f"{over_25_prob:.1f}%")

  st.markdown(
      f""" <div class="pro-box"> 🔍 <b>DIAGNOSTICA 57 UP:</b><br>
    • xG 90' -> Casa: <b>{base_home_xg:.2f}</b> | Ospite: <b>{base_away_xg:.2f}</b> &nbsp;|&nbsp; BTTS Match: <b>{btts_match_prob:.1f}%</b><br>
    • xG 1° Tempo -> Casa: <b>{final_h_xg:.2f}</b> | Ospite: <b>{final_a_xg:.2f}</b> &nbsp;|&nbsp; BTTS HT (>= 57): <b>{btts_ht_prob:.1f}%</b>
    </div>""",
      unsafe_allow_html=True,
  )

else:
  st.info(
      "📌 Inserisci i dati e avvia la simulazione con il filtro a partire dal"
      " 57%."
  )
