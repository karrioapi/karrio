from unittest import TestCase
from unittest.mock import patch

from karrio.server.core import utils


class TestAsyncDbCleanup(TestCase):
    def test_run_async_cleans_up_db_connections_on_success(self):
        with patch("karrio.server.core.utils.close_old_connections") as close_old, patch.object(
            utils.connections, "close_all"
        ) as close_all:
            result = utils.run_async(lambda: "ok").result(timeout=2)

        self.assertEqual(result, "ok")
        close_old.assert_called_once_with()
        close_all.assert_called_once_with()

    def test_run_async_cleans_up_db_connections_on_error(self):
        with patch("karrio.server.core.utils.close_old_connections") as close_old, patch.object(
            utils.connections, "close_all"
        ) as close_all:
            future = utils.run_async(lambda: (_ for _ in ()).throw(ValueError("boom")))

            with self.assertRaises(ValueError):
                future.result(timeout=2)

        close_old.assert_called_once_with()
        close_all.assert_called_once_with()