# pytest test_data_extraction.py --html-report=./report/report.html

import pytest
from ...data_processing_scripts.process_rating import extract_ratings
from ...data_processing_scripts.process_history import extract_history

def test_extract_history():
    assert extract_history("dummy_data_test/history1.csv") == "SUCCESS"

def test_extract_ratings():
    assert extract_ratings("dummy_data_test/ratings.csv") == "SUCCESS"

# Testing extract_history with incorrect date format
# def test_extract_history_date_format():
#     with pytest.raises(ValueError) as excinfo:
#         extract_history("dummy_data_test/history_wrong_date_format.csv")
#     assert "incorrect date format" in str(excinfo.value).lower()

# def test_extract_history_empty():
#         assert extract_history('dummy_data_test/empty_history.csv') == "SUCCESS"