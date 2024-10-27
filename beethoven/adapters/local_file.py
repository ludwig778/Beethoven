"""
from hartware_lib.adapters.directory import DirectoryAdapter


class LocalFileAdapter(DirectoryAdapter):
    def _format_filename(self, name: str) -> str:
        return f"{name}.json"

    def exists(self, name: str) -> bool:
        return self.file_exists(self._format_filename(name))

    def delete(self, name: str) -> None:
        return self.delete_file(self._format_filename(name))

    def read(self, name: str) -> dict:
        return self.read_json_file(self._format_filename(name))

    def save(self, name: str, data: dict) -> None:
        self.save_json_file(self._format_filename(name), data)
"""
