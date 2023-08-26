from pathlib import Path

from fastapi import UploadFile
from fastapi.responses import FileResponse

import aiofiles

from burrito.utils.singleton_pattern import singleton
from burrito.utils.task_manager import get_task_manager


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

    async def push_file(self, file_data: UploadFile) -> None:
        path_to_file: Path = self.__base_path / file_data.filename
        async with aiofiles.open(
            path_to_file,
            mode="w"
        ) as file:
            await file_data.read()
            await file.write("123")

    async def push_files(self, file_data_list: list[UploadFile]) -> None:
        get_task_manager().add_multiply_task(
            [self.push_file(item) for item in file_data_list]
        )

    async def pull_file(self) -> FileResponse:
        ...

    async def pull_files(self) -> list[FileResponse]:
        ...


def get_file_manager() -> _FileManager:
    return _FileManager(
        "storage/",
        [""]
    )
