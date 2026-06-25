# 🕵️ 흡연 탐정 (Smoking Detective)

신체검사 수치만으로 흡연 여부를 간파하는 인터랙티브 웹앱 (Streamlit).

## 기능
- **🕵️ 수사하기**: 신체 수치 입력 → 흡연 의심도(%) 판결
- **📊 데이터 탐험**: 필터 + 분포·t검정·카이제곱·상관 히트맵
- **📖 측정 원리**: 상관계수·p값·효과크기·회귀·ROC/AUC를 쉬운 설명과 함께

## 데이터
Kaggle *Body signal of smoking* (kukuroo3) — 약 5.5만 명, 신체신호 → 흡연(0/1)

## 사용 기술
Streamlit · pandas · numpy · scipy · statsmodels · matplotlib · seaborn

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```
