# 🌍 Fuentes de Datos Reales para Evently MVP - UNESCO

## 📊 Resumen de Fuentes Identificadas

### ✅ Datos Descargables (CSV/API Gratuito)

| Fuente | Tipo de Datos | Formato | URL | Estado |
|--------|---------------|---------|-----|--------|
| **Kaggle - London Marathon** | Participantes 2018-2023 | CSV | https://www.kaggle.com/datasets/kevinegan/london-marathon-results | ✅ Gratuito |
| **Zenodo - London Marathon** | Resultados 2018-2023 | CSV/ZIP | https://zenodo.org/records/10960982 | ✅ Gratuito |
| **Kaggle - UEFA Champions League** | Histórico 1955-2023 | CSV | https://www.kaggle.com/datasets/fardifaalam170041060/champions-league-dataset-1955-2023 | ✅ Gratuito |
| **World Bank Open Data** | Turismo global | CSV/JSON/API | https://data.worldbank.org/indicator/ST.INT.ARVL | ✅ Gratuito |
| **Eurostat Tourism** | Turismo europeo | CSV/SDMX/API | https://ec.europa.eu/eurostat/web/tourism/database | ✅ Gratuito |
| **Google Mobility Reports** | Movilidad urbana | CSV | https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv | ✅ Gratuito |
| **football.csv** | Champions League histórico | CSV | https://footballcsv.github.io/ | ✅ Gratuito |

### ⚠️ Datos Comerciales (Requieren Suscripción)

| Fuente | Tipo de Datos | Limitación |
|--------|---------------|------------|
| **Statista - Wimbledon** | Attendance, Revenue | Requiere suscripción |
| **GlobalData - Wimbledon** | Post-event analysis | Comercial (~$500-1000) |
| **UNWTO Database** | Turismo detallado | Gratis para investigadores con solicitud formal |

---

## 🎾 1. LONDON MARATHON

### Datos Disponibles
- **Período**: 2018-2023 (sin 2020 por COVID)
- **Registros**: ~250,000 runners
- **Métricas**: Times, finish positions, participant demographics

### Fuentes

#### A) Kaggle Dataset
```bash
# Descarga manual o vía Kaggle API
kaggle datasets download -d kevinegan/london-marathon-results
```

**Campos disponibles:**
- `year`, `category`, `finish_position`, `finish_time`
- `club`, `nationality`, `age_category`

#### B) Zenodo Dataset
```bash
wget https://zenodo.org/records/10960982/files/london_marathon_2018_2023.zip
```

### Datos de Impacto Económico (Fuentes Secundarias)
- **Revenue generado**: £73.5M charity (2024)
- **Hotel/Restaurantes**: £13.2M
- **Gasto promedio runner**: £452
- **Espectadores**: £27M contribution

**Fuente**: Análisis de medios y reportes oficiales London Marathon Events

---

## ⚽ 2. UEFA CHAMPIONS LEAGUE

### Datos Disponibles
- **Período**: 1955-2023 (68 años)
- **Registros**: Todos los finales + performance histórica
- **Métricas**: Attendance, winners, venues, scores

### Fuentes

#### A) Kaggle - Historical Dataset
```bash
kaggle datasets download -d fardifaalam170041060/champions-league-dataset-1955-2023
```

**Archivos:**
- `UCL_Finals_1955-2023.csv` - Datos de cada final
- `UCL_AllTime_Performance_Table.csv` - Performance de equipos

**Campos:**
- `season`, `date`, `venue`, `attendance`
- `winner`, `runner_up`, `score`
- `city`, `country`, `stadium_capacity`

#### B) football.csv
```bash
# Descargar desde https://footballcsv.github.io/
wget https://raw.githubusercontent.com/footballcsv/europe-champions-league/master/[archivo].csv
```

### Datos de Impacto Económico
- **Broadcasting rights**: €2.6B (2022/23)
- **Attendance histórica**: 124,000 (1957), 127,621 (1960)
- **Datos económicos detallados**: Requieren análisis secundario

---

## 🎾 3. WIMBLEDON

### Datos Disponibles
- **Período**: Limitado (estadísticas públicas fragmentadas)
- **Attendance records**: Disponibles por año
- **Métricas económicas**: Revenue reports (comerciales)

### Fuentes Públicas

#### A) Estadísticas Oficiales (Manual scraping)
- **URL**: https://www.wimbledon.com/en_GB/atoz/statistics.html
- **Datos**: Attendance por año, prize money

**Datos confirmados:**
- 2023: 532,651 asistentes
- 2024: 526,455 asistentes
- Prize money 2024: $63.6M

#### B) Datos Económicos (Fuentes Secundarias)
- **Revenue 2023**: £380M ($499M)
- **LTA revenue**: £56.1M (51.7% del total LTA)
- **Broadcasting (ESPN)**: $95M/año (2024-2035)

**Limitación**: No hay CSV público descargable. Requiere:
- Web scraping de estadísticas oficiales
- Uso de datos de Statista (comercial)
- Estimaciones basadas en reportes de medios

---

## 🌍 4. TOURISM GLOBAL (World Bank)

### World Bank Open Data API

**Indicadores clave:**
- `ST.INT.ARVL` - International tourism arrivals
- `ST.INT.RCPT.CD` - International tourism receipts (USD)
- `ST.INT.XPND.CD` - International tourism expenditure (USD)

### API Endpoints

```bash
# CSV Download
https://api.worldbank.org/v2/country/all/indicator/ST.INT.ARVL?downloadformat=csv

# JSON
https://api.worldbank.org/v2/country/all/indicator/ST.INT.ARVL?format=json&date=2015:2024

# Por país específico
https://api.worldbank.org/v2/country/GBR;FRA;ESP;USA/indicator/ST.INT.ARVL?format=json&date=2020:2024
```

### Países relevantes
- GBR (UK - London)
- FRA (France - Paris)
- ESP (Spain - Madrid)
- USA (United States - New York, LA)
- JPN (Japan - Tokyo)
- BRA (Brazil - Rio)
- DEU (Germany - Berlin)
- ARE (UAE - Dubai)
- SGP (Singapore)
- AUS (Australia - Sydney)

---

## 🇪🇺 5. EUROSTAT (Tourism Europa)

### Datasets Principales

**Códigos de datasets:**
- `tour_occ_nim` - Nights spent at tourist accommodation
- `tour_occ_arnat` - Arrivals at tourist accommodation
- `tour_occ_cap` - Capacity of tourist accommodation
- `tour_occ_ninat` - Nights spent by residents/non-residents

### API Eurostat

```bash
# URL base
https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/

# Ejemplo: Noches en hoteles
curl "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tour_occ_nim?format=JSON&lang=EN&freq=M&unit=NR&nace_r2=I551-I553&geo=ES;FR;DE;UK&time=2024"
```

**Formatos disponibles:**
- SDMX-CSV
- JSON-stat
- TSV (Tab-Separated)

### Filtros útiles
- `geo`: ES, FR, DE, UK, IT, NL (países)
- `freq`: M (monthly), Q (quarterly), A (annual)
- `nace_r2`: I551-I553 (Hotels and similar accommodation)

---

## 📱 6. GOOGLE MOBILITY REPORTS

### Datos Disponibles
- **Período**: 2020-presente (COVID-19 Mobility)
- **Cobertura**: Global, nivel ciudad/región
- **Métricas**: Cambio % respecto baseline en:
  - Retail & recreation
  - Grocery & pharmacy
  - Parks
  - Transit stations
  - Workplaces
  - Residential

### Download Directo

```bash
# CSV global (actualizado regularmente)
wget https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv
```

**Campos:**
- `country_region_code`, `sub_region_1`, `date`
- `retail_and_recreation_percent_change_from_baseline`
- `transit_stations_percent_change_from_baseline`
- `workplaces_percent_change_from_baseline`

**Ciudades disponibles:**
- Londres: `sub_region_1 = 'England'`
- París: `sub_region_1 = 'Île-de-France'`
- Madrid: `sub_region_1 = 'Community of Madrid'`
- Berlín: `sub_region_1 = 'Berlin'`
- Nueva York: `sub_region_1 = 'New York'`
- Tokyo: `sub_region_1 = 'Tokyo'`

---

## 🏨 7. HOTEL PRICING DATA (Alternativas)

### Fuentes Potenciales

#### A) Booking.com / Airbnb (Web Scraping Legal)
- Requiere scraping ético y compliance
- Datos históricos limitados

#### B) STR Global (Comercial)
- Industry-standard hotel data
- Requiere suscripción ($$$)

#### C) Alternativa: Estimaciones basadas en
- Eurostat occupancy rates
- Precios promedio por ciudad (datos públicos)
- Correlación con eventos (nuestro modelo)

---

## 📋 PLAN DE IMPLEMENTACIÓN

### Fase 1: Descarga de Datos ✅
```bash
data/sources/
├── london_marathon/
│   ├── kaggle_results_2018_2023.csv
│   └── zenodo_runners.csv
├── champions_league/
│   ├── finals_1955_2023.csv
│   └── performance_table.csv
├── worldbank/
│   ├── tourism_arrivals.csv
│   └── tourism_receipts.csv
├── eurostat/
│   ├── hotel_nights.csv
│   └── arrivals_by_country.csv
└── google_mobility/
    └── global_mobility_report.csv
```

### Fase 2: ETL Pipeline
1. **Extract**: Descargar todos los CSVs
2. **Transform**: Normalizar fechas, unidades, ciudades
3. **Load**: Importar a PostgreSQL

### Fase 3: ML Training
1. Series temporales por ciudad
2. Correlación eventos → impacto
3. Modelos predictivos (Prophet, ARIMA)

---

## 🔐 APIs que Requieren Keys (Futuro)

- **AIRROI**: Hotel analytics (comercial)
- **STR Global**: Hotel occupancy industry standard
- **Statista**: Statistics platform (suscripción)
- **PredictHQ**: Event intelligence API

---

## 📞 Contactos para Datos Adicionales

- **UNWTO**: tourism@unwto.org (solicitud formal para investigadores)
- **UEFA**: media@uefa.ch (solicitud de datos para investigación)
- **Wimbledon/AELTC**: communications@aeltc.com
- **London Marathon Events**: info@londonmarathonevents.co.uk

---

**Última actualización**: 2025-11-21
**Responsable**: Equipo Evently - UNESCO MVP
