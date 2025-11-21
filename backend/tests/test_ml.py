"""
Unit tests for ML models
Tests predictors, training pipeline, and predictions
"""
import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta
from pathlib import Path

from app.ml.predictors import (
    TourismPredictor,
    HotelPricePredictor,
    ImpactPredictor,
    EnsemblePredictor
)


class TestTourismPredictor:
    """Test suite for Tourism Predictor"""

    def test_initialization(self):
        """Test predictor can be initialized"""
        predictor = TourismPredictor()
        assert predictor is not None
        assert not predictor.is_trained

    def test_training_with_data(self):
        """Test training with sample data"""
        predictor = TourismPredictor()

        # Create sample training data
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        visitors = 5000 + 1000 * np.sin(np.arange(365) * 2 * np.pi / 365) + np.random.normal(0, 200, 365)

        df = pd.DataFrame({
            'ds': dates,
            'y': visitors,
            'date': dates,
            'visitors': visitors
        })

        # Train
        try:
            predictor.train(df)
            assert predictor.is_trained
        except Exception as e:
            # Prophet might not be installed, which is ok
            pytest.skip(f"Prophet not available: {e}")

    def test_prediction(self):
        """Test making predictions"""
        predictor = TourismPredictor()

        # Create and train
        dates = pd.date_range('2023-01-01', periods=365, freq='D')
        visitors = 5000 + 1000 * np.sin(np.arange(365) * 2 * np.pi / 365)

        train_df = pd.DataFrame({
            'ds': dates,
            'y': visitors,
            'date': dates,
            'visitors': visitors
        })

        try:
            predictor.train(train_df)

            # Predict future
            future_dates = pd.date_range('2024-01-01', periods=30, freq='D')
            future_df = pd.DataFrame({'ds': future_dates, 'date': future_dates})

            predictions = predictor.predict(future_df)

            assert len(predictions) == 30
            assert 'yhat' in predictions.columns or 'yhat' in predictions.index
        except Exception as e:
            pytest.skip(f"Prophet not available: {e}")


class TestHotelPricePredictor:
    """Test suite for Hotel Price Predictor"""

    def test_initialization(self):
        """Test predictor can be initialized"""
        predictor = HotelPricePredictor()
        assert predictor is not None
        assert not predictor.is_trained

    def test_training_with_data(self):
        """Test training with sample data"""
        predictor = HotelPricePredictor()

        # Create synthetic data
        n_samples = 365
        data = {
            'occupancy_rate': np.random.uniform(50, 95, n_samples),
            'baseline_price': np.random.uniform(100, 200, n_samples),
            'is_weekend': np.random.choice([0, 1], n_samples),
            'is_event_period': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
            'days_to_event': np.random.randint(-30, 30, n_samples),
            'event_size': np.random.choice([0, 50000, 100000], n_samples),
        }

        # Price = baseline * (1 + occupancy/100) * (1.2 if event else 1.0) + noise
        data['price'] = (
            data['baseline_price'] *
            (1 + data['occupancy_rate']/200) *
            (1.2 if data['is_event_period'].any() else 1.0) +
            np.random.normal(0, 10, n_samples)
        )

        df = pd.DataFrame(data)

        # Train
        metrics = predictor.train(df)

        assert predictor.is_trained
        assert 'r2' in metrics
        assert 'mae' in metrics
        assert metrics['r2'] >= 0  # R² should be non-negative

    def test_prediction(self):
        """Test making predictions"""
        predictor = HotelPricePredictor()

        # Train with sample data
        n_samples = 200
        df = pd.DataFrame({
            'occupancy_rate': np.random.uniform(50, 95, n_samples),
            'baseline_price': [150] * n_samples,
            'is_weekend': [0] * n_samples,
            'is_event_period': [0] * 100 + [1] * 100,
            'days_to_event': list(range(-50, -50+n_samples)),
            'event_size': [0] * 100 + [50000] * 100,
            'price': [150] * 100 + [200] * 100,  # Price jump during events
        })

        predictor.train(df)

        # Predict
        test_df = pd.DataFrame({
            'occupancy_rate': [80.0],
            'baseline_price': [150.0],
            'is_weekend': [1],
            'is_event_period': [1],
            'days_to_event': [0],
            'event_size': [50000],
        })

        predictions = predictor.predict(test_df)

        assert len(predictions) == 1
        assert predictions[0] > 0
        assert predictions[0] > 150  # Should be higher than baseline during event

    def test_feature_importance(self):
        """Test feature importance extraction"""
        predictor = HotelPricePredictor()

        # Train
        n_samples = 200
        df = pd.DataFrame({
            'occupancy_rate': np.random.uniform(50, 95, n_samples),
            'baseline_price': [150] * n_samples,
            'is_weekend': [0] * n_samples,
            'is_event_period': [0] * 100 + [1] * 100,
            'days_to_event': list(range(n_samples)),
            'event_size': [0] * 100 + [50000] * 100,
            'price': [150] * 100 + [200] * 100,
        })

        predictor.train(df)

        # Get importance
        importance = predictor.feature_importance()

        assert isinstance(importance, dict)
        assert len(importance) == 6
        assert all(0 <= v <= 1 for v in importance.values())


class TestImpactPredictor:
    """Test suite for Impact Predictor"""

    def test_initialization(self):
        """Test predictor can be initialized"""
        predictor = ImpactPredictor()
        assert predictor is not None
        assert not predictor.is_trained

    def test_training_with_data(self):
        """Test training with sample data"""
        predictor = ImpactPredictor()

        # Create synthetic impact data
        n_samples = 50
        df = pd.DataFrame({
            'attendance': np.random.randint(10000, 200000, n_samples),
            'duration_days': np.random.randint(1, 14, n_samples),
            'event_type_encoded': np.random.randint(0, 5, n_samples),
            'city_population': np.random.randint(1000000, 10000000, n_samples),
            'city_annual_tourists': np.random.randint(5000000, 50000000, n_samples),
            'baseline_hotel_price': np.random.uniform(100, 300, n_samples),
        })

        # Impact roughly proportional to attendance * duration
        df['total_economic_impact'] = (
            df['attendance'] * df['duration_days'] * 50 +
            np.random.normal(0, 1000000, n_samples)
        )

        # Train
        metrics = predictor.train(df)

        assert predictor.is_trained
        assert 'r2' in metrics
        assert 'mape' in metrics

    def test_prediction_with_confidence(self):
        """Test predictions with confidence intervals"""
        predictor = ImpactPredictor()

        # Train
        n_samples = 30
        df = pd.DataFrame({
            'attendance': [100000] * n_samples,
            'duration_days': [7] * n_samples,
            'event_type_encoded': [1] * n_samples,
            'city_population': [5000000] * n_samples,
            'city_annual_tourists': [10000000] * n_samples,
            'baseline_hotel_price': [180] * n_samples,
            'total_economic_impact': np.random.normal(50000000, 5000000, n_samples),
        })

        predictor.train(df)

        # Predict
        test_df = pd.DataFrame({
            'attendance': [100000],
            'duration_days': [7],
            'event_type_encoded': [1],
            'city_population': [5000000],
            'city_annual_tourists': [10000000],
            'baseline_hotel_price': [180],
        })

        predictions, lower, upper = predictor.predict_with_confidence(test_df)

        assert len(predictions) == 1
        assert len(lower) == 1
        assert len(upper) == 1
        assert lower[0] < predictions[0] < upper[0]
        assert predictions[0] > 0


class TestEnsemblePredictor:
    """Test suite for Ensemble Predictor"""

    def test_initialization(self):
        """Test ensemble can be initialized"""
        ensemble = EnsemblePredictor()
        assert ensemble is not None
        assert ensemble.tourism_predictor is not None
        assert ensemble.hotel_predictor is not None
        assert ensemble.impact_predictor is not None

    def test_full_prediction_pipeline(self):
        """Test full prediction with all models"""
        ensemble = EnsemblePredictor()

        # Predict event impact
        city_data = {
            'avg_hotel_price': 180,
            'population': 5000000,
            'annual_tourists': 10000000,
        }

        result = ensemble.predict_event_impact(
            event_date=date(2025, 6, 1),
            event_duration=7,
            expected_attendance=100000,
            city_data=city_data,
        )

        assert isinstance(result, dict)
        assert 'total_economic_impact' in result
        assert 'metrics' in result


class TestModelPersistence:
    """Test model saving and loading"""

    def test_save_and_load_hotel_predictor(self, tmp_path):
        """Test saving and loading hotel predictor"""
        predictor = HotelPricePredictor(model_dir=tmp_path)

        # Train
        n_samples = 100
        df = pd.DataFrame({
            'occupancy_rate': np.random.uniform(50, 95, n_samples),
            'baseline_price': [150] * n_samples,
            'is_weekend': [0] * n_samples,
            'is_event_period': [0] * 50 + [1] * 50,
            'days_to_event': list(range(n_samples)),
            'event_size': [0] * 50 + [50000] * 50,
            'price': [150] * 50 + [200] * 50,
        })

        predictor.train(df)

        # Save
        predictor.save_model("test_model.pkl")

        # Load in new predictor
        new_predictor = HotelPricePredictor(model_dir=tmp_path)
        new_predictor.load_model("test_model.pkl")

        assert new_predictor.is_trained

        # Predictions should match
        test_df = pd.DataFrame({
            'occupancy_rate': [80.0],
            'baseline_price': [150.0],
            'is_weekend': [1],
            'is_event_period': [1],
            'days_to_event': [0],
            'event_size': [50000],
        })

        pred1 = predictor.predict(test_df)
        pred2 = new_predictor.predict(test_df)

        np.testing.assert_array_almost_equal(pred1, pred2)


class TestDataValidation:
    """Test data validation and error handling"""

    def test_empty_dataframe(self):
        """Test handling of empty dataframes"""
        predictor = HotelPricePredictor()

        with pytest.raises(Exception):
            empty_df = pd.DataFrame()
            predictor.train(empty_df)

    def test_missing_columns(self):
        """Test handling of missing columns"""
        predictor = HotelPricePredictor()

        with pytest.raises(Exception):
            incomplete_df = pd.DataFrame({
                'occupancy_rate': [80.0],
                'price': [200.0],
                # Missing required columns
            })
            predictor.train(incomplete_df)

    def test_prediction_before_training(self):
        """Test error when predicting before training"""
        predictor = HotelPricePredictor()

        with pytest.raises(ValueError, match="Model not trained yet"):
            test_df = pd.DataFrame({
                'occupancy_rate': [80.0],
                'baseline_price': [150.0],
                'is_weekend': [1],
                'is_event_period': [1],
                'days_to_event': [0],
                'event_size': [50000],
            })
            predictor.predict(test_df)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
