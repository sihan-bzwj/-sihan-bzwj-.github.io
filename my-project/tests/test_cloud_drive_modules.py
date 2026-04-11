from __future__ import annotations

import unittest
from io import BytesIO
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

from cloud_drive_app.config import CloudDriveConfig
from cloud_drive_app.service import delete_entry, list_directory_payload, store_uploads
from cloud_drive_app.storage import make_unique_path, resolve_inside_root
from cloud_drive_app.uploads import UploadedFile
from cloud_drive_server import CloudDriveHandler


class CloudDriveModuleTests(unittest.TestCase):
    def test_resolve_inside_root_blocks_traversal(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with self.assertRaises(ValueError):
                resolve_inside_root(root, "../escape.txt")

    def test_make_unique_path_appends_number_suffix(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            original = root / "notes.txt"
            original.write_text("first", encoding="utf-8")

            unique_path = make_unique_path(original)

            self.assertEqual(unique_path.name, "notes (1).txt")

    def test_store_uploads_avoids_overwriting_existing_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "report.txt").write_text("existing", encoding="utf-8")

            uploaded = store_uploads(
                root,
                "",
                [UploadedFile(filename="report.txt", file=BytesIO(b"new report"))],
            )

            self.assertEqual(uploaded[0]["name"], "report (1).txt")
            self.assertEqual((root / "report.txt").read_text(encoding="utf-8"), "existing")
            self.assertEqual((root / "report (1).txt").read_bytes(), b"new report")

    def test_list_directory_payload_puts_directories_first(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "folder").mkdir()
            (root / "folder" / "child.txt").write_text("child", encoding="utf-8")
            (root / "file.txt").write_text("file", encoding="utf-8")

            payload = list_directory_payload(root, "")

            self.assertEqual([entry["name"] for entry in payload["entries"]], ["folder", "file.txt"])

    def test_delete_entry_rejects_storage_root(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with self.assertRaises(ValueError):
                delete_entry(root, "")

    def test_head_root_returns_ok(self) -> None:
        with TemporaryDirectory() as temp_dir:
            server = ThreadingHTTPServer(("127.0.0.1", 0), CloudDriveHandler)
            server.config = CloudDriveConfig(root=Path(temp_dir), upload_password="testpass")
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()

            try:
                connection = HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
                connection.request("HEAD", "/")
                response = connection.getresponse()

                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader("Content-Type"), "text/html; charset=utf-8")
                self.assertIsNotNone(response.getheader("Content-Length"))
            finally:
                connection.close()
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
