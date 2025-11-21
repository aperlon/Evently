#!/usr/bin/env python3
"""
Train Economic Impact Model from CSV files

Usage:
    python data/scripts/train_economic_model.py

This script:
1. Reads data from data/examples/*.csv
2. Trains multiple regression models
3. Selects the best model
4. Saves the trained model to backend/app/ml/saved_models/

When you update the CSV files with real data, just run this script again.
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Now import the model (avoiding __init__.py issues)
exec(open(backend_path / "app" / "ml" / "economic_impact_model.py").read())

if __name__ == "__main__":
    main()
