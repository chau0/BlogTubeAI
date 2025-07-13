import os
import sys
import types
from datetime import datetime, timedelta
import asyncio

import pytest

# Provide a minimal aiofiles implementation if not installed
if 'aiofiles' not in sys.modules:
    class _AsyncFile:
        def __init__(self, path, mode='r', encoding=None):
            self._file = open(path, mode, encoding=encoding)
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            self._file.close()
        async def write(self, data):
            self._file.write(data)
        async def read(self):
            return self._file.read()
    aiofiles_mock = types.SimpleNamespace(open=lambda path, mode='r', encoding=None: _AsyncFile(path, mode, encoding))
    sys.modules['aiofiles'] = aiofiles_mock

from backend.src.core.file_manager import FileManager


def test_save_transcript_and_read_file(tmp_path):
    fm = FileManager()
    fm.transcript_dir = tmp_path
    path = asyncio.run(fm.save_transcript("job1", "hello"))
    assert os.path.exists(path)
    content = asyncio.run(fm.read_file(path))
    assert content == "hello"


def test_save_blog_output(tmp_path):
    fm = FileManager()
    fm.base_output_dir = tmp_path
    path = asyncio.run(fm.save_blog_output("job2", "blog"))
    assert os.path.exists(path)
    content = asyncio.run(fm.read_file(path))
    assert content == "blog"


def test_delete_file(tmp_path):
    p = tmp_path / "todelete.txt"
    p.write_text("data")

    fm = FileManager()
    result = asyncio.run(fm.delete_file(str(p)))
    assert result is True
    assert not p.exists()


def test_delete_missing_file(tmp_path):
    fm = FileManager()
    result = asyncio.run(fm.delete_file(str(tmp_path / "missing.txt")))
    assert result is False


def test_get_file_info(tmp_path):
    p = tmp_path / "info.txt"
    data = "text"
    p.write_text(data)

    fm = FileManager()
    info = asyncio.run(fm.get_file_info(str(p)))

    assert info is not None
    assert info["size"] == len(data)
    assert info["exists"] is True


def test_cleanup_temp_files(tmp_path):
    fm = FileManager()
    fm.temp_dir = tmp_path

    old = tmp_path / "old.tmp"
    old.write_text("x")
    past = datetime.now() - timedelta(hours=25)
    os.utime(old, (past.timestamp(), past.timestamp()))

    new = tmp_path / "new.tmp"
    new.write_text("y")

    cleaned = fm.cleanup_temp_files()
    assert cleaned == 1
    assert not old.exists()
    assert new.exists()
