import os

class UnknownSourceException(Exception):
    pass

class PowerApp():
    def __init__(self, source) -> None:
        self.source = os.path.normpath(source)
        self.source_type = self._check_source_type()
        
    def get_pa_src_path(self):
        source_path = None
        if self.source_type == "directory":
            source_path = self.source
        elif self.source_type == "zip":
            # TODO: unzip and unpack msssap to retrieve src folder
            pass
        elif self.source_type == "msapp":
            # TODO: unpack msssap to retrieve src folder
            pass

        return source_path

    def _check_source_type(self) -> str:
        if os.path.isdir(self.source):
            return "directory"
        elif os.path.isfile(self.source) and self.source.endswith(".zip"):
            return "zip"
        elif os.path.isfile(self.source) and self.source.endswith(".msapp"):
            return "msapp"
        else:
            raise UnknownSourceException


    def _unpack_zip(self):
        pass

    def _unpack_mssap(self):
        pass