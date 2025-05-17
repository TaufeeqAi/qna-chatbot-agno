# common/exception.py
import sys
import traceback

class AppException(Exception):
    """Base class for application-specific errors."""
    def __init__(self, message: str, status_code: int = 500, error_detail: Exception = None):
        self.status_code = status_code
        self.error_detail = error_detail
        self.error_message = self.get_detailed_error_message(message, self.error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message, error_detail):
        _, _, exc_tb = sys.exc_info()
        if exc_tb:
            frame = exc_tb.tb_frame
            filename = frame.f_code.co_filename
            lineno = exc_tb.tb_lineno
            full_msg = f"{message} | Detail: {error_detail} | File: {filename} | Line: {lineno}"
        else:
            filename, lineno = "Unknown file name", "Unknown line number"
        
        return full_msg
    
    def __str__(self):
        return self.error_message

class ResourceNotFound(AppException):
    """Raises when a requested resource is missing."""
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", status_code=404)
