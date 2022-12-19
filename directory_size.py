import os


class DirectorySize:
    def __init__(self, dir_path: str):
        self.size: int = self._get_size(dir_path)
        self._lenght: int = len(str(self.size))

    def _get_size(self, dir_path: str) -> int:
        size = 0
        for file in os.scandir(dir_path):
            size += os.path.getsize(file)
        return size

    def __format__(self, format: str):
        if format == "size_unit":
            if self._lenght >= 9:
                size = round(self.size/(1024**3), 2)
                return f"{size} GB"

            elif self._lenght >= 6:
                size = round(self.size/(1024**2), 2)
                return f"{size} MB"

            elif self._lenght >= 3:
                size = round(self.size/1024, 2)
                return f"{size} KB"

        elif format == "KB":
            return str(round(self.size/1024, 2))

        elif format == "MB":
            return str(round(self.size/(1024**2), 2))

        elif format == "GB":
            return str(round(self.size/(1024**3), 2))

        return str(self.size)


"""fs = FileSize("./photos")
print(f"{fs:size_unit}")

print(f"{fs:GB}")
print(f"{fs:MB}")
print(f"{fs:KB}")
print(f"{fs:}")

print(fs.size)
"""
