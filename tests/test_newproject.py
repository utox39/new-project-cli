import errno
import os
import tempfile
import unittest

from newproject.newproject import Check


class TestCheck(unittest.TestCase):
    def test_config_file_validator(self):
        # Create a sample config file and JSON schema for testing
        config_file = {
            "key1": "value1",
            "key2": "value2"
        }
        json_schema = {
            "type": "object",
            "properties": {
                "key1": {"type": "string"},
                "key2": {"type": "string"}
            }
        }

        # Test a valid configuration
        self.assertTrue(Check.config_file_validator(config_file, json_schema))

        # Test an invalid configuration
        config_file["key2"] = 123  # Add an invalid property
        self.assertFalse(Check.config_file_validator(config_file, json_schema))

        print("----------")

    def test_dev_dir_check(self):
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test an existing directory
            self.assertTrue(Check.dev_dir_check(temp_dir))

            # Test a non-existing directory
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            self.assertFalse(Check.dev_dir_check(non_existing_dir))

            print("----------")

    def test_path_check(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            with self.assertRaises(SystemExit) as se:
                Check.projects_path_check(non_existing_dir)
            self.assertEquals(se.exception.code, errno.ENOENT)

    def test_name_check(self):
        with self.assertRaises(SystemExit) as se:
            Check.projects_path_check("invalid name")
        self.assertEquals(se.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
