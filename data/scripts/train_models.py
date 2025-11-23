"""
Train ML models using historical data
UNESCO MVP - Model Training Pipeline
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from app.core.database import SessionLocal
from app.models import (
    City, Event, EventType,
    TourismMetric, HotelMetric, EventImpact
)
from app.ml.predictors import (
    TourismPredictor,
    HotelPricePredictor,
    ImpactPredictor,
    EnsemblePredictor
)


class ModelTrainer:
    """Orchestrates training of all ML models"""

    def __init__(self, db):
        self.db = db
        self.tourism_predictor = TourismPredictor()
        self.hotel_predictor = HotelPricePredictor()
        self.impact_predictor = ImpactPredictor()

    def prepare_tourism_data(self, city_id: int = None) -> pd.DataFrame:
        """Prepare tourism data for training"""
        print("\n📊 Preparing tourism data...")

        query = self.db.query(TourismMetric)
        if city_id:
            query = query.filter(TourismMetric.city_id == city_id)

        metrics = query.order_by(TourismMetric.date).all()

        if not metrics:
            print("  ⚠️  No tourism data found")
            return pd.DataFrame()

        # Prophet format: ds (datetime), y (target value)
        data = []
        for m in metrics:
            data.append({
                'ds': pd.to_datetime(m.date),
                'y': m.total_visitors or 0,
                'date': m.date,
                'visitors': m.total_visitors or 0,
            })

        df = pd.DataFrame(data)
        print(f"  ✅ Prepared {len(df)} tourism records")
        return df

    def prepare_hotel_data(self, city_id: int = None) -> pd.DataFrame:
        """Prepare hotel pricing data for training"""
        print("\n🏨 Preparing hotel data...")

        # Query hotels and events
        query = self.db.query(HotelMetric, City).join(City)
        if city_id:
            query = query.filter(HotelMetric.city_id == city_id)

        results = query.order_by(HotelMetric.date).all()

        if not results:
            print("  ⚠️  No hotel data found")
            return pd.DataFrame()

        # Get all events for context
        events = self.db.query(Event).all()
        event_map = {}
        for event in events:
            for i in range((event.end_date - event.start_date).days + 1):
                event_date = event.start_date + timedelta(days=i)
                if event_date not in event_map:
                    event_map[event_date] = []
                event_map[event_date].append(event)

        # Build feature matrix
        data = []
        for hotel, city in results:
            # Check if this date has an event
            events_on_date = event_map.get(hotel.date, [])
            is_event_period = len(events_on_date) > 0
            event_size = sum(e.actual_attendance or e.expected_attendance or 0 for e in events_on_date)

            # Calculate days to nearest event
            days_to_event = 999
            for event_date, _ in event_map.items():
                days_diff = abs((event_date - hotel.date).days)
                days_to_event = min(days_to_event, days_diff)

            data.append({
                'date': hotel.date,
                'occupancy_rate': hotel.occupancy_rate_pct or 70.0,
                'baseline_price': city.avg_hotel_price_usd or 150.0,
                'is_weekend': hotel.date.weekday() >= 5,
                'is_event_period': is_event_period,
                'days_to_event': days_to_event,
                'event_size': event_size,
                'price': hotel.avg_price_usd or city.avg_hotel_price_usd,
            })

        df = pd.DataFrame(data)
        print(f"  ✅ Prepared {len(df)} hotel records")
        return df

    def prepare_impact_data(self) -> pd.DataFrame:
        """Prepare event impact data for training"""
        print("\n💰 Preparing economic impact data...")

        # Query events with impacts
        results = (
            self.db.query(Event, EventImpact, City)
            .join(EventImpact, Event.id == EventImpact.event_id)
            .join(City, Event.city_id == City.id)
            .all()
        )

        if not results:
            print("  ⚠️  No impact data found")
            return pd.DataFrame()

        # Encode event types
        event_type_map = {
            EventType.SPORTS: 1,
            EventType.MUSIC: 2,
            EventType.CULTURE: 3,
            EventType.BUSINESS: 4,
            EventType.FESTIVAL: 5,
            EventType.FAIR: 6,
            EventType.CONFERENCE: 7,
            EventType.OTHER: 0,
        }

        data = []
        for event, impact, city in results:
            duration = (event.end_date - event.start_date).days + 1

            data.append({
                'event_name': event.name,
                'attendance': event.actual_attendance or event.expected_attendance or 10000,
                'duration_days': duration,
                'event_type_encoded': event_type_map.get(event.event_type, 0),
                'city_population': city.population or 1000000,
                'city_annual_tourists': city.annual_tourists or 5000000,
                'baseline_hotel_price': city.avg_hotel_price_usd or 150,
                'total_economic_impact': impact.total_economic_impact_usd or 0,
            })

        df = pd.DataFrame(data)
        print(f"  ✅ Prepared {len(df)} event impact records")
        return df

    def train_all_models(self):
        """Train all ML models"""
        print("\n" + "=" * 60)
        print("🤖 TRAINING ML MODELS")
        print("=" * 60)

        # 1. Tourism predictor
        tourism_df = self.prepare_tourism_data()
        if len(tourism_df) > 30:  # Need enough data
            print("\n🎯 Training tourism predictor...")
            try:
                self.tourism_predictor.train(tourism_df)
                self.tourism_predictor.save_model("tourism_predictor.pkl")
            except Exception as e:
                print(f"  ❌ Error training tourism model: {e}")
        else:
            print("\n⚠️  Not enough tourism data (need > 30 records)")

        # 2. Hotel price predictor
        hotel_df = self.prepare_hotel_data()
        if len(hotel_df) > 50:
            print("\n🎯 Training hotel price predictor...")
            try:
                metrics = self.hotel_predictor.train(hotel_df)
                self.hotel_predictor.save_model("hotel_price_predictor.pkl")

                print("\n📊 Hotel Price Model Metrics:")
                for key, value in metrics.items():
                    print(f"  {key.upper()}: {value:.4f}")

                print("\n📈 Feature Importance:")
                for feature, importance in self.hotel_predictor.feature_importance().items():
                    print(f"  {feature}: {importance:.4f}")

            except Exception as e:
                print(f"  ❌ Error training hotel model: {e}")
        else:
            print("\n⚠️  Not enough hotel data (need > 50 records)")

        # 3. Economic impact predictor
        impact_df = self.prepare_impact_data()
        if len(impact_df) > 5:
            print("\n🎯 Training economic impact predictor...")
            try:
                metrics = self.impact_predictor.train(impact_df)
                self.impact_predictor.save_model("impact_predictor.pkl")

                print("\n📊 Impact Model Metrics:")
                for key, value in metrics.items():
                    print(f"  {key.upper()}: {value:.4f}")

            except Exception as e:
                print(f"  ❌ Error training impact model: {e}")
        else:
            print("\n⚠️  Not enough impact data (need > 5 records)")

    def test_predictions(self):
        """Run test predictions to verify models"""
        print("\n" + "=" * 60)
        print("🧪 TESTING PREDICTIONS")
        print("=" * 60)

        # Test tourism prediction
        if self.tourism_predictor.is_trained:
            print("\n📊 Tourism Prediction Test:")
            future = pd.DataFrame({
                'ds': pd.date_range('2025-01-01', periods=30, freq='D')
            })
            try:
                predictions = self.tourism_predictor.predict(future)
                print(f"  ✅ Predicted visitors for next 30 days")
                print(f"  Average: {predictions['yhat'].mean():.0f} visitors/day")
            except Exception as e:
                print(f"  ❌ Error: {e}")

        # Test hotel price prediction
        if self.hotel_predictor.is_trained:
            print("\n🏨 Hotel Price Prediction Test:")
            test_data = pd.DataFrame({
                'occupancy_rate': [80.0],
                'baseline_price': [150.0],
                'is_weekend': [1],
                'is_event_period': [1],
                'days_to_event': [0],
                'event_size': [50000],
            })
            try:
                price = self.hotel_predictor.predict(test_data)
                print(f"  ✅ Predicted price during event: ${price[0]:.2f}")
            except Exception as e:
                print(f"  ❌ Error: {e}")

        # Test impact prediction
        if self.impact_predictor.is_trained:
            print("\n💰 Economic Impact Prediction Test:")
            test_data = pd.DataFrame({
                'attendance': [100000],
                'duration_days': [7],
                'event_type_encoded': [1],
                'city_population': [5000000],
                'city_annual_tourists': [10000000],
                'baseline_hotel_price': [180],
            })
            try:
                impact, lower, upper = self.impact_predictor.predict_with_confidence(test_data)
                print(f"  ✅ Predicted economic impact: ${impact[0]:,.0f}")
                print(f"  Confidence interval: ${lower[0]:,.0f} - ${upper[0]:,.0f}")
            except Exception as e:
                print(f"  ❌ Error: {e}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("  🤖 EVENTLY ML TRAINING PIPELINE")
    print("  UNESCO MVP - Predictive Models")
    print("=" * 60)
    print(f"\n⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create session
    db = SessionLocal()
    trainer = ModelTrainer(db)

    try:
        # Train all models
        trainer.train_all_models()

        # Test predictions
        trainer.test_predictions()

        print("\n" + "=" * 60)
        print("✅ TRAINING COMPLETED!")
        print("=" * 60)
        print("\n📁 Models saved to: backend/app/ml/saved_models/")
        print("\n💡 Next steps:")
        print("   1. Review model metrics above")
        print("   2. Run tests: pytest backend/tests/test_ml.py")
        print("   3. Integrate predictions into API")
        print("   4. Update frontend to display predictions")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
