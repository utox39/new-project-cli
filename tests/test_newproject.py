import errno
import os
import tempfile
import unittest
from shutil import which
from unittest.mock import patch, mock_open

from newproject.newproject import Check, NewProject

OK: str = "OK\n----------"
path_to_project: str = '/path/to/project'


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

        print(OK)

    def test_dev_dir_check(self):
        print("- test_dev_dir_check\n")
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test an existing directory
            self.assertTrue(Check.dev_dir_check(temp_dir))

            # Test a non-existing directory
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            self.assertFalse(Check.dev_dir_check(non_existing_dir))

            print(OK)

    def test_path_check(self):
        print("- test_path_check\n")

        # Test a non-existing directory
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            with self.assertRaises(SystemExit) as cm:
                Check.projects_path_check(non_existing_dir)
            self.assertEqual(cm.exception.code, errno.ENOENT)

            print(OK)

    def test_name_check(self):
        print("- test_name_check\n")

        # Test an invalid project name
        with self.assertRaises(SystemExit) as cm:
            Check.projects_path_check("invalid name")
        self.assertEqual(cm.exception.code, 2)

        print(OK)


class TestNewProject(unittest.TestCase):
    @unittest.skipIf(which("code") is None, "Do not run if code is not installed")
    @patch('shutil.which', return_value='code')
    @patch('subprocess.run')
    def test_open_in_ide_success(self, mock_run, mock_which):
        print("- test_open_in_ide_success\n")

        NewProject.open_in_ide('code', path_to_project)

        # Assert that code path/to/project was called
        mock_run.assert_called_once_with(['code', path_to_project])

        print(OK)

    @patch('shutil.which')
    def test_open_in_ide_command_not_found(self, mock_which):
        print("- test_open_in_ide_command_not_found\n")

        with patch('builtins.print') as mock_print:
            mock_which.return_value = None

            NewProject.open_in_ide('invalid_ide', path_to_project)

            mock_print.assert_called_once_with('newproject: invalid_ide: ide command not found')

        print(OK)

    @patch('subprocess.run')
    @patch('shutil.which')
    def test_git_init_command_success(self, mock_which, mock_run):
        print("- test_git_init_command_success\n")
        mock_which.return_value = which("git")

        with tempfile.TemporaryDirectory() as temp_dir:
            content = 'sample_content'

            NewProject().git_init_command(temp_dir, content)

            # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", temp_dir])

        print(OK)

    @patch('subprocess.run', side_effect=Exception("Test Exception"))
    @patch('logging.error')
    def test_git_init_command_failure(self, mock_run, mock_logging_error):
        print("- test_git_init_command_failure\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            content = 'sample_content'

            try:
                NewProject().git_init_command(project_dir, content)
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

            # Assert that .gitignore was not created
            gitignore_path = os.path.join(project_dir, '.gitignore')
            self.assertFalse(os.path.exists(gitignore_path))

        print(OK)

    @patch('builtins.open', new_callable=mock_open)
    def test_create_and_write_file_success(self, mock_file_open):
        print("- test_create_and_write_file\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            file_name = 'test.txt'
            content = 'This is a test content.'

            NewProject.create_and_write_file(new_project_dir=project_dir, file_name=file_name, content=content)

            # Check if the file opened correctly
            mock_file_open.assert_called_once_with(f"{project_dir}/{file_name}", "w")

            # Check if the contents were written to the file
            mock_file_open().write.assert_called_once_with(content)

        print(OK)

    @patch('builtins.open', side_effect=Exception("Test Exception"))
    @patch('logging.error')
    def test_create_and_write_file_failure(self, mock_logging_error, mock_file_open):
        print("- test_create_and_write_file_exception\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            file_name = 'test.txt'
            content = 'This is a test content.'

            try:
                NewProject.create_and_write_file(new_project_dir=project_dir, file_name=file_name, content=content)
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)

    @patch('subprocess.run')
    def test_create_python_venv_success(self, mock_run):
        print("- test_create_venv_success")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            NewProject.create_python_venv(new_project_path=project_dir)
            # Assert that 'python3 -m venv f"{project_dir}/venv"' was called
            mock_run.assert_called_once_with(["python3", "-m", "venv", f"{project_dir}/venv"])

        print(OK)

    @patch('subprocess.run', side_effect=Exception("Test Exception"))
    @patch('logging.error')
    def test_create_python_venv_failure(self, mock_logging_error, mock_run, ):
        print("- test_create_venv_failure")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, 'test_project')
            try:
                NewProject.create_python_venv(new_project_path=project_dir)
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)

    def test_create_readme_success(self):
        print("- test_create_readme_success")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = 'test_project'
            content = f"# {project_name}"

            NewProject.create_readme(new_project_dir=temp_dir, project_name=project_name)

            readme_path = os.path.join(temp_dir, "README.md")
            self.assertTrue(os.path.exists(readme_path))

            # Check if the contents were written to the file
            with open(readme_path, "r") as readme_file:
                readme_content = readme_file.read()
                self.assertIn(content, readme_content)

        print(OK)

    @patch('builtins.open', side_effect=Exception("Test Exception"))
    @patch('logging.error')
    def test_create_readme_failure(self, mock_logging_error, mock_file_open):
        print("- test_create_readme_failure")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = 'test_project'
            try:
                NewProject.create_readme(new_project_dir=temp_dir, project_name=project_name)
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)


if __name__ == '__main__':
    unittest.main()
