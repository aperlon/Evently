"""
Analizar features y eliminar redundantes para mejorar el modelo
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "backend"))

import pandas as pd
import numpy as np
from app.ml.economic_impact_model import EconomicImpactModel
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import SelectKBest, f_regression
import json

DATA_OUTPUTS = BASE_DIR / "data" / "outputs"
DATA_OUTPUTS.mkdir(parents=True, exist_ok=True)
RECOMMENDATIONS_FILE = DATA_OUTPUTS / "feature_recommendations.json"

print("=" * 80)
print("🔍 ANÁLISIS DE FEATURES Y REDUCCIÓN")
print("=" * 80)
print()

# Cargar modelo y datos
model = EconomicImpactModel()
df_training = model.load_data()

print(f"📊 Dataset: {len(df_training)} muestras")
print(f"📊 Features actuales: {len(model.feature_columns)}")
print()

# Preparar datos para análisis
X = df_training[model.feature_columns].fillna(0)
y = df_training[model.target_column]

# 1. Análisis de correlación entre features
print("=" * 80)
print("1️⃣ ANÁLISIS DE CORRELACIÓN")
print("=" * 80)
print()

correlation_matrix = X.corr().abs()
high_corr_pairs = []

# Encontrar pares con alta correlación (>0.9)
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr = correlation_matrix.iloc[i, j]
        if corr > 0.9:
            high_corr_pairs.append((
                correlation_matrix.columns[i],
                correlation_matrix.columns[j],
                corr
            ))

if high_corr_pairs:
    print("⚠️  Features con alta correlación (>0.9):")
    for feat1, feat2, corr in sorted(high_corr_pairs, key=lambda x: x[2], reverse=True):
        print(f"   {feat1} <-> {feat2}: {corr:.4f}")
    print()
else:
    print("✅ No hay features con correlación >0.9")
    print()

# 2. Importancia de features (usando Gradient Boosting)
print("=" * 80)
print("2️⃣ IMPORTANCIA DE FEATURES")
print("=" * 80)
print()

# Entrenar modelo rápido para obtener importancia
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Transformación logarítmica
y_train_log = np.log1p(y_train)
y_test_log = np.log1p(y_test)

gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
gb_model.fit(X_train_scaled, y_train_log)

# Obtener importancia
feature_importance = pd.DataFrame({
    'feature': model.feature_columns,
    'importance': gb_model.feature_importances_
}).sort_values('importance', ascending=False)

print("📊 Top 20 features más importantes:")
for idx, row in feature_importance.head(20).iterrows():
    print(f"   {row['feature']:<40} {row['importance']:.4f}")
print()

# 3. Selección de features usando SelectKBest
print("=" * 80)
print("3️⃣ SELECCIÓN DE FEATURES (SelectKBest)")
print("=" * 80)
print()

selector = SelectKBest(score_func=f_regression, k='all')
selector.fit(X_train_scaled, y_train_log)

feature_scores = pd.DataFrame({
    'feature': model.feature_columns,
    'score': selector.scores_
}).sort_values('score', ascending=False)

print("📊 Top 20 features por score estadístico:")
for idx, row in feature_scores.head(20).iterrows():
    print(f"   {row['feature']:<40} {row['score']:.2f}")
print()

# 4. Identificar features a eliminar
print("=" * 80)
print("4️⃣ FEATURES RECOMENDADAS PARA ELIMINAR")
print("=" * 80)
print()

# Features con baja importancia Y baja correlación con target
low_importance = feature_importance[feature_importance['importance'] < 0.001]
low_score = feature_scores[feature_scores['score'] < 10]

# Features redundantes (alta correlación entre sí)
redundant_features = set()
for feat1, feat2, corr in high_corr_pairs:
    # Mantener la más importante
    imp1 = feature_importance[feature_importance['feature'] == feat1]['importance'].values[0]
    imp2 = feature_importance[feature_importance['feature'] == feat2]['importance'].values[0]
    if imp1 < imp2:
        redundant_features.add(feat1)
    else:
        redundant_features.add(feat2)

# Features a eliminar
features_to_remove = set()
features_to_remove.update(redundant_features)
features_to_remove.update(low_importance['feature'].tolist()[:10])  # Top 10 menos importantes

if features_to_remove:
    print(f"🗑️  Features recomendadas para eliminar ({len(features_to_remove)}):")
    for feat in sorted(features_to_remove):
        imp = feature_importance[feature_importance['feature'] == feat]['importance'].values[0]
        print(f"   {feat:<40} (importancia: {imp:.6f})")
    print()
else:
    print("✅ No se encontraron features claramente redundantes")
    print()

# 5. Features recomendadas (top features)
print("=" * 80)
print("5️⃣ FEATURES RECOMENDADAS (Top 25)")
print("=" * 80)
print()

# Combinar importancia y score
feature_combined = feature_importance.merge(feature_scores, on='feature')
feature_combined['combined_score'] = (
    feature_combined['importance'] * 0.7 + 
    (feature_combined['score'] / feature_combined['score'].max()) * 0.3
)
feature_combined = feature_combined.sort_values('combined_score', ascending=False)

recommended_features = feature_combined.head(25)['feature'].tolist()

print(f"✅ Top 25 features recomendadas:")
for i, feat in enumerate(recommended_features, 1):
    imp = feature_importance[feature_importance['feature'] == feat]['importance'].values[0]
    print(f"   {i:2d}. {feat:<40} (importancia: {imp:.4f})")
print()

print("=" * 80)
print("📋 RESUMEN")
print("=" * 80)
print(f"   Features actuales: {len(model.feature_columns)}")
print(f"   Features recomendadas: {len(recommended_features)}")
print(f"   Reducción: {len(model.feature_columns) - len(recommended_features)} features")
print(f"   Features a eliminar: {len(features_to_remove)}")
print()

# Guardar recomendaciones
recommendations = {
    'keep': recommended_features,
    'remove': list(features_to_remove),
    'all_current': model.feature_columns
}

with open(RECOMMENDATIONS_FILE, 'w') as f:
    json.dump(recommendations, f, indent=2)

print(f"💾 Recomendaciones guardadas en: {RECOMMENDATIONS_FILE.relative_to(BASE_DIR)}")
print()
print("=" * 80)
print("✅ ANÁLISIS COMPLETADO")
print("=" * 80)

