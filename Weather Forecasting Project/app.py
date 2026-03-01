from flask_ngrok import run_with_ngrok
from flask import Flask, render_template_string
from flask import request
app = Flask(__name__)
run_with_ngrok(app) # Start ngrok when app is run

@app.route("/")
def dashboard():
    data = list(zip(
        pd.date_range(df_b_imputed.index[-1] + pd.Timedelta(days=1), periods=10, freq='D').strftime('%Y-%m-%d'),
        forecast_varma_b['tavg'].round(2).tolist(),
        ["Yes" if r == 1 else "No" for r in rain_pred_b]
    ))
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bangalore Forecast Dashboard</title>
        <style>
            body {
                font-family: sans-serif;
                background-color: #f4f4f4;
                margin: 20px;
            }
            h2 {
                color: #333;
                text-align: center;
                margin-bottom: 20px;
            }
            table {
                border-collapse: collapse;
                width: 80%;
                margin: 0 auto;
                background-color: #fff;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            th, td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h2>Bangalore Forecast Dashboard</h2>
        <table>
            <tr><th>Date</th><th>Temperature Avg (°C)</th><th>Will it Rain?</th></tr>
            {% for d, t, r in data %}
              <tr><td>{{ d }}</td><td>{{ t }}</td><td>{{ r }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    ''', data=data)