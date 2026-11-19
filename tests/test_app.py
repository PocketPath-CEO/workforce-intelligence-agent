import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import app

class WorkforceAgentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_file = app.DATA_FILE
        app.DATA_FILE = Path(self.temp_dir.name) / "requests.json"

    def tearDown(self):
        app.DATA_FILE = self.original_file
        self.temp_dir.cleanup()

    def test_save_and_load(self):
        sample = [{"request_id": 1, "employee": "John", "status": "Pending"}]
        app.save_requests(sample)
        self.assertEqual(app.load_requests(), sample)

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(app.load_requests(), [])

    @patch("builtins.input", side_effect=["E001", "2", "Personal"])
    def test_valid_request_is_added(self, mocked_input):
        requests = []
        with patch("builtins.print"):
            app.submit_leave_request(requests)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0]["leave_days"], 2)
        self.assertEqual(requests[0]["status"], "Pending")

    @patch("builtins.input", side_effect=["E001", "zero"])
    def test_non_numeric_days_are_rejected(self, mocked_input):
        requests = []
        with patch("builtins.print"):
            app.submit_leave_request(requests)
        self.assertEqual(requests, [])

if __name__ == "__main__":
    unittest.main()
