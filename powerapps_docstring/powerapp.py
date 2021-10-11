import os

class UnknownSourceException(Exception):
    pass

class PowerApp():
    def __init__(self, source) -> None:
        self.source = source
        self.source_type = self._check_source_type()
        
    def get_pa_src_path(self):
        source_path = None
        if self.source_type == "directory":
            # TODO: check if directory contains powerapp content
            
            if self.source[-1] != "/":
                self.source = self.source + "/"

            source_path = self.source
        elif self.source_type == "zip":
            # TODO: unzip and unpack msssap to retrieve src folder
            pass
        elif self.source_type == "mssap":
            # TODO: unpack msssap to retrieve src folder
            pass

        return source_path

    def _check_source_type(self) -> str:
        if os.path.isdir(self.source):
            return "directory"
        elif os.path.isfile(self.source) and self.source.endswith(".Zip"):
            return "zip"
        elif os.path.isfile(self.source) and self.source.endswith(".mssap"):
            return "mssap"
        else:
            raise UnknownSourceException


    def _unpack_zip(self):
        pass

    def _unpack_mssap(self):
        pass