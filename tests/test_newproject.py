import errno
import logging
import os
import subprocess
import tempfile
import unittest
from shutil import which
from unittest.mock import patch, MagicMock, Mock

from rich.console import Console

from newproject.newproject import Check, NewProject

console = Console()


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
            with self.assertRaises(SystemExit) as cm:
                Check.projects_path_check(non_existing_dir)
            self.assertEqual(cm.exception.code, errno.ENOENT)

            print("----------")

    def test_name_check(self):
        with self.assertRaises(SystemExit) as cm:
            Check.projects_path_check("invalid name")
        self.assertEqual(cm.exception.code, 2)

        print("----------")


class TestNewProject(unittest.TestCase):
    @patch('subprocess.run')
    @patch('shutil.which')
    def test_open_in_ide_success(self, mock_which, mock_run):
        mock_which.return_value = which("code")

        NewProject.open_in_ide('code', '/path/to/project')

        # Assert that code path/to/project was called
        mock_run.assert_called_once_with(['code', '/path/to/project'])

        print("----------")

    @patch('shutil.which')
    @patch('builtins.print')
    def test_open_in_ide_command_not_found(self, mock_print, mock_which):
        mock_which.return_value = None

        NewProject.open_in_ide('invalid_ide', '/path/to/project')

        mock_print.assert_called_once_with('newproject: invalid_ide: ide command not found')

        print("----------")

    @patch('subprocess.run')
    @patch('shutil.which')
    def test_git_init_command_success(self, mock_which, mock_run):
        mock_which.return_value = which("git")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            content = 'sample_content'

            NewProject().git_init_command(project_dir, content)

            # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", project_dir])

            print("----------")

    @patch('subprocess.run')
    # @patch('builtins.print')  # Mock the print function
    def test_git_init_failure(self, mock_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            content = 'sample_content'

            NewProject().git_init_command(project_dir, content)

            # # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", project_dir])

            # Assert that .gitignore was not created
            gitignore_path = os.path.join(project_dir, '.gitignore')
            self.assertFalse(os.path.exists(gitignore_path))

            print("----------")


if __name__ == '__main__':
    unittest.main()
