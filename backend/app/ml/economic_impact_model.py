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
                Path("/home/user/Evently/data/examples"),
            ]
            for path in possible_paths:
                if path.exists():
                    data_dir = path
                    break

        self.data_dir = Path(data_dir) if data_dir else Path("data/examples")
        self.models_dir = Path(__file__).parent / "saved_models"
        self.models_dir.mkdir(exist_ok=True)

        # Data
        self.df_events = None
        self.df_cities = None
        self.df_impacts = None
        self.df_training = None

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

    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV files and prepare for training.

        Returns:
            DataFrame ready for training
        """
        print("\n📂 Loading data from CSV files...")
        print(f"   Directory: {self.data_dir}")

        # Load CSVs
        self.df_events = pd.read_csv(self.data_dir / "events.csv")
        self.df_cities = pd.read_csv(self.data_dir / "cities.csv")
        self.df_impacts = pd.read_csv(self.data_dir / "event_impacts.csv")

        print(f"   ✓ events.csv: {len(self.df_events)} events")
        print(f"   ✓ cities.csv: {len(self.df_cities)} cities")
        print(f"   ✓ event_impacts.csv: {len(self.df_impacts)} impact records")

        # Merge data
        self.df_training = self._prepare_training_data()

        print(f"\n   📊 Training dataset: {len(self.df_training)} samples")
        print(f"   📊 Features: {len(self.feature_columns)} columns")

        return self.df_training

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

        # Get event type from events.csv
        event_types = self.df_events[['event_name', 'event_type']].drop_duplicates()
        # Match by event name prefix (remove year)
        df['event_base_name'] = df['event_name'].str.replace(r'\s*\d{4}$', '', regex=True)
        event_types['event_base_name'] = event_types['event_name'].str.replace(r'\s*\d{4}$', '', regex=True)

        df = df.merge(
            event_types[['event_base_name', 'event_type']].drop_duplicates(),
            on='event_base_name',
            how='left'
        )

        # Calculate duration from events.csv
        events_duration = self.df_events[['event_name', 'start_date', 'end_date']].copy()
        events_duration['start_date'] = pd.to_datetime(events_duration['start_date'])
        events_duration['end_date'] = pd.to_datetime(events_duration['end_date'])
        events_duration['duration_days'] = (events_duration['end_date'] - events_duration['start_date']).dt.days + 1

        df = df.merge(
            events_duration[['event_name', 'duration_days']],
            on='event_name',
            how='left'
        )

        # Get attendance from impacts (additional_visitors or calculate from visitor increase)
        df['attendance'] = df['additional_visitors'].fillna(
            df['baseline_daily_visitors'] * df['visitor_increase_pct'] / 100 * df['duration_days']
        )

        # Create derived features
        df['attendance_per_day'] = df['attendance'] / df['duration_days'].clip(lower=1)
        df['visitors_per_hotel_room'] = df['attendance'] / df['hotel_rooms'].clip(lower=1)
        df['city_tourism_intensity'] = df['annual_tourists'] / df['population'].clip(lower=1)
        df['price_sensitivity'] = df['price_increase_pct'] / df['visitor_increase_pct'].clip(lower=0.1)
        df['occupancy_boost'] = df['event_occupancy_pct'] - df['baseline_occupancy_pct']

        # Encode categorical variables
        if 'event_type' in df.columns:
            self.label_encoders['event_type'] = LabelEncoder()
            df['event_type_encoded'] = self.label_encoders['event_type'].fit_transform(
                df['event_type'].fillna('other')
            )

        # Define feature columns
        self.feature_columns = [
            # Event characteristics
            'attendance',
            'duration_days',
            'event_type_encoded',
            'visitor_increase_pct',
            'price_increase_pct',
            'occupancy_boost',

            # City characteristics
            'population',
            'annual_tourists',
            'hotel_rooms',
            'avg_hotel_price_usd',

            # Derived features
            'attendance_per_day',
            'visitors_per_hotel_room',
            'city_tourism_intensity',
        ]

        # Keep only rows with target variable
        df = df[df[self.target_column].notna()]

        # Fill missing values
        for col in self.feature_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())

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
                'mape': np.mean(np.abs((y_test_original - y_pred) / y_test_original)) * 100,
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

        # Build feature vector
        features = [
            attendance,
            duration_days,
            event_type_encoded,
            visitor_increase_pct,
            price_increase_pct,
            occupancy_boost,
            population,
            annual_tourists,
            hotel_rooms,
            avg_hotel_price,
            attendance / max(duration_days, 1),  # attendance_per_day
            attendance / max(hotel_rooms, 1),    # visitors_per_hotel_room
            annual_tourists / max(population, 1), # city_tourism_intensity
        ]

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

        # Estimate jobs created (rough: $40,000 per job created)
        jobs_created = int(prediction / 40000)

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
        avg_visitor_increase = reference_data['visitor_increase_pct'].mean()
        avg_price_increase = reference_data['price_increase_pct'].mean()
        avg_occupancy_boost = (reference_data['event_occupancy_pct'] -
                              reference_data['baseline_occupancy_pct']).mean()

        # Calculate average attendance per day
        # Get duration info from events dataframe
        events_duration = self.df_events[['event_name', 'start_date', 'end_date']].copy()
        events_duration['start_date'] = pd.to_datetime(events_duration['start_date'])
        events_duration['end_date'] = pd.to_datetime(events_duration['end_date'])
        events_duration['duration'] = (events_duration['end_date'] -
                                       events_duration['start_date']).dt.days + 1

        # Merge duration with reference data
        events_with_duration = reference_data.merge(
            events_duration[['event_name', 'duration']],
            on='event_name',
            how='left'
        )
        events_with_duration['attendance_per_day'] = (
            events_with_duration['additional_visitors'] / events_with_duration['duration'].clip(lower=1)
        )

        avg_attendance_per_day = events_with_duration['attendance_per_day'].mean()
        avg_impact_per_day = (events_with_duration['total_economic_impact_usd'] /
                             events_with_duration['duration'].clip(lower=1)).mean()

        # Handle NaN values (when no matching events found)
        if pd.isna(avg_attendance_per_day):
            avg_attendance_per_day = 50000  # Default fallback
        if pd.isna(avg_visitor_increase):
            avg_visitor_increase = 50.0
        if pd.isna(avg_price_increase):
            avg_price_increase = 60.0
        if pd.isna(avg_occupancy_boost):
            avg_occupancy_boost = 20.0
        if pd.isna(avg_impact_per_day):
            avg_impact_per_day = 50000000

        # Estimate attendance if not provided
        if attendance is None:
            attendance = int(avg_attendance_per_day * duration_days)

        # Build prediction request with estimated parameters
        prediction_params = {
            'event_type': event_type,
            'city': city,
            'attendance': attendance,
            'duration_days': duration_days,
            'visitor_increase_pct': avg_visitor_increase,
            'price_increase_pct': avg_price_increase,
            'occupancy_boost': avg_occupancy_boost,
        }

        # Get prediction from main model
        result = self.predict(prediction_params)

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

        with open(load_path, 'rb') as f:
            model_data = pickle.load(f)

        self.best_model = model_data['best_model']
        self.best_model_name = model_data['best_model_name']
        self.models = model_data['all_models']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.metrics = model_data['metrics']

        # Load CSVs for city lookups
        self.df_cities = pd.read_csv(self.data_dir / "cities.csv")

        print(f"\n📂 Model loaded from: {load_path}")
        print(f"   Best model: {self.best_model_name}")
        print(f"   R² Score: {self.metrics[self.best_model_name]['r2']:.4f}")
        print(f"   Trained at: {model_data.get('trained_at', 'Unknown')}")

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
