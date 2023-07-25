from loguru import logger

LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"

LOG_LEVELS = [
  LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR, LOG_LEVEL_INFO, LOG_LEVEL_WARNING
]


class LogTrace:

  def __init__(self, logger_name, log_file_path, log_level):
    if log_file_path is None:
      raise RuntimeError('log_file_path must be defined')

    if log_level not in LOG_LEVELS:
      raise RuntimeError(f'log_level must be in {LOG_LEVELS}')

    logger.add(
      log_file_path,
      level=log_level,
      format=
      "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}.{function}:{line} | {message}",
      rotation="10 MB",
      filter=lambda record: record["extra"].get("logger_name") == logger_name,
    )
    self.logger = logger.bind(logger_name=logger_name)

  def log(self, level, message, **kwargs):
    self.logger.opt(depth=2, exception=None,
                    lazy=False).log(level, message, **kwargs)

  def error(self, message, **kwargs):
    self.log(LOG_LEVEL_ERROR, message, **kwargs)

  def warning(self, message, **kwargs):
    self.log(LOG_LEVEL_WARNING, message, **kwargs)

  def info(self, message, **kwargs):
    self.log(LOG_LEVEL_INFO, message, **kwargs)

  def debug(self, message, **kwargs):
    self.log(LOG_LEVEL_DEBUG, message, **kwargs)

  def close(self):
    self.logger.complete()
    self.logger.remove()

#Quick local test for manual checking
if __name__ == "__main__":
  tracer = LogTrace('test_tracer', "Local_test_file.txt", LOG_LEVEL_DEBUG)
  tracer.error("An error occurred. {error_code}", error_code=123)
