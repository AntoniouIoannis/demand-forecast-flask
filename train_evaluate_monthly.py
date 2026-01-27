import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os
import json

def run_training_and_forecast(train_path, test_path, outdir):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    # Επιλογή στηλών που δημιουργήθηκαν στο preprocessing
    features = ['lag_1', 'lag_2', 'lag_3', 'roll_mean_3']
    target = 'ordered_qty'

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_df[features], train_df[target])

    test_df['forecast_qty'] = model.predict(test_df[features])
    
    # Προετοιμασία για JSON
    # Μέσα στη συνάρτηση run_training_and_forecast, άλλαξε τη γραμμή του output:
    output_data = test_df[['product_id', 'month_year', 'forecast_qty']].copy()
    output_data['month_year'] = output_data['month_year'].astype(str)
    
    json_list = output_data.to_dict(orient='records')
    output_file = os.path.join(outdir, "forecast_results.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_list, f, ensure_ascii=False, indent=4)
    
    return output_file
    