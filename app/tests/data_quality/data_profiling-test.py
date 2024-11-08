# pytest . --html-report=test_runs/test_result.html

import pytest
import os
import glob
from ...data_quality.data_profiling import load_smaller_data_files, make_reports

# integrated test: check if the data files are loaded and report generation is working for the loaded data files.
# Uncomment to generate report
# def test_data_reporting():
#     dummy_report_direc = "test_dummy_reports"
#     make_reports(load_smaller_data_files("test_dummy_reports"), location="test_dummy_reports")
#     html_files = glob.glob(f"{dummy_report_direc}/*.html")
#     if len(html_files)>0:
#         # do clean up
#         for file in html_files:
#             os.remove(file)
#     else:
#         pytest.fail("Reports were not generated")



