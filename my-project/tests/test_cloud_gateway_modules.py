from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cloud_gateway_app.routing import Upstream, choose_upstream, normalize_mount_prefix, rewrite_location
from cloud_gateway_app.visitors import IPVisitorCounter


class CloudGatewayModuleTests(unittest.TestCase):
    def test_normalize_mount_prefix_handles_root(self) -> None:
        self.assertEqual(normalize_mount_prefix("/"), "")
        self.assertEqual(normalize_mount_prefix("cloud-drive"), "/cloud-drive")

    def test_choose_upstream_routes_drive_requests(self) -> None:
        ai_upstream = Upstream("127.0.0.1", 3210, "")
        drive_upstream = Upstream("127.0.0.1", 8787, "/cloud-drive")

        upstream, stripped = choose_upstream("/cloud-drive/files/demo.txt", ai_upstream, drive_upstream)

        self.assertEqual(upstream, drive_upstream)
        self.assertEqual(stripped, "/files/demo.txt")

    def test_rewrite_location_keeps_mount_prefix(self) -> None:
        upstream = Upstream("127.0.0.1", 8787, "/cloud-drive")

        rewritten = rewrite_location("http://127.0.0.1:8787/login", upstream)

        self.assertEqual(rewritten, "/cloud-drive/login")

    def test_visitor_counter_deduplicates_and_persists(self) -> None:
        with TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / ".visitor_ips"
            counter = IPVisitorCounter(data_file)

            self.assertEqual(counter.record_visitor("10.0.0.1:1234"), 1)
            self.assertEqual(counter.record_visitor("10.0.0.1"), 1)

            restored = IPVisitorCounter(data_file)
            self.assertEqual(restored.get_count(), 1)


if __name__ == "__main__":
    unittest.main()
