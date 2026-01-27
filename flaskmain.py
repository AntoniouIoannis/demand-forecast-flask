import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Εισαγωγή των συναρτήσεων από τα scripts σου
from preprocess_sales import run_preprocessing_pipeline
from train_evaluate_monthly import run_training_and_forecast

app = Flask(__name__)
CORS(app)  # Απαραίτητο για τη σύνδεση με FlutterFlow

# Ρυθμίσεις φακέλων βάσει της δομής σου
UPLOAD_FOLDER = 'ff_import_files'
OUTPUT_FOLDER = 'output'

@app.route('/forecast', methods=['POST'])
def full_pipeline():
    try:
        # 1. Παραλαβή αρχείων από το FlutterFlow
        if 'sales2017' not in request.files or 'sales2018' not in request.files or 'sales2019' not in request.files:
            return jsonify({"error": "Missing files"}), 400

        file_paths = {}
        for year in ['2017', '2018', '2019']:
            file = request.files[f'sales{year}']
            path = os.path.join(UPLOAD_FOLDER, f"sales_{year}.xlsx")
            file.save(path)
            file_paths[year] = path

        # 2. BHMA 1: Preprocessing
        # Μετατρέπει τα Excel σε train_with_roll.csv και test_with_roll.csv
        train_csv, test_csv = run_preprocessing_pipeline(
            sales_files=file_paths,
            outdir=OUTPUT_FOLDER
        )

        # 3. BHMA 2: Training & Forecasting
        # Εκπαιδεύει το μοντέλο και παράγει το forecast_results.json
        json_results_path = run_training_and_forecast(
            train_path=train_csv,
            test_path=test_csv,
            outdir=OUTPUT_FOLDER
        )

        # 4. Ανάγνωση του τελικού JSON για επιστροφή στο FlutterFlow
        with open(json_results_path, 'r', encoding='utf-8') as f:
            forecast_data = json.load(f)

        return jsonify({
            "status": "success",
            "message": "Process completed!",
            "results": forecast_data  # Αυτά τα δεδομένα θα εμφανιστούν στο Results tab
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Βεβαιώσου ότι οι φάκελοι υπάρχουν
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    app.run(debug=True, port=5000)
    