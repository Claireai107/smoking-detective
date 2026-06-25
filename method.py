# -*- coding: utf-8 -*-
"""📖 측정 원리 — 흡연 탐정이 '어떻게' 판단하는지 단계별 설명.
이 페이지는 전체 데이터 기준이며 '데이터 탐험'의 필터와 무관합니다."""

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from helpers import load_data, train_model, compute_associations, roc_auc, FORMULA

st.title("📖 측정 원리")
st.write("흡연 탐정이 **어떤 조사 → 어떤 분석 → 어떤 모델**로 흡연을 간파하는지 설명합니다.")
st.caption("ℹ️ 이 페이지는 전체 데이터 기준입니다 (필터 영향 없음).")

df = load_data()

# 1단계 ──────────────────────────────────────────
st.header("1단계 · 어떤 신호가 흡연과 연관 큰가?")
st.markdown("""
각 신체신호마다 **흡연자 vs 비흡연자**를 비교해 3가지를 계산했습니다.

| 지표 | 의미 |
|---|---|
| **상관계수** | 흡연과 같이 움직이는 정도 (-1 ~ +1) |
| **t검정 p값** | 두 그룹 평균 차이가 우연인지 (p<0.05면 유의) |
| **Cohen's d (효과크기)** | 차이가 *실질적으로* 큰지 (0.2 작음·0.5 중간·**0.8 큼**) |
""")

with st.expander("🔎 상관계수가 뭐예요?"):
    st.markdown("두 가지가 **같이 움직이는 정도**예요. 키가 크면 발도 커지죠? → 키와 발은 '상관이 있다'고 해요. "
                "혈색소가 높을수록 담배 확률도 높으면 → 둘은 상관이 있어요. "
                "**+1에 가까울수록 같이 커지고, -1에 가까울수록 반대로 움직이며, 0이면 관계가 거의 없어요.**")
with st.expander("🔎 p값(유의확률)이 뭐예요?"):
    st.markdown("이 차이가 **'진짜'인지 '우연'인지** 알려주는 숫자예요. p값이 아주 작으면(0.05보다 작으면) "
                "→ \"우연이 아니라 진짜 차이!\" 라는 뜻이에요. "
                "동전을 10번 던졌는데 10번 다 앞면이면 \"이거 좀 이상한데?\" 싶죠? 그게 바로 p값이 작은 거예요.")
with st.expander("🔎 효과크기(Cohen's d)가 뭐예요?"):
    st.markdown("차이가 **얼마나 큰지**를 알려줘요. 키가 1cm 다른 건 작은 차이지만 30cm 다르면 큰 차이죠? "
                "이 숫자가 **0.8을 넘으면 \"차이가 눈에 확 띈다\"** 는 뜻이에요. "
                "p값은 '차이가 있냐 없냐', 효과크기는 '차이가 크냐 작냐'를 봅니다.")

assoc = compute_associations(df)
view = assoc.copy()
view["p값"] = view["p값"].apply(lambda x: f"{x:.1e}")
st.dataframe(view, width="stretch")

st.subheader("📊 연관성 한눈에 (상관계수 절댓값)")
top = assoc.head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#E8453C" if abs(c) >= 0.25 else "#9aa0a6" for c in top["상관계수"]]
ax.barh(top["변수"], top["상관계수"].abs(), color=colors)
ax.set_xlabel("|상관계수| (흡연과의 연관 강도)")
st.pyplot(fig)

# 2단계 ──────────────────────────────────────────
st.header("2단계 · ⚠️ '키'의 함정 — 교란변수")
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("""
키·몸무게가 상위권에 보이지만 **'키가 크면 담배를 핀다'는 뜻이 아닙니다.**

오른쪽 표처럼 **남성 흡연율이 여성의 13배**예요. 흡연자는 대부분 남성 →
남성이 키·몸무게가 큼 → '키'가 흡연과 연관된 *척* 보이는 것뿐입니다.

이렇게 숨어서 관계를 부풀리는 제3의 변수를 **교란변수(confounder)** 라 하고,
이런 함정은 **다중공선성(VIF)** 이라는 방법으로 걸러낼 수 있습니다.

➡️ 그래서 키·몸무게를 빼면, 흡연이 *생리적으로 직접* 바꾸는 진짜 신호는
**혈색소 · GTP · 중성지방 · HDL** 입니다.
""")
with col2:
    rate = pd.crosstab(df["성별"], df["흡연여부"], normalize="index").mul(100).round(1)
    st.markdown("**성별 흡연율 (%)**")
    st.dataframe(rate)
    st.caption("카이제곱 p ≈ 0 → 성별과 흡연은 강하게 연관")

with st.expander("🔎 교란변수가 뭐예요?"):
    st.markdown("어떤 결과를 만든 **숨은 진짜 범인**이에요. '키 큰 사람이 담배를 많이 핀다'처럼 보여도, "
                "사실은 **남자**가 담배를 많이 피우고 남자가 키가 커서 그렇게 보이는 거예요. "
                "진짜 범인은 '성별'이지 '키'가 아니죠. 이렇게 숨어서 가짜 관계를 만드는 변수가 교란변수예요. "
                "똑똑한 탐정은 성별을 함께 고려해서 이런 함정에 속지 않아요!")

# 3단계 ──────────────────────────────────────────
st.header("3단계 · 탐정은 어떻게 '흡연 의심도'를 내나?")
st.markdown("2단계에서 고른 강한 신호로 **회귀모델**을 학습합니다 (`smf.ols(...).fit()`).")
st.code(f'model = smf.ols("{FORMULA}", data=df).fit()\nscore = model.predict(용의자)   # 0~1 흡연 의심도', language="python")

model = train_model(df)
st.markdown("**학습된 회귀계수** (양수일수록 흡연 가능성 ↑):")
st.dataframe(model.params.round(4).rename("계수").to_frame(), width="stretch")
with st.expander("🔎 계수가 뭐예요?"):
    st.markdown("각 숫자가 판단에 **얼마나 힘을 보태는지**예요. 계수가 **+(플러스)면 그 수치가 높을수록 "
                "'흡연 쪽으로 미는 힘'**, **-(마이너스)면 '비흡연 쪽으로 미는 힘'** 입니다. "
                "단, 변수마다 단위가 달라 계수 크기끼리 직접 비교는 하지 않고, 연관 강도는 1단계의 상관/효과크기로 봅니다.")

# 4단계 ──────────────────────────────────────────
st.header("4단계 · 탐정을 얼마나 믿을까? (ROC / AUC)")
fpr, tpr, auc = roc_auc(df)
c1, c2 = st.columns([2, 3])
with c1:
    st.metric("이 탐정의 AUC", f"{auc:.3f}")
    st.markdown("""
- **민감도**: 진짜 흡연자를 잡아낸 비율 (검거율)
- **특이도**: 비흡연자를 무고하게 풀어준 비율
- 기준점을 바꾸면 둘이 시소처럼 맞바뀜 → 그 궤적이 ROC 곡선
- 왼쪽 위로 붙을수록(AUC 1에 가까울수록) 우수
- 0.5 동전던지기 · 0.7~0.8 양호 · 0.9+ 우수
""")
with c2:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(fpr, tpr, color="#E8453C", lw=2, label=f"AUC = {auc:.3f}")
    ax.plot([0, 1], [0, 1], "--", color="gray")
    ax.set_xlabel("거짓양성률 (1-특이도)"); ax.set_ylabel("민감도")
    ax.set_title("탐정 ROC 곡선"); ax.legend()
    st.pyplot(fig)

with st.expander("🔎 AUC가 뭐예요?"):
    st.markdown("탐정이 **얼마나 똑똑한지 매긴 시험 점수**예요. 0.5점은 그냥 찍기(동전 던지기), "
                f"1.0점은 백발백중 천재! 우리 탐정은 **{auc:.2f}점** 이라 꽤 잘하는 탐정이에요.")

st.success("정리: 조사(그룹 비교) → 분석(상관·t검정·효과크기) → 교란변수 제거 → 회귀 예측 → ROC/AUC 검증 순서로 작동합니다.")
