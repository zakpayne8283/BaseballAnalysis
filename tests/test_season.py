import pytest
import os

from src.models.season import Season

# TODO: Look into a test_setup to have test_season setup for each instance?

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
    assert(test_season.hitter_data is not None)

    # Test an invalid season
    with pytest.raises(SystemExit) as e:
        test_season = Season(2099)

def test_print_data(capfd):

    test_season = Season(2024)

    test_season.print_data('raw')
    out, err = capfd.readouterr()
    assert "gid" in out

    test_season.print_data('batter')
    out, err = capfd.readouterr()
    assert "abrac001" in out
