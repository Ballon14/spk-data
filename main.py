from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

CSV_FILE = 'Dataset Package NodeJS - Dataset 25 November.csv'
CRITERIA = ['downloads_last_month', 'github_stars', 'package_size_kb', 'days_since_publish']

# 3 kriteria benefit, 1 cost (days_since_publish semakin kecil semakin baik)
WEIGHT_DEFAULT = [0.3, 0.3, 0.2, 0.2]  # Bisa diubah via input user

# Helper to parse package_size_kb field

def parse_pkg_size(val):
    try:
        if isinstance(val, str):
            val = val.replace(',', '.')
        return float(val)
    except Exception:
        return np.nan


def load_data():
    df = pd.read_csv(CSV_FILE)
    df['package_size_kb'] = df['package_size_kb'].apply(parse_pkg_size)
    df = df.dropna(subset=CRITERIA)  # Pastikan lengkap
    return df


def normalize(df):
    norm = pd.DataFrame()
    # Benefit (jenis max): downloads, github_star, package_size_kb
    for c in ['downloads_last_month', 'github_stars', 'package_size_kb']:
        # Jika seluruh nilai sama, akan di-normalisasi ke 1
        maxv = df[c].max()
        minv = df[c].min()
        norm[c] = (df[c] - minv) / (maxv - minv) if maxv != minv else 1
    # Cost (jenis min): days_since_publish (semakin baru = semakin kecil days)
    c = 'days_since_publish'
    maxv = df[c].max()
    minv = df[c].min()
    norm[c] = (maxv - df[c]) / (maxv - minv) if maxv != minv else 1
    return norm

@app.route('/rank', methods=['POST'])
def rank_packages():
    '''Input: JSON {"weights": [..float..] 4 elemen optional, default=WEIGHT_DEFAULT}
       Output: Ranking hasil SAW berdasarkan bobot.
    '''
    data = request.get_json(silent=True) or {}
    weights = data.get('weights', WEIGHT_DEFAULT)
    if len(weights) != 4:
        return jsonify({'error':'Length of weights must be 4'}), 400
    df = load_data()
    norm = normalize(df)
    saw_scores = np.dot(norm.values, np.array(weights))
    df['saw_score'] = saw_scores
    df_sorted = df.sort_values('saw_score', ascending=False).reset_index(drop=True)
    # Bisa tambah kolom yang ingin ditampilkan (misal name, score, dsb)
    result = df_sorted[['name','saw_score'] + CRITERIA].to_dict(orient='records')
    return jsonify(result)

@app.route('/')
def root():
    return 'SAW Flask API for NodeJS Packages', 200

if __name__ == '__main__':
    app.run(debug=True)
