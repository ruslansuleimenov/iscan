from pathlib import Path
import pytest
from iscan.scanning.scanner import LocalDirectorySource


class TestScanner:
    @pytest.mark.parametrize(
        "extension",
        [
            ".jpg",
            ".jpeg",
            ".heic",
            ".heif",
            ".dng",
            ".cr2",
            ".cr3",
            ".nef",
            ".arw",
            ".raf",
            ".HEIC",
            ".JPEG",
        ],
    )
    def test_find_images(self, tmp_path, extension):
        image_path = tmp_path / f"photo{extension}"
        image_path.touch()
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert images == [image_path]

    def test_find_images_inside_directory(self, tmp_path):
        image_path = tmp_path / "qwe" / "photo.heic"
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image_path.touch()
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert images == [image_path]

    def test_find_several_images(self, tmp_path):
        paths = [
            tmp_path / "photo.heic",
            tmp_path / "photo.jpeg",
            tmp_path / "photo.jpg",
        ]
        for path in paths:
            path.touch()
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert set(images) == set(paths)

    def test_sorted_images(self, tmp_path):
        z_path = tmp_path / "zzz.jpeg"
        z_path.touch()
        a_path = tmp_path / "aaa.jpeg"
        a_path.touch()
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert images == [a_path, z_path]

    def test_search_empty_directory(self, tmp_path):
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert images == []

    def test_nonexistent_path(self, tmp_path):
        photo_dir = tmp_path / "missing"

        with pytest.raises(FileNotFoundError):
            LocalDirectorySource(photo_dir)

    def test_file_instead_of_directory(self, tmp_path):
        photo_path = tmp_path / "photo.jpg"
        photo_path.touch()

        with pytest.raises(NotADirectoryError):
            LocalDirectorySource(photo_path)

    def test_only_photo(self, tmp_path):
        photo_path = tmp_path / "photo.jpg"
        photo_path.touch()
        notes_path = tmp_path / "notes.txt"
        notes_path.touch()
        music_path = tmp_path / "music.mp3"
        music_path.touch()
        local_directory_source = LocalDirectorySource(tmp_path)
        images = local_directory_source.find_images()
        assert images == [photo_path]
