from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np

app = Flask(__name__)

CSV_FILE = 'Dataset Package NodeJS - Dataset 25 November.csv'
CRITERIA = ['downloads_last_month', 'github_stars', 'package_size_kb', 'days_since_publish']
CR_LABELS = [
    'Downloads Bulan Lalu',
    'GitHub Stars',
    'Package Size (KB)',
    'Hari sejak Publish'
]
WEIGHT_DEFAULT = [0.3, 0.3, 0.2, 0.2]


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
    for c in ['downloads_last_month', 'github_stars', 'package_size_kb']:
        maxv = df[c].max()
        minv = df[c].min()
        norm[c] = (df[c] - minv) / (maxv - minv) if maxv != minv else 1
    c = 'days_since_publish'
    maxv = df[c].max()
    minv = df[c].min()
    norm[c] = (maxv - df[c]) / (maxv - minv) if maxv != minv else 1
    return norm

@app.route('/rank', methods=['POST'])
def rank_packages():
    data = request.get_json(silent=True) or {}
    weights = data.get('weights', WEIGHT_DEFAULT)
    if len(weights) != 4:
        return jsonify({'error':'Length of weights must be 4'}), 400
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
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>SPK SAW Package NodeJS</title>
        <style>
        body { font-family:sans-serif; background:#f8fafc; color:#24292f; margin:0; padding:0; }
        .container { max-width:730px;padding:32px;margin:auto; margin-top:40px; background:#fff; border-radius:10px; box-shadow:0 2px 12px #0001; }
        h2, h4 {color:#0c4880; margin-top: 0;}
        label { display:inline-block; margin-bottom:7px; }
        input[type=number] {width:80px; padding:4px 8px; margin-left:8px; border-radius:3px; border:1px solid #bcd;}
        button { background:#0a6efd; color:#fff; border:none; border-radius:5px; padding:8px 24px; font-size:1rem; cursor:pointer; margin-top:14px; }
        button:active, button:hover { background:#084082; }
        .bobot-info { font-size:0.96em; background:#eaf3fa; border-left:3px solid #2188c7; padding:8px 15px; margin:10px 0 13px 0; color:#13354b; border-radius:4px;}
        @media (max-width:670px) {
            .container{padding:8px;margin-top:8px;border-radius:0;}
        }
        table { border-collapse:collapse; width:100%; margin-top:26px; background:#fbfdfe; }
        th,td { border:1.4px solid #c3d6e3; padding:5px 8px; text-align:right; font-size:0.98em; }
        th:first-child,td:first-child { text-align:left; }
        th,thead {background:#f1f7fb; }
        tr.highlight { background:#dfefe2; font-weight:bold; }
        .errormsg {color:#ac2519;background:#ffd9d4;padding:8px;border-radius:4px;margin:7px 0;font-weight:bold;}
        </style>
      </head>
      <body>
      <div class="container">
        <h2>Sistem Pendukung Keputusan<br><small style="color:#629ad0;font-size:.75em;">Metode Simple Additive Weighting (SAW)</small></h2>
        <div class="bobot-info">
          <span>Masukkan bobot untuk keempat kriteria utama di bawah (jumlah total bobot harus <b>1.00</b>).</span><br>
          <ul style="margin-top:2px;margin-bottom:4px;">
            <li><b>Download Bulan Lalu</b>: semakin banyak semakin bagus</li>
            <li><b>GitHub Stars</b>: semakin banyak semakin bagus</li>
            <li><b>Package Size (KB)</b>: semakin kecil biasanya lebih efisien, namun bisa dianggap semakin besar semakin bagus jika butuh fitur lebih</li>
            <li><b>Hari sejak Publish</b>: semakin kecil semakin baru</li>
          </ul>
        </div>
        <form id="saw-form" autocomplete="off" style="margin-bottom:18px;">
          {% for lbl in labels %}
            <label>{{ lbl }}:
                <input name="w{{ loop.index0 }}" type="number" value="{{ default[loop.index0] }}" min="0" max="1" step="0.01" required>
            </label><br/>
          {% endfor %}
          <button type="submit">Hitung Ranking</button>
          <span id="form-error" class="errormsg" style="display:none;"></span>
        </form>
        <div id="result-section"></div>
      </div>
      <script>
      document.getElementById('saw-form').onsubmit = async function(ev){
        ev.preventDefault();
        let w=[], total=0;
        for(let i=0; i<4; i++){
          let val = parseFloat(this.elements['w'+i].value)||0;
          w.push(val);
          total+=val;
        }
        if(Math.abs(total-1.0) > 0.01){
            let err = document.getElementById('form-error');
            err.innerText = 'Jumlah total bobot harus 1.00 (sekarang: '+ total.toFixed(2)+')';
            err.style.display='';
            return;
        } else {
            document.getElementById('form-error').style.display='none';
        }
        const rs = await fetch('/rank', {
          method:'POST',
          body: JSON.stringify({weights: w}),
          headers:{'Content-Type':'application/json'}
        });
        const data = await rs.json();
        let html = '<h4>Ranking SPK</h4>';
        if(data.error){
            html += '<div class="errormsg">'+data.error+'</div>';
            document.getElementById('result-section').innerHTML = html;
            return;
        }
        html += '<table><thead><tr><th>Peringkat</th><th>Nama Package</th><th>Score SAW</th>' +
          {{ columns|tojson }}.slice(1).map(c=>'<th>'+c+'</th>').join('') + '</tr></thead><tbody>';
        let rownum = 0;
        for(let row of data){
          rownum++;
          html += `<tr${rownum==1?' class=highlight':''}><td>${rownum}</td><td>${row['name']}</td><td>${row['saw_score'].toFixed(4)}</td>` +
            [{{ crits|tojson }}[0],{{ crits|tojson }}[1],{{ crits|tojson }}[2],{{ crits|tojson }}[3]].map(c=>`<td>${row[c]}</td>`).join('') + '</tr>';
        }
        html += '</tbody></table>';
        document.getElementById('result-section').innerHTML = html;
        window.scrollTo({top:400,behavior:'smooth'});
      }
      </script>
      </body>
    </html>
    '''
    return render_template_string(
        html,
        default=WEIGHT_DEFAULT,
        labels=CR_LABELS,
        columns=['Nama Package','Skor SAW'] + CR_LABELS,
        crits=CRITERIA
    )

if __name__ == '__main__':
    app.run(debug=True)
