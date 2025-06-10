import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("로지스틱 개체군 생장 곡선 시뮬레이션")

# 환경 저항 (수용력) 설정 슬라이더
K = st.slider("환경 저항 값 (수용력 K)", min_value=50, max_value=500, value=200, step=10)

# 초기 개체수
N0 = 10
# 성장률 (r)
r = 0.2
# 시간
t = np.linspace(0, 50, 500)

# 로지스틱 함수
def logistic_growth(t, N0, r, K):
    return K / (1 + ((K - N0)/N0) * np.exp(-r*t))

N = logistic_growth(t, N0, r, K)

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(t, N, label=f'K={K}')
ax.set_xlabel('시간 (t)')
ax.set_ylabel('개체수 (N)')
ax.set_title('로지스틱 개체군 생장 곡선')
ax.legend()
ax.grid(True)

st.pyplot(fig)
