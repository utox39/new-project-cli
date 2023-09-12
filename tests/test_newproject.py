import errno
import logging
import os
import site
import subprocess
import tempfile
import unittest
from shutil import which
from unittest.mock import patch, MagicMock, Mock

from newproject.newproject import Check, NewProject


class TestCheck(unittest.TestCase):
    def test_config_file_validator(self):
        # Create a sample config file and JSON schema for testing
        print("- test_config_file_validator\n")
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

        print("OK\n----------")

    def test_dev_dir_check(self):
        print("- test_dev_dir_check\n")
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test an existing directory
            self.assertTrue(Check.dev_dir_check(temp_dir))

            # Test a non-existing directory
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            self.assertFalse(Check.dev_dir_check(non_existing_dir))

            print("OK\n----------")

    def test_path_check(self):
        print("- test_path_check\n")

        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            with self.assertRaises(SystemExit) as cm:
                Check.projects_path_check(non_existing_dir)
            self.assertEqual(cm.exception.code, errno.ENOENT)

            print("OK\n----------")

    def test_name_check(self):
        print("- test_name_check\n")

        with self.assertRaises(SystemExit) as cm:
            Check.projects_path_check("invalid name")
        self.assertEqual(cm.exception.code, 2)

        print("OK\n----------")


class TestNewProject(unittest.TestCase):
    @unittest.skipIf(which("code") is None, "Do not run if code is not installed")
    @patch('shutil.which', return_value='code')
    @patch('subprocess.run')
    def test_open_in_ide_success(self, mock_run, mock_which):
        print("- test_open_in_ide_success\n")

        NewProject.open_in_ide('code', '/path/to/project')

        # Assert that code path/to/project was called
        mock_run.assert_called_once_with(['code', '/path/to/project'])

        print("OK\n----------")

    @patch('shutil.which')
    def test_open_in_ide_command_not_found(self, mock_which):
        print("- test_open_in_ide_command_not_found\n")

        with patch('builtins.print') as mock_print:
            mock_which.return_value = None

            NewProject.open_in_ide('invalid_ide', '/path/to/project')

            mock_print.assert_called_once_with('newproject: invalid_ide: ide command not found')

        print("OK\n----------")

    @patch('subprocess.run')
    @patch('shutil.which')
    def test_git_init_command_success(self, mock_which, mock_run):
        print("- test_git_init_command_success\n")
        mock_which.return_value = which("git")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            content = 'sample_content'

            NewProject().git_init_command(project_dir, content)

            # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", project_dir])

            print("OK\n----------")

    @patch('subprocess.run')
    # @patch('builtins.print')  # Mock the print function
    def test_git_init_failure(self, mock_run):
        print("- test_git_init_failure\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            content = 'sample_content'

            NewProject().git_init_command(project_dir, content)

            # # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", project_dir])

            # Assert that .gitignore was not created
            gitignore_path = os.path.join(project_dir, '.gitignore')
            self.assertFalse(os.path.exists(gitignore_path))

            print("OK\n----------")


if __name__ == '__main__':
    unittest.main()
