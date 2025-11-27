# Evently - Analizador de Impacto de Eventos

## Hola Ramiro Rego y Juan José Sáez (Corporate Intelligence)
Este repositorio respalda la asignatura “Corporate Intelligence” con una pila completa que analiza el impacto económico y turístico de grandes eventos en ciudades globales. Aquí encontrarán los artefactos necesarios para entender el flujo de datos, entrenar modelos, desplegar la aplicación y responder preguntas de inteligencia sobre ROI, ocupación hotelera y movilidad.

## ¿De qué trata Evently?
Evently combina un frontend React con un backend FastAPI y modelos de machine learning para:

- Visualizar el impacto de eventos históricos y sintéticos sobre turismo, ocupación hotelera y economía.
- Permitir simulaciones what-if donde se varían ciudad, tipo de evento, duración y asistencia para anticipar impacto económico.
- Exponer APIs, un predictor interactivo y un servidor simple para prototipado rápido sin PostgreSQL.

## Organización general

- `backend/`: API REST, lógica de análisis y modelos de machine learning.
- `frontend/`: dashboard React con globo 3D y páginas de análisis comparativo.
- `scripts/data/`: scripts para generar/afinar eventos sintéticos, sincronizar `events.csv` y ajustar datos.
- `scripts/ml/`: herramientas de entrenamiento, visualización de métricas, recomendaciones de features y predicción desde consola o FastAPI ligera.
- `data/examples/` y `data/outputs/`: CSVs base y artefactos derivados (como `feature_recommendations.json`).
- `docs/`: guías detalladas (`INSTRUCCIONES_RAPIDAS.md`, `MODELO_ML_DOCUMENTACION.md`, `BACKEND_PREDICTION_DOCUMENTATION.md`).
- `docker-compose.yml`, `start.sh/.ps1`, `dev.sh`: scripts de puesta en marcha.
- `railway.json`, `vercel.json`: configuraciones listas para desplegar backend y frontend respectivamente.

## Cómo correr el proyecto

### Opción recomendada: Docker
1. Verifiquen Docker y Docker Compose: `docker --version` y `docker-compose --version`.
2. Ejecución: `chmod +x start.sh && ./start.sh` (Linux/WSL/Mac) o `.\start.ps1` (PowerShell).
3. La salida mostrará `✅ EVENTLY IS READY!`; entonces ya está disponible:
   - Frontend: http://localhost:3000
   - Backend (API): http://localhost:8000
   - Docs Swagger: http://localhost:8000/api/v1/docs
4. Para parar los servicios: `docker-compose down`.

### Opción alternativa: ejecución manual
1. Crear PostgreSQL `evently` + usuario `evently/evently123` y actualizar `backend/.env`.
2. Backend:
   - `cd backend && python -m venv venv && source venv/bin/activate`
   - `pip install -r requirements.txt`
   - Iniciar: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
3. Frontend:
   - `cd frontend`, `npm install`, `npm run dev`
4. Datos sintéticos:
   - `python scripts/data/generate_quality_events.py`
   - `python scripts/data/generate_final_events.py`
   - `python scripts/data/generate_more_event_impacts.py`
   - `python scripts/data/update_events_csv.py`
   - `python scripts/data/fix_and_retrain.py`
5. ML y utilidades:
   - Entrenamiento: `python scripts/ml/train_and_evaluate_model.py`
   - Métricas y features: `python scripts/ml/show_model_metrics.py`, `python scripts/ml/analyze_and_reduce_features.py`
   - Predicción: `python scripts/ml/predict.py` (CLI) o `python scripts/ml/server_simple.py`

## Comandos útiles

- Entrenar y guardar modelos: `python scripts/ml/train_and_evaluate_model.py`
- Ver métricas sin reentrenar: `python scripts/ml/show_model_metrics.py`
- Generar recomendaciones de features: `python scripts/ml/analyze_and_reduce_features.py` (salida en `data/outputs/feature_recommendations.json`)
- Predicción rápida: `python scripts/ml/predict.py` o `python scripts/ml/server_simple.py`
- Frontend para producción: desde `frontend/`, `npm run build` y `npm run preview`
- Logs / mantenimiento Docker: `docker-compose logs -f [backend|frontend]`, `docker-compose build --no-cache`, `docker-compose down -v`

## Validaciones rápidas

1. Visitar `http://localhost:8000/health` → debe responder `{"status":"healthy"…}`.
2. Verificar tablas clave: `psql -U evently -d evently -h localhost` y contar ciudades/eventos.
3. Abrir `http://localhost:3000` para comprobar globo 3D y flujos interactivos.
4. Correr `python scripts/ml/predict.py` para probar la predicción manual y revisar los outputs en consola.

## Soporte

1. Backend: `docker-compose logs backend` o revisar la terminal de `uvicorn`.
2. Frontend: `docker-compose logs frontend` o la terminal de `npm run dev`.
3. Asegurarse de tener Python 3.11+, Node 18+, PostgreSQL 15+ y dependencias instaladas.

**Desarrollado con React, FastAPI y PostgreSQL** 🚀
