from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np

app = Flask(__name__)

CSV_FILE = 'Dataset_10_Desember.csv'
CRITERIA = ['days_since_publish', 'interoperability_score', 'package_size_kb', 'readme_length', 'github_stars']
CR_LABELS = [
    'Keamanan (Hari sejak Publish)',
    'Interoperabilitas',
    'Efisiensi (Package Size KB)',
    'Dokumentasi (README Length)',
    'Popularitas (GitHub Stars)'
]
WEIGHT_DEFAULT = [0.46, 0.26, 0.15, 0.09, 0.04]


def parse_pkg_size(val):
    try:
        if isinstance(val, str):
            val = val.replace(',', '.')
        return float(val)
    except Exception:
        return np.nan

def load_data():
    df = pd.read_csv(CSV_FILE, delimiter='\t')
    df['package_size_kb'] = df['package_size_kb'].apply(parse_pkg_size)
    df = df.dropna(subset=CRITERIA)  # Pastikan lengkap
    return df

def normalize(df):
    norm = pd.DataFrame()
    # Benefit criteria: higher is better (interoperability_score, readme_length, github_stars)
    for c in ['interoperability_score', 'readme_length', 'github_stars']:
        maxv = df[c].max()
        minv = df[c].min()
        norm[c] = (df[c] - minv) / (maxv - minv) if maxv != minv else 1
    # Cost criteria: lower is better (days_since_publish, package_size_kb)
    for c in ['days_since_publish', 'package_size_kb']:
        maxv = df[c].max()
        minv = df[c].min()
        norm[c] = (maxv - df[c]) / (maxv - minv) if maxv != minv else 1
    return norm

@app.route('/rank', methods=['POST'])
def rank_packages():
    data = request.get_json(silent=True) or {}
    weights = data.get('weights', WEIGHT_DEFAULT)
    if len(weights) != 5:
        return jsonify({'error':'Length of weights must be 5'}), 400
    if not np.isclose(sum(weights), 1.0):
        return jsonify({'error': 'Jumlah total bobot harus 1.00'}), 400
    df = load_data()
    norm = normalize(df)
    saw_scores = np.dot(norm.values, np.array(weights))
    df['saw_score'] = saw_scores
    df_sorted = df.sort_values('saw_score', ascending=False).reset_index(drop=True)
    result = df_sorted[['name','saw_score'] + CRITERIA].to_dict(orient='records')
    return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    html = '''
    <!doctype html>
    <html lang="id" class="scroll-smooth">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>SPK SAW - Analisis Package NodeJS</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
          * { font-family: 'Inter', sans-serif; }
          .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          }
          .gradient-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
          }
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
          }
          .glass {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
          }
          input[type="number"]::-webkit-inner-spin-button,
          input[type="number"]::-webkit-outer-spin-button {
            opacity: 1;
          }
          .rank-badge {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
          }
          .rank-2 {
            background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
          }
          .rank-3 {
            background: linear-gradient(135deg, #cd7f32 0%, #daa520 100%);
          }
        </style>
      </head>
      <body class="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 min-h-screen">
        <!-- Header -->
        <div class="gradient-bg text-white py-8 shadow-2xl">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center fade-in-up">
              <h1 class="text-4xl md:text-5xl font-bold mb-2">🎯 Sistem Pendukung Keputusan</h1>
              <p class="text-xl md:text-2xl font-light opacity-90">Analisis Package NodeJS dengan Metode SAW</p>
              <p class="text-sm mt-2 opacity-75">Simple Additive Weighting - Decision Support System</p>
            </div>
          </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          <!-- Info Card -->
          <div class="glass rounded-2xl shadow-xl p-6 md:p-8 mb-8 fade-in-up">
            <div class="flex items-start space-x-3 mb-4">
              <div class="bg-blue-500 text-white rounded-lg p-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-bold text-gray-800 mb-2">Kriteria Penilaian Package</h3>
                <p class="text-gray-600 mb-4">Masukkan bobot untuk setiap kriteria. <span class="font-semibold text-purple-600">Total harus 1.00</span></p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div class="gradient-card rounded-lg p-4 border border-purple-200">
                <div class="flex items-center mb-2">
                  <span class="text-2xl mr-2">🛡️</span>
                  <h4 class="font-semibold text-gray-800">Keamanan</h4>
                </div>
                <p class="text-sm text-gray-600">Hari sejak publish - Semakin baru semakin aman</p>
                <p class="text-xs text-purple-600 mt-1 font-medium">Default: 0.46 (46%)</p>
              </div>
              
              <div class="gradient-card rounded-lg p-4 border border-purple-200">
                <div class="flex items-center mb-2">
                  <span class="text-2xl mr-2">🔗</span>
                  <h4 class="font-semibold text-gray-800">Interoperabilitas</h4>
                </div>
                <p class="text-sm text-gray-600">Kompatibilitas dengan dependencies</p>
                <p class="text-xs text-purple-600 mt-1 font-medium">Default: 0.26 (26%)</p>
              </div>
              
              <div class="gradient-card rounded-lg p-4 border border-purple-200">
                <div class="flex items-center mb-2">
                  <span class="text-2xl mr-2">⚡</span>
                  <h4 class="font-semibold text-gray-800">Efisiensi</h4>
                </div>
                <p class="text-sm text-gray-600">Ukuran package - Semakin kecil semakin baik</p>
                <p class="text-xs text-purple-600 mt-1 font-medium">Default: 0.15 (15%)</p>
              </div>
              
              <div class="gradient-card rounded-lg p-4 border border-purple-200">
                <div class="flex items-center mb-2">
                  <span class="text-2xl mr-2">📚</span>
                  <h4 class="font-semibold text-gray-800">Dokumentasi</h4>
                </div>
                <p class="text-sm text-gray-600">Panjang README - Semakin lengkap semakin baik</p>
                <p class="text-xs text-purple-600 mt-1 font-medium">Default: 0.09 (9%)</p>
              </div>
              
              <div class="gradient-card rounded-lg p-4 border border-purple-200">
                <div class="flex items-center mb-2">
                  <span class="text-2xl mr-2">⭐</span>
                  <h4 class="font-semibold text-gray-800">Popularitas</h4>
                </div>
                <p class="text-sm text-gray-600">GitHub stars - Dukungan komunitas</p>
                <p class="text-xs text-purple-600 mt-1 font-medium">Default: 0.04 (4%)</p>
              </div>
            </div>
          </div>

          <!-- Form Card -->
          <div class="glass rounded-2xl shadow-xl p-6 md:p-8 mb-8 fade-in-up" style="animation-delay: 0.2s">
            <h3 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span class="bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-lg p-2 mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
                </svg>
              </span>
              Input Bobot Kriteria
            </h3>
            <form id="saw-form" autocomplete="off">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {% for lbl in labels %}
                <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">{{ lbl }}</label>
                  <input 
                    name="w{{ loop.index0 }}" 
                    type="number" 
                    value="{{ default[loop.index0] }}" 
                    min="0" 
                    max="1" 
                    step="0.01" 
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 hover:border-purple-300"
                  >
                </div>
                {% endfor %}
              </div>
              
              <div id="weight-sum" class="mt-6 p-4 bg-gray-100 rounded-lg">
                <div class="flex justify-between items-center">
                  <span class="text-gray-700 font-medium">Total Bobot:</span>
                  <span id="total-display" class="text-2xl font-bold text-purple-600">1.00</span>
                </div>
              </div>
              
              <div id="form-error" class="hidden mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg flex items-center">
                <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                <span id="error-text"></span>
              </div>
              
              <button type="submit" class="mt-6 w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold py-4 px-6 rounded-lg shadow-lg transform transition-all duration-200 hover:scale-105 hover:shadow-xl flex items-center justify-center space-x-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                </svg>
                <span>Hitung Ranking SAW</span>
              </button>
            </form>
          </div>

          <!-- Results Section -->
          <div id="result-section"></div>
        </div>

        <script>
        // Update total weight display
        function updateTotal() {
          let total = 0;
          for(let i=0; i<5; i++){
            const val = parseFloat(document.querySelector(`input[name="w${i}"]`).value) || 0;
            total += val;
          }
          const display = document.getElementById('total-display');
          display.textContent = total.toFixed(2);
          if(Math.abs(total - 1.0) > 0.01) {
            display.classList.remove('text-purple-600');
            display.classList.add('text-red-600');
          } else {
            display.classList.remove('text-red-600');
            display.classList.add('text-purple-600');
          }
        }
        
        // Add event listeners to inputs
        document.querySelectorAll('input[type="number"]').forEach(input => {
          input.addEventListener('input', updateTotal);
        });
        
        document.getElementById('saw-form').onsubmit = async function(ev){
          ev.preventDefault();
          let w=[], total=0;
          for(let i=0; i<5; i++){
            let val = parseFloat(this.elements['w'+i].value)||0;
            w.push(val);
            total+=val;
          }
          if(Math.abs(total-1.0) > 0.01){
              const err = document.getElementById('form-error');
              document.getElementById('error-text').innerText = 'Jumlah total bobot harus 1.00 (sekarang: '+ total.toFixed(2)+')';
              err.classList.remove('hidden');
              return;
          } else {
              document.getElementById('form-error').classList.add('hidden');
          }
          
          // Show loading
          document.getElementById('result-section').innerHTML = `
            <div class="glass rounded-2xl shadow-xl p-12 text-center fade-in-up">
              <div class="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-purple-500"></div>
              <p class="mt-4 text-gray-600 font-medium">Menghitung ranking packages...</p>
            </div>
          `;
          
          const rs = await fetch('/rank', {
            method:'POST',
            body: JSON.stringify({weights: w}),
            headers:{'Content-Type':'application/json'}
          });
          const data = await rs.json();
          
          if(data.error){
              document.getElementById('result-section').innerHTML = `
                <div class="glass rounded-2xl shadow-xl p-6 fade-in-up">
                  <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    <span>${data.error}</span>
                  </div>
                </div>
              `;
              return;
          }
          
          let html = `
            <div class="glass rounded-2xl shadow-xl p-6 md:p-8 fade-in-up">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-2xl md:text-3xl font-bold text-gray-800 flex items-center">
                  <span class="bg-gradient-to-r from-green-400 to-blue-500 text-white rounded-lg p-2 mr-3">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                    </svg>
                  </span>
                  Hasil Ranking Packages
                </h3>
                <span class="text-sm text-gray-600">${data.length} packages</span>
              </div>
              
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="bg-gradient-to-r from-purple-500 to-indigo-500 text-white">
                      <th class="px-4 py-3 text-left rounded-tl-lg">Rank</th>
                      <th class="px-4 py-3 text-left">Package Name</th>
                      <th class="px-4 py-3 text-center">Score SAW</th>
                      <th class="px-4 py-3 text-center">Keamanan</th>
                      <th class="px-4 py-3 text-center">Interop</th>
                      <th class="px-4 py-3 text-center">Efisiensi</th>
                      <th class="px-4 py-3 text-center">Dok</th>
                      <th class="px-4 py-3 text-center rounded-tr-lg">Pop</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
          `;
          
          let rownum = 0;
          for(let row of data){
            rownum++;
            const isTop3 = rownum <= 3;
            const rankClass = rownum === 1 ? 'rank-badge' : rownum === 2 ? 'rank-2' : rownum === 3 ? 'rank-3' : 'bg-gray-100';
            const rowClass = isTop3 ? 'bg-gradient-to-r from-yellow-50 to-amber-50' : (rownum % 2 === 0 ? 'bg-white' : 'bg-gray-50');
            const medal = rownum === 1 ? '🥇' : rownum === 2 ? '🥈' : rownum === 3 ? '🥉' : '';
            
            html += `
              <tr class="${rowClass} hover:bg-purple-50 transition-colors duration-150">
                <td class="px-4 py-3">
                  <div class="flex items-center space-x-2">
                    <span class="${rankClass} text-gray-800 font-bold px-3 py-1 rounded-full text-sm shadow-sm">${rownum}</span>
                    ${medal ? `<span class="text-2xl">${medal}</span>` : ''}
                  </div>
                </td>
                <td class="px-4 py-3 font-medium text-gray-800">${row['name']}</td>
                <td class="px-4 py-3 text-center">
                  <span class="bg-purple-100 text-purple-800 font-bold px-3 py-1 rounded-full text-sm">
                    ${row['saw_score'].toFixed(4)}
                  </span>
                </td>
                <td class="px-4 py-3 text-center text-gray-600">${row['days_since_publish']}</td>
                <td class="px-4 py-3 text-center text-gray-600">${row['interoperability_score']}</td>
                <td class="px-4 py-3 text-center text-gray-600">${row['package_size_kb'].toFixed(2)}</td>
                <td class="px-4 py-3 text-center text-gray-600">${row['readme_length']}</td>
                <td class="px-4 py-3 text-center text-gray-600">${row['github_stars'] || 'N/A'}</td>
              </tr>
            `;
          }
          
          html += `
                  </tbody>
                </table>
              </div>
            </div>
          `;
          
          document.getElementById('result-section').innerHTML = html;
          document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        </script>
      </body>
    </html>
    '''
    return render_template_string(
        html,
        default=WEIGHT_DEFAULT,
        labels=CR_LABELS,
        columns=['Skor SAW'] + CR_LABELS,
        crits=CRITERIA
    )

if __name__ == '__main__':
    app.run(debug=True)
