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
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}.{function} | {message}",
            rotation="10 MB",
            filter=lambda record: record["extra"].get("logger_name") == logger_name,
        )
        self.logger = logger.bind(logger_name=logger_name)

    # TODO: update to print the correct call stack frame
    def log(self, level, message, **kwargs):
        stack = inspect.stack()
        caller_frame = stack[2].frame if len(stack) >= 3 else stack[1].frame
        module_name = caller_frame.f_globals['__name__']
        method_name = caller_frame.f_code.co_name
        self.logger.opt(depth=1).log(level, message, module=module_name, function=method_name, **kwargs)

    def error(self, message, **kwargs):
        self.log("ERROR", message, **kwargs)

    def warning(self, message, **kwargs):
        self.log("WARNING", message, **kwargs)

    def info(self, message, **kwargs):
        self.log("INFO", message, **kwargs)

    def debug(self, message, **kwargs):
        self.log("DEBUG", message, **kwargs)
