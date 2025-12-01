import pandas as pd

CSV_PATH = r"C:\train_health_risk1.py\sleep_health_and_lifestyle.csv"  # exact path
df = pd.read_csv(CSV_PATH)
print(df.head())
