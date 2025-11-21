"""
ML Predictors for Evently
Uses Prophet and scikit-learn for time series forecasting
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
import pickle
from pathlib import Path

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Warning: Prophet not installed. Install with: pip install prophet")

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class BasePredictor:
    """Base class for all predictors"""

    def __init__(self, model_dir: Path = None):
        self.model = None
        self.is_trained = False
        self.metrics = {}
        self.model_dir = model_dir or Path(__file__).parent / "saved_models"
        self.model_dir.mkdir(exist_ok=True)

    def save_model(self, filename: str):
        """Save trained model to disk"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")

        filepath = self.model_dir / filename
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)

        print(f"✅ Model saved to {filepath}")

    def load_model(self, filename: str):
        """Load model from disk"""
        filepath = self.model_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")

        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)

        self.is_trained = True
        print(f"✅ Model loaded from {filepath}")

    def calculate_metrics(self, y_true, y_pred) -> Dict:
        """Calculate regression metrics"""
        return {
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
            "r2": float(r2_score(y_true, y_pred)),
            "mape": float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100),
        }


class TourismPredictor(BasePredictor):
    """
    Predict visitor numbers using Prophet (time series with seasonality)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if PROPHET_AVAILABLE:
            self.model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
            )
        else:
            # Fallback to simple regression
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.use_prophet = False

    def train(self, df: pd.DataFrame):
        """
        Train on historical visitor data

        Args:
            df: DataFrame with columns ['ds', 'y'] for Prophet
                or ['date', 'visitors', 'day_of_week', 'month', ...] for regression
        """
        if PROPHET_AVAILABLE and hasattr(self.model, 'fit'):
            # Prophet format: ds (date), y (value)
            self.model.fit(df)
        else:
            # Fallback: extract features
            X = self._extract_features(df)
            y = df['visitors'].values
            self.model.fit(X, y)

        self.is_trained = True
        print("✅ Tourism model trained")

    def predict(self, future_dates: pd.DataFrame) -> pd.DataFrame:
        """Predict visitor numbers for future dates"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")

        if PROPHET_AVAILABLE and hasattr(self.model, 'predict'):
            forecast = self.model.predict(future_dates)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        else:
            X = self._extract_features(future_dates)
            predictions = self.model.predict(X)
            return pd.DataFrame({
                'ds': future_dates['date'],
                'yhat': predictions,
                'yhat_lower': predictions * 0.9,
                'yhat_upper': predictions * 1.1,
            })

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract time-based features for non-Prophet models"""
        features = []
        for _, row in df.iterrows():
            dt = pd.to_datetime(row['date'] if 'date' in row else row['ds'])
            features.append([
                dt.dayofweek,
                dt.month,
                dt.day,
                dt.dayofyear,
                int(dt.dayofweek >= 5),  # is_weekend
            ])
        return np.array(features)


class HotelPricePredictor(BasePredictor):
    """
    Predict hotel prices based on occupancy, seasonality, and events
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

    def train(self, df: pd.DataFrame):
        """
        Train on historical hotel data

        Args:
            df: DataFrame with columns:
                - occupancy_rate
                - baseline_price
                - is_weekend
                - is_event_period
                - days_to_event
                - event_size (attendance)
                - price (target)
        """
        feature_cols = [
            'occupancy_rate', 'baseline_price', 'is_weekend',
            'is_event_period', 'days_to_event', 'event_size'
        ]

        X = df[feature_cols].fillna(0).values
        y = df['price'].values

        # Split train/test
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Train
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        self.metrics = self.calculate_metrics(y_test, y_pred)

        self.is_trained = True
        print(f"✅ Hotel price model trained (R² = {self.metrics['r2']:.3f})")

        return self.metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict hotel prices"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")

        feature_cols = [
            'occupancy_rate', 'baseline_price', 'is_weekend',
            'is_event_period', 'days_to_event', 'event_size'
        ]

        X_features = X[feature_cols].fillna(0).values
        return self.model.predict(X_features)

    def feature_importance(self) -> Dict[str, float]:
        """Get feature importances"""
        if not self.is_trained:
            return {}

        feature_names = [
            'occupancy_rate', 'baseline_price', 'is_weekend',
            'is_event_period', 'days_to_event', 'event_size'
        ]

        importances = self.model.feature_importances_
        return dict(zip(feature_names, importances))


class ImpactPredictor(BasePredictor):
    """
    Predict total economic impact based on event characteristics
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = LinearRegression()

    def train(self, df: pd.DataFrame):
        """
        Train on historical event impacts

        Args:
            df: DataFrame with columns:
                - attendance
                - duration_days
                - event_type_encoded
                - city_population
                - city_annual_tourists
                - baseline_hotel_price
                - total_economic_impact (target)
        """
        feature_cols = [
            'attendance', 'duration_days', 'event_type_encoded',
            'city_population', 'city_annual_tourists', 'baseline_hotel_price'
        ]

        X = df[feature_cols].fillna(0).values
        y = df['total_economic_impact'].values

        # Log transform target for better fit
        y_log = np.log1p(y)

        # Split train/test
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y_log[:split_idx], y_log[split_idx:]

        # Train
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred_log = self.model.predict(X_test)
        y_pred = np.expm1(y_pred_log)
        y_test_original = np.expm1(y_test)

        self.metrics = self.calculate_metrics(y_test_original, y_pred)

        self.is_trained = True
        print(f"✅ Impact model trained (R² = {self.metrics['r2']:.3f}, MAPE = {self.metrics['mape']:.1f}%)")

        return self.metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict economic impact"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")

        feature_cols = [
            'attendance', 'duration_days', 'event_type_encoded',
            'city_population', 'city_annual_tourists', 'baseline_hotel_price'
        ]

        X_features = X[feature_cols].fillna(0).values

        # Predict in log space and transform back
        y_log = self.model.predict(X_features)
        return np.expm1(y_log)

    def predict_with_confidence(self, X: pd.DataFrame, confidence: float = 0.9) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Predict with confidence intervals

        Returns:
            Tuple of (predictions, lower_bound, upper_bound)
        """
        predictions = self.predict(X)

        # Estimate confidence based on training RMSE
        rmse = self.metrics.get('rmse', predictions.std())
        margin = rmse * 1.96  # 95% confidence

        lower = predictions - margin
        upper = predictions + margin

        return predictions, lower, upper


class EnsemblePredictor:
    """
    Ensemble of multiple predictors for robust predictions
    """

    def __init__(self):
        self.tourism_predictor = TourismPredictor()
        self.hotel_predictor = HotelPricePredictor()
        self.impact_predictor = ImpactPredictor()

    def predict_event_impact(
        self,
        event_date: date,
        event_duration: int,
        expected_attendance: int,
        city_data: Dict,
    ) -> Dict:
        """
        Predict full impact of an event

        Returns comprehensive prediction including:
        - Visitor increase
        - Hotel price changes
        - Total economic impact
        - Confidence intervals
        """
        # Prepare future dates
        start_date = event_date - timedelta(days=30)
        end_date = event_date + timedelta(days=30)
        dates = pd.date_range(start_date, end_date, freq='D')

        future_df = pd.DataFrame({'ds': dates})

        # Predict visitors
        if self.tourism_predictor.is_trained:
            visitor_forecast = self.tourism_predictor.predict(future_df)
        else:
            visitor_forecast = None

        # Predict hotel prices
        if self.hotel_predictor.is_trained:
            hotel_df = pd.DataFrame({
                'occupancy_rate': [75.0] * len(dates),
                'baseline_price': [city_data.get('avg_hotel_price', 150)] * len(dates),
                'is_weekend': [d.dayofweek >= 5 for d in dates],
                'is_event_period': [(event_date <= d.date() < event_date + timedelta(days=event_duration)) for d in dates],
                'days_to_event': [(event_date - d.date()).days for d in dates],
                'event_size': [expected_attendance] * len(dates),
            })
            hotel_prices = self.hotel_predictor.predict(hotel_df)
        else:
            hotel_prices = None

        # Predict total impact
        if self.impact_predictor.is_trained:
            impact_df = pd.DataFrame({
                'attendance': [expected_attendance],
                'duration_days': [event_duration],
                'event_type_encoded': [1],  # Default
                'city_population': [city_data.get('population', 1000000)],
                'city_annual_tourists': [city_data.get('annual_tourists', 5000000)],
                'baseline_hotel_price': [city_data.get('avg_hotel_price', 150)],
            })
            total_impact, impact_lower, impact_upper = self.impact_predictor.predict_with_confidence(impact_df)
        else:
            total_impact = impact_lower = impact_upper = None

        return {
            "visitor_forecast": visitor_forecast.to_dict() if visitor_forecast is not None else None,
            "hotel_prices": hotel_prices.tolist() if hotel_prices is not None else None,
            "total_economic_impact": {
                "prediction": float(total_impact[0]) if total_impact is not None else None,
                "lower_bound": float(impact_lower[0]) if impact_lower is not None else None,
                "upper_bound": float(impact_upper[0]) if impact_upper is not None else None,
            },
            "metrics": {
                "tourism": self.tourism_predictor.metrics,
                "hotel": self.hotel_predictor.metrics,
                "impact": self.impact_predictor.metrics,
            }
        }
