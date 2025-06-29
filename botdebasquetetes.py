import streamlit as st
import math

st.set_page_config(page_title="Bot de Handicap - Basquete Real", layout="centered")

st.title("🏀 Bot de Handicap - Basquete Real")

quarto = st.number_input("📍 Quarto Atual", min_value=1, max_value=4, step=1)

st.markdown("## 📊 Pontos por Quarto")
pontos_A = []
pontos_B = []
for i in range(1, 5):
    col1, col2 = st.columns(2)
    with col1:
        pontos_A.append(st.number_input(f"Q{i} - Time A", min_value=0))
    with col2:
        pontos_B.append(st.number_input(f"Q{i} - Time B", min_value=0))

st.markdown("## 📈 Handicaps")
col1, col2 = st.columns(2)
with col1:
    handicapA = st.text_input("Handicap Time A", value="-2.5")
with col2:
    handicapB = st.text_input("Handicap Time B", value="+2.5")

st.markdown("## 🎯 Estatísticas")
col1, col2 = st.columns(2)
with col1:
    fgA = st.text_input("FG Time A (ex: 22/45)", value="22/45")
    fg3A = st.text_input("3PT Time A (ex: 6/18)", value="6/18")
    rebA = st.number_input("Rebotes A", min_value=0)
    astA = st.number_input("Assistências A", min_value=0)
    stlA = st.number_input("Roubos A", min_value=0)
    blkA = st.number_input("Bloqueios A", min_value=0)
    tovA = st.number_input("Turnovers A", min_value=0)
    leadA = st.number_input("Maior Vantagem A", min_value=0)
    changesA = st.number_input("🔁 Mudanças de liderança A", min_value=0)

with col2:
    fgB = st.text_input("FG Time B (ex: 20/48)", value="20/48")
    fg3B = st.text_input("3PT Time B (ex: 5/15)", value="5/15")
    rebB = st.number_input("Rebotes B", min_value=0)
    astB = st.number_input("Assistências B", min_value=0)
    stlB = st.number_input("Roubos B", min_value=0)
    blkB = st.number_input("Bloqueios B", min_value=0)
    tovB = st.number_input("Turnovers B", min_value=0)
    leadB = st.number_input("Maior Vantagem B", min_value=0)
    changesB = st.number_input("🔁 Mudanças de liderança B", min_value=0)

def parse_fg(texto):
    try:
        feito, tentado = map(int, texto.strip().split("/"))
        return (feito / tentado) * 100 if tentado > 0 else 0
    except:
        return 0

def performance(fg, fg3, reb, ast, stl, blk, tov, lead):
    return (0.25*fg + 0.15*fg3 + 0.15*reb + 0.10*ast + 0.10*stl + 0.05*blk + 0.10*lead - 0.20*tov)

def sigmoide(x):
    return 1 / (1 + math.exp(-x))

if st.button("🎯 Gerar Sugestão"):
    try:
        hA = float(handicapA)
        hB = float(handicapB)
    except:
        st.error("⚠️ Handicaps inválidos")
        st.stop()

    total_A = sum(pontos_A)
    total_B = sum(pontos_B)
    diff = total_A - total_B
    q = quarto
    media = diff / q if q > 0 else 0

    proj_A = total_A + (media * (4 - q)/2)
    proj_B = total_B - (media * (4 - q)/2)
    margem_A = (proj_A + hA) - proj_B
    margem_B = (proj_B + hB) - proj_A

    fgA_val = parse_fg(fgA)
    fg3A_val = parse_fg(fg3A)
    fgB_val = parse_fg(fgB)
    fg3B_val = parse_fg(fg3B)

    perfA = performance(fgA_val, fg3A_val, rebA, astA, stlA, blkA, tovA, leadA)
    perfB = performance(fgB_val, fg3B_val, rebB, astB, stlB, blkB, tovB, leadB)
    perf_diff = perfA - perfB

    total_changes = changesA + changesB
    ajuste = max(0.9, 1 - total_changes * 0.02)

    chanceA = sigmoide((perf_diff + margem_A)/2.5) * ajuste
    chanceB = sigmoide((-perf_diff + margem_B)/2.5) * ajuste

    st.markdown(f"""
## 📌 Resultado da Análise
🏀 Total Time A: {total_A} | Total Time B: {total_B}  
📉 Diferença: {diff:+}  
📏 Margem A: {margem_A:+.1f} | Margem B: {margem_B:+.1f}  
📊 Índice A: {perfA:.1f} | Índice B: {perfB:.1f}  
✅ Chance A: {chanceA*100:.1f}% | Chance B: {chanceB*100:.1f}%
""")

    if chanceA > 0.7:
        st.success(f"✅ Sugestão: Apostar no Time A com handicap {hA:+}")
    elif chanceB > 0.7:
        st.success(f"✅ Sugestão: Apostar no Time B com handicap {hB:+}")
    elif 0.6 < chanceA <= 0.7:
        st.warning(f"⚠️ Aposta moderada no Time A com handicap {hA:+}")
    elif 0.6 < chanceB <= 0.7:
        st.warning(f"⚠️ Aposta moderada no Time B com handicap {hB:+}")
    else:
        st.error("❌ Melhor evitar aposta neste momento.")
