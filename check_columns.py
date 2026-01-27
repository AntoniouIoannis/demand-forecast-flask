import pandas as pd

# Δοκιμάζουμε να διαβάσουμε το αρχείο του 2017 από τον φάκελο data
try:
    file_path = "data/sales 2017.xlsx"
    df = pd.read_excel(file_path, engine='openpyxl', nrows=5)
    print("\n--- Στήλες που βρέθηκαν στο Excel ---")
    print(df.columns.tolist())
    print("\n--- Πρώτες γραμμές ---")
    print(df.head())
except Exception as e:
    print(f"Σφάλμα κατά την ανάγνωση: {e}")
    