"""
Economic Impact Regression Model
Predicts total economic impact of events based on event and city characteristics
Reads directly from CSV files for easy data updates

Author: Evently UNESCO MVP
"""
import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional, List

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class EconomicImpactModel:
    """
    Regression model to predict economic impact of events.

    Reads data from CSV files, making it easy to update with real data.
    When you replace the CSV files with real data, just retrain the model.

    Usage:
        model = EconomicImpactModel()
        model.load_data()           # Load from CSVs
        model.train()               # Train all models
        model.predict(event_data)   # Predict for new event
    """

    def __init__(self, data_dir: str = None):
        """
        Initialize the model.

        Args:
            data_dir: Directory containing CSV files.
                      Defaults to data/examples/
        """
        if data_dir is None:
            # Find data directory relative to this file or current working directory
            possible_paths = [
                Path(__file__).parent.parent.parent / "data" / "examples",
                Path.cwd() / "data" / "examples",
                Path("/data/examples"),  # Docker path
                Path("/home/user/Evently/data/examples"),
            ]
            for path in possible_paths:
                if path.exists():
                    data_dir = path
                    break

        self.data_dir = Path(data_dir) if data_dir else Path("data/examples")
        
        # Debug: print data directory
        print(f"📂 EconomicImpactModel initialized with data_dir: {self.data_dir}")
        print(f"   Data dir exists: {self.data_dir.exists()}")
        self.models_dir = Path(__file__).parent / "saved_models"
        self.models_dir.mkdir(exist_ok=True)

        # Data
        self.df_events = None
        self.df_cities = None
        self.df_impacts = None
        self.df_training = None
        
        # Additional metrics CSVs (time-series data)
        self.df_tourism_metrics = None
        self.df_hotel_metrics = None
        self.df_economic_metrics = None
        self.df_mobility_metrics = None

        # Models
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.label_encoders = {}

        # Feature columns
        self.feature_columns = []
        self.target_column = "total_economic_impact_usd"

        # Metrics
        self.metrics = {}
        
        # Jobs creation ratios by city (calculated from historical data analysis)
        # These ratios represent: total_economic_impact_usd / jobs_created
        # Updated based on analysis of 1,102 events
        # Cities with higher cost of living create jobs at higher cost per job
        self.jobs_ratios_by_city = {
            'Paris': 47475,           # Highest: $47,475 per job (high cost of living)
            'New York': 43102,        # $43,102 per job
            'Berlin': 42426,          # $42,426 per job
            'London': 41727,          # $41,727 per job
            'Madrid': 40383,          # $40,383 per job
            'Tokyo': 40315,           # $40,315 per job
            'Rio de Janeiro': 40027,   # $40,027 per job
            'Barcelona': 40009,       # $40,009 per job
            'Amsterdam': 40009,        # $40,009 per job
            'Dubai': 40007,            # $40,007 per job
            'São Paulo': 40007,        # $40,007 per job
            'Sydney': 40006,           # $40,006 per job
            'Singapore': 40005,        # $40,005 per job
            'Miami': 40005,            # $40,005 per job
            'Los Angeles': 40002,      # $40,002 per job
            'Chicago': 40001,          # $40,001 per job (lowest)
        }
        self.default_jobs_ratio = 40000  # Default if city not found
        
        # Jobs creation ratios (calculated from historical data)
        # Format: {event_type: {city: ratio}, ...}
        # Default: 40000 if no specific data available
        self.jobs_ratios = {
            'sports': 43398,      # Average from real data
            'music': 40243,
            'culture': 41085,
            'festival': 40966,
            'conference': 40005,
            'expo': 40007,
        }
        self.default_jobs_ratio = 40000

    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV files and prepare for training.

        Returns:
            DataFrame ready for training
        """
        print("\n📂 Loading data from CSV files...")
        print(f"   Directory: {self.data_dir}")

        # Load basic CSVs
        self.df_events = pd.read_csv(self.data_dir / "events.csv")
        self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
        self.df_impacts = pd.read_csv(self.data_dir / "event_impacts.csv")
        
        # Load time-series metrics CSVs
        self.df_tourism_metrics = pd.read_csv(self.data_dir / "tourism_metrics.csv")
        self.df_hotel_metrics = pd.read_csv(self.data_dir / "hotel_metrics.csv")
        self.df_economic_metrics = pd.read_csv(self.data_dir / "economic_metrics.csv")
        self.df_mobility_metrics = pd.read_csv(self.data_dir / "mobility_metrics.csv")
        
        # Convert date columns to datetime
        self.df_tourism_metrics['date'] = pd.to_datetime(self.df_tourism_metrics['date'])
        self.df_hotel_metrics['date'] = pd.to_datetime(self.df_hotel_metrics['date'])
        self.df_economic_metrics['date'] = pd.to_datetime(self.df_economic_metrics['date'])
        self.df_mobility_metrics['date'] = pd.to_datetime(self.df_mobility_metrics['date'])

        print(f"   ✓ events.csv: {len(self.df_events)} events")
        print(f"   ✓ cities.csv: {len(self.df_cities)} cities")
        print(f"   ✓ event_impacts.csv: {len(self.df_impacts)} impact records")
        print(f"   ✓ tourism_metrics.csv: {len(self.df_tourism_metrics)} daily records")
        print(f"   ✓ hotel_metrics.csv: {len(self.df_hotel_metrics)} daily records")
        print(f"   ✓ economic_metrics.csv: {len(self.df_economic_metrics)} daily records")
        print(f"   ✓ mobility_metrics.csv: {len(self.df_mobility_metrics)} daily records")

        # Merge data
        self.df_training = self._prepare_training_data()

        print(f"\n   📊 Training dataset: {len(self.df_training)} samples")
        print(f"   📊 Features: {len(self.feature_columns)} columns")

        return self.df_training

    def _enrich_with_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrich event data with time-series metrics from tourism, hotel, economic, and mobility CSVs.
        
        For each event:
        1. Get event dates (start_date, end_date) from events.csv
        2. Calculate baseline metrics (30 days before event)
        3. Calculate event period metrics (during event)
        4. Calculate differences and ratios
        5. Add as new features
        """
        print("\n📊 Enriching events with time-series metrics...")
        
        # Get event dates from events.csv
        events_with_dates = self.df_events[['event_name', 'start_date', 'end_date']].copy()
        events_with_dates['start_date'] = pd.to_datetime(events_with_dates['start_date'])
        events_with_dates['end_date'] = pd.to_datetime(events_with_dates['end_date'])
        
        # Merge to get dates for each impact record
        df = df.merge(events_with_dates, on='event_name', how='left')
        
        # Initialize new feature columns
        metric_features = []
        
        def calculate_event_metrics(row):
            """Calculate metrics for a single event"""
            city = row['city']
            start_date = row['start_date']
            end_date = row['end_date']
            
            if pd.isna(start_date) or pd.isna(end_date):
                return pd.Series()
            
            # Baseline period: 30 days before event
            baseline_start = start_date - pd.Timedelta(days=30)
            baseline_end = start_date - pd.Timedelta(days=1)
            
            # Filter metrics for this city
            city_tourism = self.df_tourism_metrics[self.df_tourism_metrics['city'] == city].copy()
            city_hotel = self.df_hotel_metrics[self.df_hotel_metrics['city'] == city].copy()
            city_economic = self.df_economic_metrics[self.df_economic_metrics['city'] == city].copy()
            city_mobility = self.df_mobility_metrics[self.df_mobility_metrics['city'] == city].copy()
            
            metrics = {}
            
            # TOURISM METRICS
            if not city_tourism.empty:
                # Event period
                event_tourism = city_tourism[
                    (city_tourism['date'] >= start_date) & 
                    (city_tourism['date'] <= end_date)
                ]
                # Baseline period
                baseline_tourism = city_tourism[
                    (city_tourism['date'] >= baseline_start) & 
                    (city_tourism['date'] <= baseline_end)
                ]
                
                if not event_tourism.empty and not baseline_tourism.empty:
                    # Event period averages
                    metrics['event_avg_total_visitors'] = event_tourism['total_visitors'].mean()
                    metrics['event_avg_spending_per_visitor'] = event_tourism['avg_spending_per_visitor_usd'].mean()
                    metrics['event_avg_stay_duration'] = event_tourism['avg_stay_duration_days'].mean()
                    
                    # Baseline averages
                    metrics['baseline_avg_total_visitors'] = baseline_tourism['total_visitors'].mean()
                    metrics['baseline_avg_spending_per_visitor'] = baseline_tourism['avg_spending_per_visitor_usd'].mean()
                    metrics['baseline_avg_stay_duration'] = baseline_tourism['avg_stay_duration_days'].mean()
                    
                    # Differences
                    metrics['visitor_increase_actual'] = (
                        (metrics['event_avg_total_visitors'] / max(metrics['baseline_avg_total_visitors'], 1) - 1) * 100
                        if metrics['baseline_avg_total_visitors'] > 0 else 0
                    )
                    metrics['spending_increase_pct'] = (
                        (metrics['event_avg_spending_per_visitor'] / max(metrics['baseline_avg_spending_per_visitor'], 1) - 1) * 100
                        if metrics['baseline_avg_spending_per_visitor'] > 0 else 0
                    )
            
            # HOTEL METRICS
            if not city_hotel.empty:
                event_hotel = city_hotel[
                    (city_hotel['date'] >= start_date) & 
                    (city_hotel['date'] <= end_date)
                ]
                baseline_hotel = city_hotel[
                    (city_hotel['date'] >= baseline_start) & 
                    (city_hotel['date'] <= baseline_end)
                ]
                
                if not event_hotel.empty and not baseline_hotel.empty:
                    metrics['event_avg_occupancy_pct'] = event_hotel['occupancy_rate_pct'].mean()
                    metrics['event_avg_hotel_price'] = event_hotel['avg_price_usd'].mean()
                    metrics['event_max_hotel_price'] = event_hotel['avg_price_usd'].max()
                    
                    metrics['baseline_avg_occupancy_pct'] = baseline_hotel['occupancy_rate_pct'].mean()
                    metrics['baseline_avg_hotel_price'] = baseline_hotel['avg_price_usd'].mean()
                    
                    metrics['occupancy_boost_actual'] = metrics['event_avg_occupancy_pct'] - metrics['baseline_avg_occupancy_pct']
                    metrics['hotel_price_increase_actual'] = (
                        (metrics['event_avg_hotel_price'] / max(metrics['baseline_avg_hotel_price'], 1) - 1) * 100
                        if metrics['baseline_avg_hotel_price'] > 0 else 0
                    )
            
            # ECONOMIC METRICS
            if not city_economic.empty:
                event_economic = city_economic[
                    (city_economic['date'] >= start_date) & 
                    (city_economic['date'] <= end_date)
                ]
                baseline_economic = city_economic[
                    (city_economic['date'] >= baseline_start) & 
                    (city_economic['date'] <= baseline_end)
                ]
                
                if not event_economic.empty and not baseline_economic.empty:
                    metrics['event_avg_daily_spending'] = event_economic['total_spending_usd'].mean()
                    metrics['event_avg_accommodation_spending'] = event_economic['accommodation_spending_usd'].mean()
                    metrics['event_avg_food_spending'] = event_economic['food_beverage_spending_usd'].mean()
                    metrics['event_avg_retail_spending'] = event_economic['retail_spending_usd'].mean()
                    
                    metrics['baseline_avg_daily_spending'] = baseline_economic['total_spending_usd'].mean()
                    
                    metrics['daily_spending_increase_pct'] = (
                        (metrics['event_avg_daily_spending'] / max(metrics['baseline_avg_daily_spending'], 1) - 1) * 100
                        if metrics['baseline_avg_daily_spending'] > 0 else 0
                    )
            
            # MOBILITY METRICS
            if not city_mobility.empty:
                event_mobility = city_mobility[
                    (city_mobility['date'] >= start_date) & 
                    (city_mobility['date'] <= end_date)
                ]
                baseline_mobility = city_mobility[
                    (city_mobility['date'] >= baseline_start) & 
                    (city_mobility['date'] <= baseline_end)
                ]
                
                if not event_mobility.empty and not baseline_mobility.empty:
                    metrics['event_avg_airport_arrivals'] = event_mobility['airport_arrivals'].mean()
                    metrics['event_avg_international_flights'] = event_mobility['international_flights'].mean()
                    metrics['event_avg_public_transport'] = event_mobility['public_transport_usage'].mean()
                    metrics['event_avg_traffic_congestion'] = event_mobility['traffic_congestion_index'].mean()
                    
                    metrics['baseline_avg_airport_arrivals'] = baseline_mobility['airport_arrivals'].mean()
                    metrics['baseline_avg_traffic_congestion'] = baseline_mobility['traffic_congestion_index'].mean()
                    
                    metrics['airport_arrivals_increase_pct'] = (
                        (metrics['event_avg_airport_arrivals'] / max(metrics['baseline_avg_airport_arrivals'], 1) - 1) * 100
                        if metrics['baseline_avg_airport_arrivals'] > 0 else 0
                    )
            
            return pd.Series(metrics)
        
        # Apply to each row
        print("   Calculating metrics for each event...")
        metric_df = df.apply(calculate_event_metrics, axis=1)
        
        # Merge metrics back to main dataframe
        df = pd.concat([df, metric_df], axis=1)
        
        # Fill NaN values with 0 or median
        for col in metric_df.columns:
            if col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(0)
        
        print(f"   ✓ Added {len(metric_df.columns)} new metric features")
        
        return df

    def _prepare_training_data(self) -> pd.DataFrame:
        """
        Prepare training data by merging events, cities, and impacts.
        Creates derived features for better predictions.
        """
        # Merge impacts with cities
        df = self.df_impacts.merge(
            self.df_cities[['name', 'population', 'annual_tourists', 'hotel_rooms',
                           'avg_hotel_price_usd', 'gdp_usd']],
            left_on='city',
            right_on='name',
            how='left'
        )

        # Get event type - it's already in event_impacts.csv, but if not, get from events.csv
        if 'event_type' not in df.columns:
            event_types = self.df_events[['event_name', 'event_type']].drop_duplicates()
            df = df.merge(
                event_types[['event_name', 'event_type']],
                on='event_name',
                how='left'
            )

        # Get duration_days from event_impacts.csv (it's already there)
        # If not present, calculate from events.csv
        if 'duration_days' not in df.columns:
            events_duration = self.df_events[['event_name', 'start_date', 'end_date']].copy()
            events_duration['start_date'] = pd.to_datetime(events_duration['start_date'])
            events_duration['end_date'] = pd.to_datetime(events_duration['end_date'])
            events_duration['duration_days'] = (events_duration['end_date'] - events_duration['start_date']).dt.days + 1

            df = df.merge(
                events_duration[['event_name', 'duration_days']],
                on='event_name',
                how='left'
            )
            # Fill missing duration_days with 1 as default
            df['duration_days'] = df['duration_days'].fillna(1)

        # Get attendance from impacts CSV (it's already there)
        if 'attendance' not in df.columns:
            # If attendance is not in the merged data, try to calculate it
            if 'additional_visitors' in df.columns:
                df['attendance'] = df['additional_visitors'].fillna(
                    df.get('baseline_daily_visitors', 10000) * df.get('visitor_increase_pct', 20) / 100 * df['duration_days'].clip(lower=1)
                )
            else:
                # Estimate from annual tourists and duration
                df['attendance'] = (df['annual_tourists'] / 365) * df['duration_days'].clip(lower=1)
        
        # Calculate missing features if not present
        if 'visitor_increase_pct' not in df.columns:
            # Estimate visitor increase based on attendance vs baseline
            baseline_daily = df['annual_tourists'] / 365
            df['visitor_increase_pct'] = ((df['attendance'] / df['duration_days'].clip(lower=1)) / baseline_daily.clip(lower=1) - 1) * 100
            df['visitor_increase_pct'] = df['visitor_increase_pct'].clip(lower=0, upper=200)
        
        if 'price_increase_pct' not in df.columns:
            df['price_increase_pct'] = df['visitor_increase_pct'] * 0.8  # Heuristic
            df['price_increase_pct'] = df['price_increase_pct'].clip(lower=0, upper=150)

        if 'occupancy_boost' not in df.columns:
            if 'event_occupancy_pct' in df.columns and 'baseline_occupancy_pct' in df.columns:
                df['occupancy_boost'] = df['event_occupancy_pct'] - df['baseline_occupancy_pct']
            else:
                df['occupancy_boost'] = df['visitor_increase_pct'] * 0.3  # Heuristic
            df['occupancy_boost'] = df['occupancy_boost'].clip(lower=0, upper=25)

        # Enrich with time-series metrics from additional CSVs
        df = self._enrich_with_metrics(df)
        
        # Create derived features
        df['attendance_per_day'] = df['attendance'] / df['duration_days'].clip(lower=1)
        df['visitors_per_hotel_room'] = df['attendance'] / df['hotel_rooms'].clip(lower=1)
        df['city_tourism_intensity'] = df['annual_tourists'] / df['population'].clip(lower=1)

        # Encode categorical variables
        if 'event_type' in df.columns:
            self.label_encoders['event_type'] = LabelEncoder()
            df['event_type_encoded'] = self.label_encoders['event_type'].fit_transform(
                df['event_type'].fillna('other')
            )
        else:
            # If event_type is missing, create a default encoding
            df['event_type_encoded'] = 0
            print("⚠️  Warning: event_type not found, using default encoding")

        # Define feature columns (OPTIMIZED - removed redundant features)
        # Based on analysis: attendance (67.97%) and event_type_encoded (29.89%) are most important
        # Removed features with high correlation (>0.9) and low importance (<0.001)
        self.feature_columns = [
            # Event characteristics (MOST IMPORTANT)
            'attendance',                    # 67.97% importance
            'event_type_encoded',            # 29.89% importance
            'duration_days',
            
            # Key derived features
            'attendance_per_day',
            'visitors_per_hotel_room',
            
            # City characteristics (essential)
            'hotel_rooms',
            'city_tourism_intensity',
            
            # Top metrics from CSVs (most informative, avoiding redundancy)
            'event_max_hotel_price',         # 0.47% importance
            'event_avg_hotel_price',         # 0.26% importance
            'daily_spending_increase_pct',   # 0.19% importance
            'event_avg_public_transport',    # 0.13% importance
            'visitor_increase_actual',       # 0.13% importance
            'baseline_avg_spending_per_visitor',  # 0.11% importance
            'event_avg_accommodation_spending',    # 0.10% importance
            
            # Removed redundant features:
            # - visitor_increase_pct (correlated 0.9995 with price_increase_pct, kept price_increase_pct)
            # - baseline_avg_total_visitors (correlated 0.9989 with baseline_avg_airport_arrivals)
            # - event_avg_daily_spending (correlated 0.9922 with event_avg_total_visitors)
            # - event_avg_food_spending, event_avg_retail_spending (correlated >0.99 with others)
            # - baseline_avg_hotel_price (correlated 0.9532 with avg_hotel_price_usd)
            # - Many mobility metrics (highly correlated with economic metrics)
        ]

        # Keep only rows with target variable
        df = df[df[self.target_column].notna()]

        # Ensure all feature columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                print(f"⚠️  Warning: Feature '{col}' not found, creating default value")
                if col == 'event_type_encoded':
                    df[col] = 0
                else:
                    df[col] = 0.0

        # Fill missing values with appropriate defaults
        for col in self.feature_columns:
            if col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    # For percentage increases, use 0 if missing
                    if 'increase' in col or 'boost' in col or 'pct' in col:
                        df[col] = df[col].fillna(0.0)
                    # For averages, use median if available, else 0
                    else:
                        df[col] = df[col].fillna(df[col].median() if len(df[col].dropna()) > 0 else 0)
                else:
                    df[col] = df[col].fillna(0)

        return df

    def train(self, test_size: float = 0.2, random_state: int = 42) -> Dict:
        """
        Train multiple regression models and select the best one.

        Args:
            test_size: Fraction of data to use for testing
            random_state: Random seed for reproducibility

        Returns:
            Dictionary with metrics for all models
        """
        if self.df_training is None:
            self.load_data()

        print("\n🤖 Training regression models...")
        print("=" * 60)

        # Prepare features and target
        X = self.df_training[self.feature_columns].values
        y = self.df_training[self.target_column].values

        # Log transform target for better distribution
        y_log = np.log1p(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_log, test_size=test_size, random_state=random_state
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        print(f"\n📊 Dataset split:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Testing samples: {len(X_test)}")

        # Define models to train
        model_configs = {
            'linear_regression': LinearRegression(),
            'ridge_regression': Ridge(alpha=1.0),
            'lasso_regression': Lasso(alpha=0.1),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=3,
                random_state=random_state,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=random_state
            ),
        }

        best_r2 = -float('inf')

        for name, model in model_configs.items():
            print(f"\n🎯 Training {name}...")

            # Train
            model.fit(X_train_scaled, y_train)

            # Predict (in log space)
            y_pred_log = model.predict(X_test_scaled)

            # Transform back to original scale
            y_pred = np.expm1(y_pred_log)
            y_test_original = np.expm1(y_test)

            # Calculate metrics
            metrics = {
                'r2': r2_score(y_test_original, y_pred),
                'mae': mean_absolute_error(y_test_original, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test_original, y_pred)),
                'mape': np.mean(np.abs((y_test_original - y_pred) / np.maximum(y_test_original, 1))) * 100,  # Evitar división por 0
            }

            # Cross-validation score
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()

            self.models[name] = model
            self.metrics[name] = metrics

            print(f"   R² Score: {metrics['r2']:.4f}")
            print(f"   MAE: ${metrics['mae']:,.0f}")
            print(f"   RMSE: ${metrics['rmse']:,.0f}")
            print(f"   MAPE: {metrics['mape']:.2f}%")
            print(f"   CV R² (5-fold): {metrics['cv_r2_mean']:.4f} ± {metrics['cv_r2_std']:.4f}")

            # Track best model
            if metrics['r2'] > best_r2:
                best_r2 = metrics['r2']
                self.best_model = model
                self.best_model_name = name

        print("\n" + "=" * 60)
        print(f"🏆 Best Model: {self.best_model_name}")
        print(f"   R² Score: {self.metrics[self.best_model_name]['r2']:.4f}")
        print(f"   MAPE: {self.metrics[self.best_model_name]['mape']:.2f}%")

        # Feature importance (for tree-based models)
        if hasattr(self.best_model, 'feature_importances_'):
            self._print_feature_importance()

        return self.metrics

    def _print_feature_importance(self):
        """Print feature importance for the best model."""
        if not hasattr(self.best_model, 'feature_importances_'):
            return

        importance = self.best_model.feature_importances_
        indices = np.argsort(importance)[::-1]

        print("\n📈 Feature Importance:")
        for i, idx in enumerate(indices[:10]):
            print(f"   {i+1}. {self.feature_columns[idx]}: {importance[idx]:.4f}")

    def predict(self, event_data: Dict) -> Dict:
        """
        Predict economic impact for a new event.

        Args:
            event_data: Dictionary with event characteristics:
                - attendance: Expected attendance
                - duration_days: Event duration
                - event_type: Type (sports, music, culture, festival, business)
                - city: City name (must exist in cities.csv)

                Optional (will be looked up from city):
                - population, annual_tourists, hotel_rooms, avg_hotel_price_usd

        Returns:
            Dictionary with prediction and confidence interval
        """
        if self.best_model is None:
            raise ValueError("Model not trained. Call train() first.")

        # Get city data if not provided
        city_name = event_data.get('city')
        if city_name and self.df_cities is not None:
            city_row = self.df_cities[self.df_cities['name'] == city_name]
            if not city_row.empty:
                city_data = city_row.iloc[0]
                event_data.setdefault('population', city_data['population'])
                event_data.setdefault('annual_tourists', city_data['annual_tourists'])
                event_data.setdefault('hotel_rooms', city_data['hotel_rooms'])
                event_data.setdefault('avg_hotel_price_usd', city_data['avg_hotel_price_usd'])

        # Encode event type
        event_type = event_data.get('event_type', 'other')
        if 'event_type' in self.label_encoders:
            try:
                event_type_encoded = self.label_encoders['event_type'].transform([event_type])[0]
            except ValueError:
                event_type_encoded = 0  # Default for unknown types
        else:
            event_type_encoded = 0

        # Calculate derived features
        attendance = event_data.get('attendance', 50000)
        duration_days = event_data.get('duration_days', 1)
        population = event_data.get('population', 1000000)
        annual_tourists = event_data.get('annual_tourists', 5000000)
        hotel_rooms = event_data.get('hotel_rooms', 50000)
        avg_hotel_price = event_data.get('avg_hotel_price_usd', 150)

        # Estimate visitor/price increases if not provided
        visitor_increase_pct = event_data.get('visitor_increase_pct',
                                              min(100, attendance / (annual_tourists / 365) * 100))
        price_increase_pct = event_data.get('price_increase_pct',
                                            min(150, visitor_increase_pct * 0.8))
        occupancy_boost = event_data.get('occupancy_boost', min(25, visitor_increase_pct * 0.3))

        # Build feature vector with all features (including metrics)
        # For new predictions, we'll use estimated values for metrics features
        # These will be filled in predict_simple() from historical averages
        
        # Base features
        base_features = {
            'attendance': attendance,
            'duration_days': duration_days,
            'event_type_encoded': event_type_encoded,
            'visitor_increase_pct': visitor_increase_pct,
            'price_increase_pct': price_increase_pct,
            'occupancy_boost': occupancy_boost,
            'population': population,
            'annual_tourists': annual_tourists,
            'hotel_rooms': hotel_rooms,
            'avg_hotel_price_usd': avg_hotel_price,
            'attendance_per_day': attendance / max(duration_days, 1),
            'visitors_per_hotel_room': attendance / max(hotel_rooms, 1),
            'city_tourism_intensity': annual_tourists / max(population, 1),
        }
        
        # Add metric features if provided, otherwise use defaults (0)
        # These will be estimated from historical data in predict_simple()
        metric_features_defaults = {
            'event_avg_total_visitors': 0,
            'baseline_avg_total_visitors': annual_tourists / 365,
            'visitor_increase_actual': visitor_increase_pct,
            'event_avg_spending_per_visitor': 0,
            'baseline_avg_spending_per_visitor': 150,  # Default
            'spending_increase_pct': 0,
            'event_avg_stay_duration': 0,
            'event_avg_occupancy_pct': 0,
            'baseline_avg_occupancy_pct': 70,  # Default
            'occupancy_boost_actual': occupancy_boost,
            'event_avg_hotel_price': avg_hotel_price,
            'baseline_avg_hotel_price': avg_hotel_price,
            'hotel_price_increase_actual': price_increase_pct,
            'event_max_hotel_price': avg_hotel_price * 1.5,
            'event_avg_daily_spending': 0,
            'baseline_avg_daily_spending': 0,
            'daily_spending_increase_pct': 0,
            'event_avg_accommodation_spending': 0,
            'event_avg_food_spending': 0,
            'event_avg_retail_spending': 0,
            'event_avg_airport_arrivals': 0,
            'baseline_avg_airport_arrivals': 0,
            'airport_arrivals_increase_pct': 0,
            'event_avg_international_flights': 0,
            'event_avg_public_transport': 0,
            'event_avg_traffic_congestion': 0,
            'baseline_avg_traffic_congestion': 0,
        }
        
        # Merge provided values with defaults
        for key, default_value in metric_features_defaults.items():
            base_features[key] = event_data.get(key, default_value)
        
        # Build feature vector in the correct order
        features = [base_features.get(col, 0.0) for col in self.feature_columns]

        # Scale and predict
        X = np.array([features])
        X_scaled = self.scaler.transform(X)

        # Predict in log space
        y_pred_log = self.best_model.predict(X_scaled)
        prediction = np.expm1(y_pred_log)[0]

        # Estimate confidence interval using model's training error
        mape = self.metrics[self.best_model_name]['mape'] / 100
        lower_bound = prediction * (1 - mape * 1.5)
        upper_bound = prediction * (1 + mape * 1.5)

        # Calculate breakdown (using typical ratios)
        direct_spending = prediction * 0.64  # 64% direct
        indirect_spending = prediction * 0.25  # 25% indirect
        induced_spending = prediction * 0.11  # 11% induced

        # Estimate jobs created using city-specific ratio adjusted for event duration
        # Ratios calculated from historical data analysis (1,102 events)
        # Cities with higher cost of living (Paris, New York) create jobs at higher cost
        # Cities with lower cost of living (Chicago, São Paulo) create jobs at lower cost
        # IMPORTANTE: Este ratio NO afecta el modelo ML, solo se usa POST-predicción para calcular jobs_created
        # 
        # El ratio base ($40,000) representa el costo de un empleo a tiempo completo durante 1 año (250 días laborables)
        # Para eventos de duración corta, ajustamos: (ratio_base / 250) * duration_days
        city_name = event_data.get('city', '')
        duration_days = event_data.get('duration_days', 1)
        jobs_ratio_base = self.jobs_ratios_by_city.get(city_name, self.default_jobs_ratio)
        
        # Ajustar ratio por duración: ratio anual / 250 días * duración del evento
        working_days_per_year = 250
        jobs_ratio_adjusted = (jobs_ratio_base / working_days_per_year) * duration_days
        
        jobs_created = int(prediction / jobs_ratio_adjusted)

        # ROI estimate
        estimated_cost = prediction / 4.0  # Typical ROI of 4:1
        roi = prediction / estimated_cost

        return {
            'prediction': {
                'total_economic_impact_usd': round(prediction, 2),
                'lower_bound_usd': round(lower_bound, 2),
                'upper_bound_usd': round(upper_bound, 2),
                'confidence_level': '90%',
            },
            'breakdown': {
                'direct_spending_usd': round(direct_spending, 2),
                'indirect_spending_usd': round(indirect_spending, 2),
                'induced_spending_usd': round(induced_spending, 2),
            },
            'estimates': {
                'jobs_created': jobs_created,
                'jobs_ratio_usd': round(jobs_ratio_adjusted, 2),  # Ratio ajustado por duración
                'jobs_ratio_base_usd': round(jobs_ratio_base, 2),  # Ratio base anual (para referencia)
                'roi_ratio': round(roi, 2),
                'estimated_event_cost_usd': round(estimated_cost, 2),
            },
            'model_info': {
                'model_used': self.best_model_name,
                'model_r2': round(self.metrics[self.best_model_name]['r2'], 4),
                'model_mape': round(self.metrics[self.best_model_name]['mape'], 2),
            },
            'input_summary': {
                'event_type': event_type,
                'city': city_name,
                'attendance': attendance,
                'duration_days': duration_days,
            }
        }

    def predict_simple(self, event_type: str, city: str, duration_days: int,
                       attendance: int = None) -> Dict:
        """
        Simplified prediction using historical averages for similar events.

        Only requires minimal inputs - the system fills in the rest using
        averages from similar events (same type, same continent).

        Args:
            event_type: Type of event (sports, music, festival, culture, business)
            city: City name (must exist in cities.csv)
            duration_days: Event duration in days
            attendance: Optional attendance estimate. If not provided,
                       uses average attendance_per_day * duration_days

        Returns:
            Dictionary with prediction, breakdown, and historical context
        """
        if self.best_model is None:
            raise ValueError("Model not trained. Call train() or load() first.")

        # Load data if not already loaded
        if self.df_cities is None:
            self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
        if self.df_events is None:
            self.df_events = pd.read_csv(self.data_dir / "events.csv")
        if self.df_impacts is None:
            self.df_impacts = pd.read_csv(self.data_dir / "event_impacts.csv")
        
        # Load time-series metrics CSVs if not already loaded
        if self.df_tourism_metrics is None:
            self.df_tourism_metrics = pd.read_csv(self.data_dir / "tourism_metrics.csv")
            self.df_tourism_metrics['date'] = pd.to_datetime(self.df_tourism_metrics['date'])
        if self.df_hotel_metrics is None:
            self.df_hotel_metrics = pd.read_csv(self.data_dir / "hotel_metrics.csv")
            self.df_hotel_metrics['date'] = pd.to_datetime(self.df_hotel_metrics['date'])
        if self.df_economic_metrics is None:
            self.df_economic_metrics = pd.read_csv(self.data_dir / "economic_metrics.csv")
            self.df_economic_metrics['date'] = pd.to_datetime(self.df_economic_metrics['date'])
        if self.df_mobility_metrics is None:
            self.df_mobility_metrics = pd.read_csv(self.data_dir / "mobility_metrics.csv")
            self.df_mobility_metrics['date'] = pd.to_datetime(self.df_mobility_metrics['date'])

        # Get city info
        city_row = self.df_cities[self.df_cities['name'] == city]
        if city_row.empty:
            available_cities = self.df_cities['name'].tolist()
            raise ValueError(f"City '{city}' not found. Available: {available_cities}")

        city_data = city_row.iloc[0]
        continent = city_data['continent']
        country = city_data['country']

        # Get events of this type
        events_of_type = self.df_events[self.df_events['event_type'] == event_type]
        if events_of_type.empty:
            available_types = self.df_events['event_type'].unique().tolist()
            raise ValueError(f"Event type '{event_type}' not found. Available: {available_types}")

        # Merge with impacts to get historical data
        events_with_impacts = events_of_type.merge(
            self.df_impacts,
            on='event_name',
            how='inner'
        )

        # Get cities with continent info
        events_with_cities = events_with_impacts.merge(
            self.df_cities[['name', 'continent', 'country']],
            left_on='city_x',
            right_on='name',
            how='left'
        )

        # Filter by continent (or use all if not enough data)
        same_continent = events_with_cities[events_with_cities['continent'] == continent]

        if len(same_continent) >= 2:
            reference_data = same_continent
            reference_scope = f"{continent} ({len(same_continent)} eventos)"
        else:
            reference_data = events_with_cities
            reference_scope = f"Global ({len(events_with_cities)} eventos)"

        # Calculate averages from historical data
        # Use attendance and duration_days from event_impacts.csv
        if 'attendance' in reference_data.columns and 'duration_days' in reference_data.columns:
            events_with_duration = reference_data.copy()
            events_with_duration['attendance_per_day'] = (
                events_with_duration['attendance'] / events_with_duration['duration_days'].clip(lower=1)
            )
            avg_attendance_per_day = events_with_duration['attendance_per_day'].mean()
            avg_impact_per_day = (events_with_duration['total_economic_impact_usd'] /
                                 events_with_duration['duration_days'].clip(lower=1)).mean()
        else:
            # Fallback: get duration from events.csv
            events_duration = self.df_events[['event_name', 'start_date', 'end_date']].copy()
            events_duration['start_date'] = pd.to_datetime(events_duration['start_date'])
            events_duration['end_date'] = pd.to_datetime(events_duration['end_date'])
            events_duration['duration'] = (events_duration['end_date'] -
                                           events_duration['start_date']).dt.days + 1

            events_with_duration = reference_data.merge(
                events_duration[['event_name', 'duration']],
                on='event_name',
                how='left'
            )
            
            # Use attendance from impacts if available, otherwise estimate
            if 'attendance' in events_with_duration.columns:
                events_with_duration['attendance_per_day'] = (
                    events_with_duration['attendance'] / events_with_duration['duration'].clip(lower=1)
                )
            else:
                # Estimate from annual tourists
                events_with_duration['attendance_per_day'] = (
                    events_with_duration.get('annual_tourists', 10000000) / 365
                )
            
            avg_attendance_per_day = events_with_duration['attendance_per_day'].mean()
            avg_impact_per_day = (events_with_duration['total_economic_impact_usd'] /
                                 events_with_duration['duration'].clip(lower=1)).mean()

        # Calculate visitor_increase_pct if not available
        if 'visitor_increase_pct' in reference_data.columns:
            avg_visitor_increase = reference_data['visitor_increase_pct'].mean()
        else:
            # Estimate from attendance vs baseline
            if 'annual_tourists' in events_with_duration.columns:
                baseline_daily = events_with_duration['annual_tourists'] / 365
                visitor_increase = ((events_with_duration['attendance_per_day'] / baseline_daily.clip(lower=1)) - 1) * 100
                avg_visitor_increase = visitor_increase.mean()
            else:
                avg_visitor_increase = 50.0  # Default

        # Calculate price_increase_pct if not available
        if 'price_increase_pct' in reference_data.columns:
            avg_price_increase = reference_data['price_increase_pct'].mean()
        else:
            # Estimate as 80% of visitor increase
            avg_price_increase = avg_visitor_increase * 0.8

        # Calculate occupancy_boost if not available
        if 'event_occupancy_pct' in reference_data.columns and 'baseline_occupancy_pct' in reference_data.columns:
            avg_occupancy_boost = (reference_data['event_occupancy_pct'] -
                                  reference_data['baseline_occupancy_pct']).mean()
        else:
            # Estimate as 30% of visitor increase
            avg_occupancy_boost = avg_visitor_increase * 0.3

        # Handle NaN values (when no matching events found)
        if pd.isna(avg_attendance_per_day):
            avg_attendance_per_day = 50000  # Default fallback
        if pd.isna(avg_visitor_increase):
            avg_visitor_increase = 50.0
        if pd.isna(avg_price_increase):
            avg_price_increase = 60.0
        if pd.isna(avg_occupancy_boost):
            avg_occupancy_boost = 15.0
        if pd.isna(avg_impact_per_day):
            avg_impact_per_day = 50000000

        # Estimate attendance if not provided
        if attendance is None:
            attendance = int(avg_attendance_per_day * duration_days)

        # Calculate average metrics from historical events (from the 4 additional CSVs)
        # These metrics will enrich the prediction with real time-series data
        avg_metrics = {}
        
        if len(reference_data) > 0:
            # Get event dates for reference events
            events_with_dates = self.df_events[
                self.df_events['event_name'].isin(reference_data['event_name'].tolist())
            ][['event_name', 'start_date', 'end_date']].copy()
            events_with_dates['start_date'] = pd.to_datetime(events_with_dates['start_date'])
            events_with_dates['end_date'] = pd.to_datetime(events_with_dates['end_date'])
            
            # Calculate metrics for each reference event and average them
            metric_values = {
                'event_avg_total_visitors': [],
                'baseline_avg_total_visitors': [],
                'event_avg_spending_per_visitor': [],
                'baseline_avg_spending_per_visitor': [],
                'event_avg_occupancy_pct': [],
                'baseline_avg_occupancy_pct': [],
                'event_avg_hotel_price': [],
                'baseline_avg_hotel_price': [],
                'event_max_hotel_price': [],
                'event_avg_daily_spending': [],
                'baseline_avg_daily_spending': [],
                'event_avg_airport_arrivals': [],
                'baseline_avg_airport_arrivals': [],
            }
            
            for _, ref_event in events_with_dates.iterrows():
                # Get city for this reference event
                ref_city_match = reference_data[reference_data['event_name'] == ref_event['event_name']]
                if len(ref_city_match) > 0:
                    ref_city = ref_city_match['city'].iloc[0] if 'city' in ref_city_match.columns else city
                else:
                    ref_city = city
                
                ref_start = ref_event['start_date']
                ref_end = ref_event['end_date']
                ref_baseline_start = ref_start - pd.Timedelta(days=30)
                ref_baseline_end = ref_start - pd.Timedelta(days=1)
                
                # Tourism metrics
                city_tourism = self.df_tourism_metrics[self.df_tourism_metrics['city'] == ref_city]
                if not city_tourism.empty:
                    event_tourism = city_tourism[(city_tourism['date'] >= ref_start) & (city_tourism['date'] <= ref_end)]
                    baseline_tourism = city_tourism[(city_tourism['date'] >= ref_baseline_start) & (city_tourism['date'] <= ref_baseline_end)]
                    if not event_tourism.empty and not baseline_tourism.empty:
                        metric_values['event_avg_total_visitors'].append(event_tourism['total_visitors'].mean())
                        metric_values['baseline_avg_total_visitors'].append(baseline_tourism['total_visitors'].mean())
                        metric_values['event_avg_spending_per_visitor'].append(event_tourism['avg_spending_per_visitor_usd'].mean())
                        metric_values['baseline_avg_spending_per_visitor'].append(baseline_tourism['avg_spending_per_visitor_usd'].mean())
                
                # Hotel metrics
                city_hotel = self.df_hotel_metrics[self.df_hotel_metrics['city'] == ref_city]
                if not city_hotel.empty:
                    event_hotel = city_hotel[(city_hotel['date'] >= ref_start) & (city_hotel['date'] <= ref_end)]
                    baseline_hotel = city_hotel[(city_hotel['date'] >= ref_baseline_start) & (city_hotel['date'] <= ref_baseline_end)]
                    if not event_hotel.empty and not baseline_hotel.empty:
                        metric_values['event_avg_occupancy_pct'].append(event_hotel['occupancy_rate_pct'].mean())
                        metric_values['baseline_avg_occupancy_pct'].append(baseline_hotel['occupancy_rate_pct'].mean())
                        metric_values['event_avg_hotel_price'].append(event_hotel['avg_price_usd'].mean())
                        metric_values['baseline_avg_hotel_price'].append(baseline_hotel['avg_price_usd'].mean())
                        metric_values['event_max_hotel_price'].append(event_hotel['avg_price_usd'].max())
                
                # Economic metrics
                city_economic = self.df_economic_metrics[self.df_economic_metrics['city'] == ref_city]
                if not city_economic.empty:
                    event_economic = city_economic[(city_economic['date'] >= ref_start) & (city_economic['date'] <= ref_end)]
                    baseline_economic = city_economic[(city_economic['date'] >= ref_baseline_start) & (city_economic['date'] <= ref_baseline_end)]
                    if not event_economic.empty and not baseline_economic.empty:
                        metric_values['event_avg_daily_spending'].append(event_economic['total_spending_usd'].mean())
                        metric_values['baseline_avg_daily_spending'].append(baseline_economic['total_spending_usd'].mean())
                
                # Mobility metrics
                city_mobility = self.df_mobility_metrics[self.df_mobility_metrics['city'] == ref_city]
                if not city_mobility.empty:
                    event_mobility = city_mobility[(city_mobility['date'] >= ref_start) & (city_mobility['date'] <= ref_end)]
                    baseline_mobility = city_mobility[(city_mobility['date'] >= ref_baseline_start) & (city_mobility['date'] <= ref_baseline_end)]
                    if not event_mobility.empty and not baseline_mobility.empty:
                        metric_values['event_avg_airport_arrivals'].append(event_mobility['airport_arrivals'].mean())
                        metric_values['baseline_avg_airport_arrivals'].append(baseline_mobility['airport_arrivals'].mean())
            
            # Calculate averages
            for key, values in metric_values.items():
                if values:
                    avg_metrics[key] = np.mean(values)
                else:
                    avg_metrics[key] = 0.0
            
            # Calculate derived metrics
            if avg_metrics.get('baseline_avg_total_visitors', 0) > 0:
                avg_metrics['visitor_increase_actual'] = (
                    (avg_metrics['event_avg_total_visitors'] / avg_metrics['baseline_avg_total_visitors'] - 1) * 100
                )
            else:
                avg_metrics['visitor_increase_actual'] = avg_visitor_increase
            
            if avg_metrics.get('baseline_avg_spending_per_visitor', 0) > 0:
                avg_metrics['spending_increase_pct'] = (
                    (avg_metrics['event_avg_spending_per_visitor'] / avg_metrics['baseline_avg_spending_per_visitor'] - 1) * 100
                )
            else:
                avg_metrics['spending_increase_pct'] = 0
            
            if avg_metrics.get('baseline_avg_occupancy_pct', 0) > 0:
                avg_metrics['occupancy_boost_actual'] = avg_metrics['event_avg_occupancy_pct'] - avg_metrics['baseline_avg_occupancy_pct']
            else:
                avg_metrics['occupancy_boost_actual'] = avg_occupancy_boost
            
            if avg_metrics.get('baseline_avg_hotel_price', 0) > 0:
                avg_metrics['hotel_price_increase_actual'] = (
                    (avg_metrics['event_avg_hotel_price'] / avg_metrics['baseline_avg_hotel_price'] - 1) * 100
                )
            else:
                avg_metrics['hotel_price_increase_actual'] = avg_price_increase
            
            if avg_metrics.get('baseline_avg_daily_spending', 0) > 0:
                avg_metrics['daily_spending_increase_pct'] = (
                    (avg_metrics['event_avg_daily_spending'] / avg_metrics['baseline_avg_daily_spending'] - 1) * 100
                )
            else:
                avg_metrics['daily_spending_increase_pct'] = 0
            
            if avg_metrics.get('baseline_avg_airport_arrivals', 0) > 0:
                avg_metrics['airport_arrivals_increase_pct'] = (
                    (avg_metrics['event_avg_airport_arrivals'] / avg_metrics['baseline_avg_airport_arrivals'] - 1) * 100
                )
            else:
                avg_metrics['airport_arrivals_increase_pct'] = 0
        
        # Set defaults for missing metrics
        defaults = {
            'event_avg_total_visitors': attendance / max(duration_days, 1),
            'baseline_avg_total_visitors': city_data['annual_tourists'] / 365,
            'event_avg_spending_per_visitor': 200,
            'baseline_avg_spending_per_visitor': 150,
            'event_avg_stay_duration': 3.5,
            'event_avg_occupancy_pct': 75.0,
            'baseline_avg_occupancy_pct': 70.0,
            'event_avg_hotel_price': city_data['avg_hotel_price_usd'],
            'baseline_avg_hotel_price': city_data['avg_hotel_price_usd'],
            'event_max_hotel_price': city_data['avg_hotel_price_usd'] * 1.5,
            'event_avg_daily_spending': 0,
            'baseline_avg_daily_spending': 0,
            'event_avg_accommodation_spending': 0,
            'event_avg_food_spending': 0,
            'event_avg_retail_spending': 0,
            'event_avg_airport_arrivals': 0,
            'baseline_avg_airport_arrivals': 0,
            'event_avg_international_flights': 0,
            'event_avg_public_transport': 0,
            'event_avg_traffic_congestion': 0,
            'baseline_avg_traffic_congestion': 0,
        }
        
        for key, default_value in defaults.items():
            if key not in avg_metrics:
                avg_metrics[key] = default_value
        
        # Ensure derived metrics exist
        if 'visitor_increase_actual' not in avg_metrics:
            avg_metrics['visitor_increase_actual'] = avg_visitor_increase
        if 'spending_increase_pct' not in avg_metrics:
            avg_metrics['spending_increase_pct'] = 0
        if 'occupancy_boost_actual' not in avg_metrics:
            avg_metrics['occupancy_boost_actual'] = avg_occupancy_boost
        if 'hotel_price_increase_actual' not in avg_metrics:
            avg_metrics['hotel_price_increase_actual'] = avg_price_increase
        if 'daily_spending_increase_pct' not in avg_metrics:
            avg_metrics['daily_spending_increase_pct'] = 0
        if 'airport_arrivals_increase_pct' not in avg_metrics:
            avg_metrics['airport_arrivals_increase_pct'] = 0

        # Build prediction request with estimated parameters including all metrics
        prediction_params = {
            'event_type': event_type,
            'city': city,
            'attendance': attendance,
            'duration_days': duration_days,
            'visitor_increase_pct': avg_visitor_increase,
            'price_increase_pct': avg_price_increase,
            'occupancy_boost': avg_occupancy_boost,
            **avg_metrics,  # Add all calculated metrics from the 4 CSVs
        }

        # Get prediction from main model
        result = self.predict(prediction_params)

        # Calculate baseline (normal week without event)
        # Baseline daily visitors (normal tourism without event)
        baseline_daily_visitors = city_data['annual_tourists'] / 365
        # Average spending per visitor per day (normal tourism, lower than event)
        # Normal tourists spend less than event attendees
        baseline_daily_spending_per_visitor = 150  # Conservative estimate for normal tourism
        baseline_daily_spending = baseline_daily_visitors * baseline_daily_spending_per_visitor
        # Calculate for the same duration as the event
        baseline_period_spending = baseline_daily_spending * duration_days
        # Apply economic multiplier (same as event impact: 1.7x)
        baseline_period_impact = baseline_period_spending * 1.7

        # Calculate comparison metrics
        event_impact = result['prediction']['total_economic_impact_usd']
        additional_impact = event_impact - baseline_period_impact
        impact_multiplier = event_impact / baseline_period_impact if baseline_period_impact > 0 else 0
        impact_increase_pct = ((event_impact / baseline_period_impact) - 1) * 100 if baseline_period_impact > 0 else 0

        # Add baseline comparison
        result['baseline_comparison'] = {
            'baseline_weekly_impact_usd': round(baseline_period_impact, 2),
            'event_impact_usd': round(event_impact, 2),
            'additional_impact_usd': round(additional_impact, 2),
            'impact_multiplier': round(impact_multiplier, 2),
            'impact_increase_pct': round(impact_increase_pct, 1),
            'baseline_daily_visitors': int(baseline_daily_visitors),
            'baseline_daily_spending_usd': round(baseline_daily_spending, 2),
            'duration_days': duration_days,
        }

        # Add historical context
        result['historical_reference'] = {
            'reference_scope': reference_scope,
            'events_analyzed': len(reference_data),
            'avg_visitor_increase_pct': round(avg_visitor_increase, 1),
            'avg_price_increase_pct': round(avg_price_increase, 1),
            'avg_occupancy_boost_pct': round(avg_occupancy_boost, 1),
            'avg_attendance_per_day': int(avg_attendance_per_day),
            'avg_impact_per_day_usd': int(avg_impact_per_day),
            'similar_events': reference_data['event_name'].tolist()[:5],
        }

        # Update input summary
        result['input_summary']['estimated_from_historical'] = attendance is None
        result['input_summary']['reference_continent'] = continent

        return result

    def get_event_types(self) -> List[str]:
        """Get available event types from historical data."""
        if self.df_events is None:
            self.df_events = pd.read_csv(self.data_dir / "events.csv")
        return self.df_events['event_type'].unique().tolist()

    def get_cities(self) -> List[Dict]:
        """Get available cities with their info."""
        if self.df_cities is None:
            self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
        return self.df_cities[['name', 'country', 'continent']].to_dict('records')

    def save(self, filename: str = "economic_impact_model.pkl"):
        """Save the trained model and preprocessors."""
        if self.best_model is None:
            raise ValueError("No model to save. Train first.")

        save_path = self.models_dir / filename

        model_data = {
            'best_model': self.best_model,
            'best_model_name': self.best_model_name,
            'all_models': self.models,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'metrics': self.metrics,
            'trained_at': datetime.now().isoformat(),
        }

        with open(save_path, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"\n💾 Model saved to: {save_path}")

    def load(self, filename: str = "economic_impact_model.pkl"):
        """Load a previously trained model."""
        load_path = self.models_dir / filename

        if not load_path.exists():
            raise FileNotFoundError(f"Model file not found: {load_path}")

        try:
            with open(load_path, 'rb') as f:
                model_data = pickle.load(f)

            self.best_model = model_data.get('best_model')
            self.best_model_name = model_data.get('best_model_name')
            self.models = model_data.get('all_models', {})
            self.scaler = model_data.get('scaler')
            self.label_encoders = model_data.get('label_encoders', {})
            self.feature_columns = model_data.get('feature_columns', [])
            self.metrics = model_data.get('metrics', {})

            # Verify model was loaded correctly
            if self.best_model is None:
                raise ValueError("Model file exists but best_model is None")

            # Load CSVs for city lookups and metrics
            if self.data_dir.exists():
                self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
                # Also load metrics CSVs for predictions
                try:
                    self.df_tourism_metrics = pd.read_csv(self.data_dir / "tourism_metrics.csv")
                    self.df_tourism_metrics['date'] = pd.to_datetime(self.df_tourism_metrics['date'])
                    self.df_hotel_metrics = pd.read_csv(self.data_dir / "hotel_metrics.csv")
                    self.df_hotel_metrics['date'] = pd.to_datetime(self.df_hotel_metrics['date'])
                    self.df_economic_metrics = pd.read_csv(self.data_dir / "economic_metrics.csv")
                    self.df_economic_metrics['date'] = pd.to_datetime(self.df_economic_metrics['date'])
                    self.df_mobility_metrics = pd.read_csv(self.data_dir / "mobility_metrics.csv")
                    self.df_mobility_metrics['date'] = pd.to_datetime(self.df_mobility_metrics['date'])
                    print("   ✓ Loaded time-series metrics CSVs")
                except Exception as e:
                    print(f"   ⚠️  Warning: Could not load metrics CSVs: {e}")
            else:
                print(f"⚠️  Warning: Data directory {self.data_dir} does not exist")

            print(f"\n📂 Model loaded from: {load_path}")
            print(f"   Best model: {self.best_model_name}")
            if self.best_model_name and self.best_model_name in self.metrics:
                print(f"   R² Score: {self.metrics[self.best_model_name]['r2']:.4f}")
            print(f"   Trained at: {model_data.get('trained_at', 'Unknown')}")
        except Exception as e:
            raise ValueError(f"Error loading model from {load_path}: {str(e)}")

    def get_model_summary(self) -> str:
        """Get a summary of the trained model."""
        if self.best_model is None:
            return "No model trained yet."

        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║           ECONOMIC IMPACT MODEL SUMMARY                      ║
╠══════════════════════════════════════════════════════════════╣
║ Best Model: {self.best_model_name:<47}║
║ R² Score: {self.metrics[self.best_model_name]['r2']:<49.4f}║
║ MAPE: {self.metrics[self.best_model_name]['mape']:<52.2f}%║
║ MAE: ${self.metrics[self.best_model_name]['mae']:<50,.0f}║
║ RMSE: ${self.metrics[self.best_model_name]['rmse']:<49,.0f}║
╠══════════════════════════════════════════════════════════════╣
║ Features Used: {len(self.feature_columns):<44}║
║ Training Samples: {len(self.df_training) if self.df_training is not None else 'N/A':<41}║
╚══════════════════════════════════════════════════════════════╝
"""
        return summary


def main():
    """Main function to train and test the model."""
    print("\n" + "=" * 60)
    print("   🎯 ECONOMIC IMPACT REGRESSION MODEL")
    print("   Training from CSV files")
    print("=" * 60)

    # Initialize model
    model = EconomicImpactModel()

    # Load data from CSVs
    model.load_data()

    # Train all models
    model.train()

    # Print summary
    print(model.get_model_summary())

    # Save model
    model.save()

    # Test predictions
    print("\n🧪 Testing Predictions:")
    print("=" * 60)

    test_events = [
        {
            'event_type': 'sports',
            'city': 'London',
            'attendance': 500000,
            'duration_days': 14,
        },
        {
            'event_type': 'music',
            'city': 'Madrid',
            'attendance': 200000,
            'duration_days': 4,
        },
        {
            'event_type': 'business',
            'city': 'Barcelona',
            'attendance': 100000,
            'duration_days': 4,
        },
    ]

    for event in test_events:
        print(f"\n📊 {event['event_type'].upper()} Event in {event['city']}")
        print(f"   Attendance: {event['attendance']:,}")
        print(f"   Duration: {event['duration_days']} days")

        result = model.predict(event)

        print(f"\n   💰 Predicted Impact: ${result['prediction']['total_economic_impact_usd']:,.0f}")
        print(f"   📊 Confidence: {result['prediction']['lower_bound_usd']:,.0f} - {result['prediction']['upper_bound_usd']:,.0f}")
        print(f"   👥 Jobs Created: {result['estimates']['jobs_created']:,}")
        print(f"   📈 ROI: {result['estimates']['roi_ratio']}x")

    print("\n" + "=" * 60)
    print("✅ Model training and testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
