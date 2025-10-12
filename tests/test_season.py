import pytest
import os

from src.models.season import Season

def test_create_object_simple():
    CSV_ROOT = 'data/'

    test_season = Season(2024, skip_setup=True)

    assert(test_season.year_id == 2024)
    assert(test_season.csv_path == os.path.join(CSV_ROOT, f"2024plays.csv"))

def test_create_object_full():
    CSV_ROOT = 'data/'

    # Test a valid season
    test_season = Season(2024)
    assert(test_season.csv_data_raw is not None)

    # Test an invalid season
    with pytest.raises(SystemExit) as e:
        test_season = Season(2099)