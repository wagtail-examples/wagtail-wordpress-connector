from unittest.mock import patch

from django.test import TestCase

from wp_connector.messages import ClientExitException, ClientMessage


class TestMessages(TestCase):
    """
    Test the messages module.
    """

    @patch("sys.stdout")
    def test_client_exit_exception(self, mock_stdout):
        # test error_message
        with self.assertRaises(SystemExit) as e:
            ClientExitException().error_message("test")
            self.assertEqual(e.exception.code, 1)
            mock_stdout.write.assert_called_with("ERROR:   test\n")

    @patch("sys.stdout")
    def test_client_message(self, mock_stdout):
        # test success_message
        ClientMessage().success_message("test")
        mock_stdout.write.assert_called_with("SUCCESS: test\n")

        # test info_message
        ClientMessage().info_message("test")
        mock_stdout.write.assert_called_with("INFO:    test\n")
