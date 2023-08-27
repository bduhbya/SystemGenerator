import os

TEST_LOG_DIR = 'UNIT_TEST_LOGS'
TEST_LOG_FILE_POSTFIX = '_log_file.txt'

def get_test_log_file_name(prefix: str):
  return os.path.join(TEST_LOG_DIR, prefix + TEST_LOG_FILE_POSTFIX)

