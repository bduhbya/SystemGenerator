import os

TEST_LOG_DIR = 'UNIT_TEST_LOGS'
TEST_LOG_FILE_POSTFIX = '_log_file.txt'

def get_test_log_file_name(prefix: str):
  return os.path.join(TEST_LOG_DIR, prefix + TEST_LOG_FILE_POSTFIX)


def clear_test_file(name, reason: str):
  try:
    print(f"clear_test_file for {reason}, Removing previous test file: {name}")
    os.remove(name)
  except OSError as e:
    print(f"clear_test_file for {reason}, Error deleting file  {name}: {type(e).__name__} - {str(e)}")