import unittest
from unittest.mock import MagicMock, patch
import logging
from service.common.log_handlers import init_logging

class TestLogHandlers(unittest.TestCase):
    """Test cases for the init_logging function."""

    def setUp(self):
        """Set up a mock app object for testing."""
        self.app = MagicMock()
        self.app.logger = MagicMock()

    def test_logging_setup_success(self):
        """Test successful setup of logging handlers and level."""
        logger_name = "gunicorn.error"
        gunicorn_logger = logging.getLogger(logger_name)
        with patch("logging.getLogger", return_value=gunicorn_logger):
            init_logging(self.app, logger_name)
            self.assertEqual(self.app.logger.handlers, gunicorn_logger.handlers)
            self.assertEqual(self.app.logger.setLevel.call_args[0][0], gunicorn_logger.level)

    def test_invalid_logger_name(self):
        """Test behavior when an invalid logger name is provided."""
        invalid_logger_name = "invalid_logger"

        with patch("logging.getLogger") as mock_get_logger:
            mock_get_logger.side_effect = Exception("Logger not found")
            with self.assertRaises(Exception):
                init_logging(self.app, invalid_logger_name)

    def test_invalid_app_object(self):
        """Test behavior when an invalid app object is passed."""
        invalid_app = None

        with self.assertRaises(AttributeError):
            init_logging(invalid_app, "gunicorn.error")
