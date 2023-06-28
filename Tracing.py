import inspect
from loguru import logger

LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"

class LogTrace:
    def __init__(self, logger_name, log_file_path, log_level):
        logger.add(
            log_file_path,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}.{function}:{line} | {message}",
            rotation="10 MB",
            filter=lambda record: record["extra"].get("logger_name") == logger_name,
        )
        self.logger = logger.bind(logger_name=logger_name)

    def log(self, level, message, **kwargs):
        self.logger.opt(depth=2, exception=None, lazy=False).log(level, message, **kwargs)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)

    def warning(self, message, **kwargs):
        self.log("WARNING", message, **kwargs)

    def info(self, message, **kwargs):
        self.log("INFO", message, **kwargs)

    def debug(self, message, **kwargs):
        self.log("DEBUG", message, **kwargs)

#Quick local test for manual checking
if __name__ == "__main__":
    tracer = LogTrace('test_tracer', "Local_test_file.txt", LOG_LEVEL_DEBUG)
    tracer.error("An error occurred. {error_code}", error_code=123)