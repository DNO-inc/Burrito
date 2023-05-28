from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse

from burrito.utils.singleton_pattern import singleton


@singleton
class _FileManager:
    def __init__(
        self,
        base_path: str | Path,
        allowed_files: list[str],
        max_size: int | float = 100
    ) -> None:
        self.__base_path = Path(base_path)
        self.__allowed_files = allowed_files
        self.__max_size = max_size

    @property
    def base_path(self) -> Path:
        return self.__base_path

    @property
    def allowed_files(self) -> list[str]:
        return self.__allowed_files

    @property
    def max_size(self) -> int | float:
        return self.__max_size

    def push_file(self, file_data: UploadFile) -> None:
        print(file_data.filename)

    def push_files(self, file_data_list: list[bytes]) -> None:
        print(file_data_list)
#        for item in file_data_list:
#            self.push_file(item)

    def pull_file(self) -> FileResponse:
        ...

    def pull_files(self) -> list[FileResponse]:
        ...


def get_file_manager() -> _FileManager:
    return _FileManager(
        "./",
        [""]
    )
