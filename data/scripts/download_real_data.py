"""
Download real data from public sources
Auto-downloads CSV files for Evently MVP
"""
import os
import sys
import requests
import zipfile
from pathlib import Path
from datetime import datetime

# Setup paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent
SOURCES_DIR = DATA_DIR / "sources"
SOURCES_DIR.mkdir(exist_ok=True)


class DataDownloader:
    """Downloads data from various public sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Evently-UNESCO-Research/1.0'
        })

    def download_file(self, url: str, dest_path: Path, force: bool = False):
        """Download a file from URL to destination"""
        if dest_path.exists() and not force:
            print(f"⏭️  Skipping {dest_path.name} (already exists)")
            return True

        print(f"⬇️  Downloading {dest_path.name}...")
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_bytes(response.content)

            print(f"✅ Downloaded {dest_path.name} ({len(response.content):,} bytes)")
            return True
        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")
            return False

    def extract_zip(self, zip_path: Path, extract_to: Path):
        """Extract ZIP file"""
        print(f"📦 Extracting {zip_path.name}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"✅ Extracted to {extract_to}")
            return True
        except Exception as e:
            print(f"❌ Error extracting {zip_path}: {e}")
            return False


def download_worldbank_tourism():
    """Download World Bank tourism data"""
    print("\n🌍 World Bank - Tourism Data")
    print("=" * 60)

    wb_dir = SOURCES_DIR / "worldbank"
    wb_dir.mkdir(exist_ok=True)

    downloader = DataDownloader()

    # Tourism indicators
    indicators = {
        "ST.INT.ARVL": "tourism_arrivals",  # International arrivals
        "ST.INT.RCPT.CD": "tourism_receipts",  # Tourism receipts (USD)
        "ST.INT.XPND.CD": "tourism_expenditure",  # Tourism expenditure
    }

    countries = "GBR;FRA;ESP;USA;JPN;BRA;DEU;ARE;SGP;AUS;NLD"
    date_range = "2015:2024"

    for indicator, name in indicators.items():
        url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
        params = f"?format=csv&date={date_range}&downloadformat=csv"

        dest_file = wb_dir / f"{name}.zip"
        if downloader.download_file(url + params, dest_file):
            downloader.extract_zip(dest_file, wb_dir)


def download_google_mobility():
    """Download Google COVID-19 Mobility Reports"""
    print("\n📱 Google Mobility Reports")
    print("=" * 60)

    mobility_dir = SOURCES_DIR / "google_mobility"
    mobility_dir.mkdir(exist_ok=True)

    downloader = DataDownloader()

    url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
    dest_file = mobility_dir / "global_mobility_report.csv"

    downloader.download_file(url, dest_file)


def download_eurostat_tourism():
    """Download Eurostat tourism data"""
    print("\n🇪🇺 Eurostat - Tourism Data")
    print("=" * 60)

    eurostat_dir = SOURCES_DIR / "eurostat"
    eurostat_dir.mkdir(exist_ok=True)

    downloader = DataDownloader()

    # Eurostat datasets
    datasets = {
        "tour_occ_nim": "nights_spent",  # Nights spent at accommodation
        "tour_occ_arnat": "arrivals",  # Arrivals at accommodation
        "tour_occ_cap": "capacity",  # Capacity of accommodation
    }

    base_url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

    for dataset_code, name in datasets.items():
        # Request parameters
        params = {
            "format": "TSV",  # Tab-separated (easier than SDMX)
            "lang": "EN",
            "freq": "M",  # Monthly
            "geo": "ES,FR,DE,UK,IT,NL",
        }

        # Build URL
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{base_url}/{dataset_code}?{param_str}"

        dest_file = eurostat_dir / f"{name}.tsv"
        downloader.download_file(url, dest_file)


def download_manual_instructions():
    """Print instructions for manual downloads (Kaggle, etc.)"""
    print("\n📋 Manual Download Instructions")
    print("=" * 60)

    manual_sources = {
        "London Marathon (Kaggle)": {
            "url": "https://www.kaggle.com/datasets/kevinegan/london-marathon-results",
            "instructions": [
                "1. Visit the URL above",
                "2. Click 'Download' button",
                "3. Save to: data/sources/london_marathon/",
                "   OR use Kaggle API: kaggle datasets download -d kevinegan/london-marathon-results"
            ]
        },
        "Champions League (Kaggle)": {
            "url": "https://www.kaggle.com/datasets/fardifaalam170041060/champions-league-dataset-1955-2023",
            "instructions": [
                "1. Visit the URL above",
                "2. Click 'Download' button",
                "3. Save to: data/sources/champions_league/",
                "   OR use Kaggle API: kaggle datasets download -d fardifaalam170041060/champions-league-dataset-1955-2023"
            ]
        },
        "London Marathon (Zenodo)": {
            "url": "https://zenodo.org/records/10960982",
            "instructions": [
                "1. Visit the URL above",
                "2. Download the ZIP file",
                "3. Extract to: data/sources/london_marathon/"
            ]
        }
    }

    for source, info in manual_sources.items():
        print(f"\n📦 {source}")
        print(f"   URL: {info['url']}")
        for instruction in info['instructions']:
            print(f"   {instruction}")

    print("\n💡 TIP: Install Kaggle API for automated downloads:")
    print("   pip install kaggle")
    print("   kaggle datasets download -d <dataset-id>")


def download_kaggle_with_api():
    """Download Kaggle datasets using API (if configured)"""
    print("\n🔍 Checking Kaggle API...")

    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()
        print("✅ Kaggle API authenticated")

        # London Marathon
        print("\n⬇️  Downloading London Marathon dataset...")
        marathon_dir = SOURCES_DIR / "london_marathon"
        marathon_dir.mkdir(exist_ok=True)

        api.dataset_download_files(
            "kevinegan/london-marathon-results",
            path=str(marathon_dir),
            unzip=True
        )
        print("✅ London Marathon downloaded")

        # Champions League
        print("\n⬇️  Downloading Champions League dataset...")
        ucl_dir = SOURCES_DIR / "champions_league"
        ucl_dir.mkdir(exist_ok=True)

        api.dataset_download_files(
            "fardifaalam170041060/champions-league-dataset-1955-2023",
            path=str(ucl_dir),
            unzip=True
        )
        print("✅ Champions League downloaded")

        return True

    except ImportError:
        print("⚠️  Kaggle API not installed")
        print("   Install with: pip install kaggle")
        return False
    except Exception as e:
        print(f"⚠️  Kaggle API error: {e}")
        print("   Make sure ~/.kaggle/kaggle.json is configured")
        return False


def main():
    """Main download orchestrator"""
    print("\n" + "=" * 60)
    print("  📥 EVENTLY - Real Data Downloader")
    print("  UNESCO MVP - Automated Data Collection")
    print("=" * 60)
    print(f"\n📁 Download directory: {SOURCES_DIR}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create sources directory structure
    for subdir in ["worldbank", "eurostat", "google_mobility", "london_marathon", "champions_league"]:
        (SOURCES_DIR / subdir).mkdir(exist_ok=True)

    # Download from public APIs (no auth required)
    download_worldbank_tourism()
    download_google_mobility()
    download_eurostat_tourism()

    # Try Kaggle API (if configured)
    kaggle_success = download_kaggle_with_api()

    # Show manual instructions if Kaggle API failed
    if not kaggle_success:
        download_manual_instructions()

    print("\n" + "=" * 60)
    print("✅ Download process completed!")
    print(f"📁 Data saved to: {SOURCES_DIR}")
    print("\n📋 Next steps:")
    print("   1. Review downloaded files")
    print("   2. Run import script: python data/scripts/import_csv_to_db.py")
    print("   3. Verify data in database")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
