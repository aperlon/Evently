#!/usr/bin/env python3
"""
Evently - Servidor Simple de Predicción
Ejecuta sin necesidad de PostgreSQL

Uso: python server_simple.py
Luego abre: http://localhost:8000
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "backend"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

from app.ml.economic_impact_model import EconomicImpactModel

# Inicializar app
app = FastAPI(
    title="Evently - Predictor de Impacto Económico",
    description="Predice el impacto económico de eventos usando Machine Learning",
    version="1.0.0"
)

# CORS para permitir requests desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo ML
model = None

def get_model():
    global model
    if model is None:
        model = EconomicImpactModel()
        model.load()
    return model


# Schemas
class PredictionInput(BaseModel):
    event_type: str = Field(..., description="Tipo: sports, music, festival, culture, business, fair")
    city: str = Field(..., description="Ciudad")
    duration_days: int = Field(..., ge=1, le=365, description="Duración en días")
    attendance: Optional[int] = Field(None, ge=0, description="Asistencia esperada (opcional)")


# Página principal con interfaz web
@app.get("/", response_class=HTMLResponse)
async def home():
    m = get_model()
    cities = m.get_cities()
    event_types = m.get_event_types()

    cities_options = "\n".join([f'<option value="{c["name"]}">{c["name"]} ({c["country"]})</option>' for c in cities])
    types_options = "\n".join([f'<option value="{t}">{t.capitalize()}</option>' for t in event_types])

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Evently - Predictor de Impacto Económico</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            header {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
            header p {{ opacity: 0.8; }}
            .form-section {{
                padding: 30px;
            }}
            .form-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .form-group {{
                display: flex;
                flex-direction: column;
            }}
            label {{
                font-weight: 600;
                margin-bottom: 8px;
                color: #333;
            }}
            select, input {{
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                transition: border-color 0.3s;
            }}
            select:focus, input:focus {{
                outline: none;
                border-color: #667eea;
            }}
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                font-size: 18px;
                border-radius: 10px;
                cursor: pointer;
                width: 100%;
                font-weight: 600;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }}
            button:disabled {{
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }}
            #result {{
                margin-top: 30px;
                padding: 30px;
                background: #f8f9fa;
                border-radius: 15px;
                display: none;
            }}
            #result.show {{ display: block; }}
            .result-header {{
                text-align: center;
                margin-bottom: 25px;
            }}
            .result-header h2 {{
                color: #1a1a2e;
                font-size: 1.5em;
            }}
            .impact-amount {{
                font-size: 3em;
                font-weight: 700;
                color: #667eea;
                text-align: center;
                margin: 20px 0;
            }}
            .confidence {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .stat-card .value {{
                font-size: 1.5em;
                font-weight: 700;
                color: #1a1a2e;
            }}
            .stat-card .label {{
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }}
            .reference {{
                margin-top: 25px;
                padding: 15px;
                background: #e8f4f8;
                border-radius: 10px;
                font-size: 0.9em;
            }}
            .reference h4 {{ color: #1a1a2e; margin-bottom: 10px; }}
            .loading {{
                text-align: center;
                padding: 20px;
            }}
            .spinner {{
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🎯 Evently</h1>
                <p>Predictor de Impacto Económico de Eventos</p>
            </header>

            <div class="form-section">
                <form id="predictionForm">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="event_type">Tipo de Evento</label>
                            <select id="event_type" required>
                                {types_options}
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="city">Ciudad</label>
                            <select id="city" required>
                                {cities_options}
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="duration_days">Duración (días)</label>
                            <input type="number" id="duration_days" min="1" max="365" value="7" required>
                        </div>

                        <div class="form-group">
                            <label for="attendance">Asistencia (opcional)</label>
                            <input type="number" id="attendance" min="0" placeholder="Auto-estimado">
                        </div>
                    </div>

                    <button type="submit" id="submitBtn">Calcular Impacto Económico</button>
                </form>

                <div id="result"></div>
            </div>
        </div>

        <script>
            document.getElementById('predictionForm').addEventListener('submit', async (e) => {{
                e.preventDefault();

                const btn = document.getElementById('submitBtn');
                const resultDiv = document.getElementById('result');

                btn.disabled = true;
                btn.textContent = 'Calculando...';
                resultDiv.className = 'show';
                resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Procesando predicción...</p></div>';

                const data = {{
                    event_type: document.getElementById('event_type').value,
                    city: document.getElementById('city').value,
                    duration_days: parseInt(document.getElementById('duration_days').value),
                }};

                const attendance = document.getElementById('attendance').value;
                if (attendance) data.attendance = parseInt(attendance);

                try {{
                    const response = await fetch('/api/predict', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(data)
                    }});

                    const result = await response.json();

                    if (response.ok) {{
                        const formatMoney = (n) => '$' + n.toLocaleString('en-US', {{maximumFractionDigits: 0}});

                        resultDiv.innerHTML = `
                            <div class="result-header">
                                <h2>${{data.event_type.toUpperCase()}} en ${{data.city}}</h2>
                                <p>${{data.duration_days}} días${{data.attendance ? ' • ' + data.attendance.toLocaleString() + ' asistentes' : ''}}</p>
                            </div>

                            <div class="impact-amount">
                                ${{formatMoney(result.prediction.total_economic_impact_usd)}}
                            </div>

                            <div class="confidence">
                                Intervalo de confianza (90%): ${{formatMoney(result.prediction.lower_bound_usd)}} - ${{formatMoney(result.prediction.upper_bound_usd)}}
                            </div>

                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="value">${{formatMoney(result.breakdown.direct_spending_usd)}}</div>
                                    <div class="label">Gasto Directo</div>
                                </div>
                                <div class="stat-card">
                                    <div class="value">${{formatMoney(result.breakdown.indirect_spending_usd)}}</div>
                                    <div class="label">Gasto Indirecto</div>
                                </div>
                                <div class="stat-card">
                                    <div class="value">${{result.estimates.jobs_created.toLocaleString()}}</div>
                                    <div class="label">Empleos Creados</div>
                                </div>
                                <div class="stat-card">
                                    <div class="value">${{result.estimates.roi_ratio}}x</div>
                                    <div class="label">ROI Esperado</div>
                                </div>
                            </div>

                            <div class="reference">
                                <h4>📚 Basado en datos históricos</h4>
                                <p><strong>Referencia:</strong> ${{result.historical_reference.reference_scope}}</p>
                                <p><strong>Eventos similares:</strong> ${{result.historical_reference.similar_events.slice(0,3).join(', ') || 'N/A'}}</p>
                                <p><strong>Modelo:</strong> ${{result.model_info.model_used}} (R² = ${{result.model_info.model_r2}})</p>
                            </div>
                        `;
                    }} else {{
                        resultDiv.innerHTML = `<p style="color: red;">Error: ${{result.detail}}</p>`;
                    }}
                }} catch (error) {{
                    resultDiv.innerHTML = `<p style="color: red;">Error de conexión: ${{error.message}}</p>`;
                }}

                btn.disabled = false;
                btn.textContent = 'Calcular Impacto Económico';
            }});
        </script>
    </body>
    </html>
    """


@app.get("/api/options")
async def get_options():
    """Obtener opciones disponibles"""
    m = get_model()
    return {
        "event_types": m.get_event_types(),
        "cities": m.get_cities()
    }


@app.post("/api/predict")
async def predict(input_data: PredictionInput):
    """Hacer predicción de impacto económico"""
    m = get_model()
    try:
        result = m.predict_simple(
            event_type=input_data.event_type,
            city=input_data.city,
            duration_days=input_data.duration_days,
            attendance=input_data.attendance
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   EVENTLY - Servidor de Predicción")
    print("="*60)
    print("\n   Abre en tu navegador: http://localhost:8000")
    print("\n   Presiona Ctrl+C para detener\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
