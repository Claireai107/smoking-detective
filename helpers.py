# -*- coding: utf-8 -*-
"""공용 함수 — 데이터 로딩 · 모델 학습 · 연관성 분석 · ROC/AUC
home.py · explore.py · method.py 가 함께 사용합니다."""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy import stats
import statsmodels.formula.api as smf

# 한글 깨짐 방지 — 윈도우(Malgun Gothic)·배포 리눅스(NanumGothic) 모두 대응
_available = {f.name for f in fm.fontManager.ttflist}
for _cand in ["Malgun Gothic", "NanumGothic", "AppleGothic", "DejaVu Sans"]:
    if _cand in _available:
        plt.rcParams["font.family"] = _cand
        break
plt.rcParams["axes.unicode_minus"] = False

# 분석으로 고른 '강한 흡연 신호' + 성별(C로 범주 처리)
NUM_FEATURES = ["hemoglobin", "Gtp", "triglyceride", "HDL"]
FORMULA = "smoking ~ hemoglobin + Gtp + triglyceride + HDL + C(gender)"


def fmt_p(p):
    """p값을 읽기 좋게 — 너무 작으면 0으로 뭉개지지 않게 '< 0.001' 로 표시."""
    if p < 0.001:
        return "< 0.001"
    return f"{p:.4f}"


@st.cache_data
def load_data():
    df = pd.read_csv("smoking.csv")
    df["흡연여부"] = df["smoking"].map({0: "비흡연", 1: "흡연"})
    df["성별"] = df["gender"].map({"M": "남성", "F": "여성"}).fillna(df["gender"].astype(str))
    return df


@st.cache_data
def train_model(df):
    """회귀모델 학습 — smf.ols('타깃 ~ 변수들').fit() 으로 흡연 의심도를 예측."""
    return smf.ols(FORMULA, data=df).fit()


@st.cache_data
def compute_associations(df):
    """각 신체신호와 흡연의 연관성 = 상관계수 + t검정 + Cohen's d.
    (상관계수 · t검정 · 효과크기를 변수마다 한 번에 계산)"""
    num_cols = [c for c in df.select_dtypes("number").columns if c not in ("ID", "smoking")]
    rows = []
    for c in num_cols:
        g_non = df[df["smoking"] == 0][c].dropna()
        g_smk = df[df["smoking"] == 1][c].dropna()
        corr = df[[c, "smoking"]].corr().iloc[0, 1]            # 상관계수
        t, p = stats.ttest_ind(g_non, g_smk, equal_var=False)   # Welch t검정
        n1, n2 = len(g_non), len(g_smk)
        sp = np.sqrt(((n1 - 1) * g_non.std() ** 2 + (n2 - 1) * g_smk.std() ** 2) / (n1 + n2 - 2))
        d = (g_smk.mean() - g_non.mean()) / sp                  # Cohen's d (효과크기)
        rows.append({"변수": c, "상관계수": round(corr, 3),
                     "비흡연평균": round(g_non.mean(), 2), "흡연평균": round(g_smk.mean(), 2),
                     "Cohen_d": round(d, 3), "p값": p})
    res = pd.DataFrame(rows)
    res = res.reindex(res["상관계수"].abs().sort_values(ascending=False).index)
    return res.reset_index(drop=True)


@st.cache_data
def roc_auc(df):
    """전체 데이터로 학습한 모델의 ROC 좌표와 AUC (기준점을 바꿔가며 직접 계산)."""
    model = train_model(df)
    proba = np.clip(model.predict(df), 0, 1)
    y = df["smoking"].values
    ths = np.linspace(0, 1, 101)
    tpr = [((proba >= t) & (y == 1)).sum() / max((y == 1).sum(), 1) for t in ths]
    fpr = [((proba >= t) & (y == 0)).sum() / max((y == 0).sum(), 1) for t in ths]
    auc = float(np.trapezoid(sorted(tpr), sorted(fpr)))
    return fpr, tpr, auc
