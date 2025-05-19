import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📁 데이터 불러오기
file_path = "data/bitcoin_etf_indicators.csv"
df = pd.read_csv(file_path, parse_dates=["Date"])

# ✅ 1. 기본 정보 출력
print("\n📌 데이터 기본 정보:")
print(df.info())

# ✅ 2. 결측치 확인
print("\n📌 결측치 확인:")
print(df.isnull().sum())

