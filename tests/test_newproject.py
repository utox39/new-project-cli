import errno
import io
import os
import tempfile
import unittest
from shutil import which
from typing import Final
from unittest.mock import patch, mock_open

import pytest

import newproject.check
import newproject.error_codes
import newproject.error_logger
from newproject.newproject import NewProject
from newproject.utils import get_config_path, select_config_file
from newproject.error_logger import log_error

OK: str = "OK\n----------"
PATH_TO_PROJECT: str = "/path/to/project"

EXIT_FAILURE: Final[int] = 1


class TestCheck(unittest.TestCase):
    def test_config_file_validator(self):
        # Create a sample config file and JSON schema for testing
        print("- test_config_file_validator\n")
        config_file = {"key1": "value1", "key2": "value2"}
        json_schema = {
            "type": "object",
            "properties": {"key1": {"type": "string"}, "key2": {"type": "string"}},
        }

        # Test a valid configuration
        self.assertTrue(newproject.check.config_file_validator(config_file, json_schema))

        # Test an invalid configuration
        config_file["key2"] = 123  # Add an invalid property
        with self.assertRaises(SystemExit) as e:
            newproject.check.config_file_validator(config_file, json_schema)

        self.assertEqual(e.exception.code, EXIT_FAILURE)

        print(OK)

    def test_dev_dir_check(self):
        print("- test_dev_dir_check\n")
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test an existing directory
            self.assertTrue(newproject.check.dev_dir_check(temp_dir))

            # Test a non-existing directory
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            assert newproject.check.dev_dir_check(non_existing_dir) is None

            print(OK)

    def test_path_check(self):
        print("- test_path_check\n")

        # Test a non-existing directory
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existing_dir = os.path.join(temp_dir, "non_existing")
            with self.assertRaises(SystemExit) as e:
                newproject.check.projects_path_check(non_existing_dir)
            self.assertEqual(e.exception.code, errno.ENOENT)

            print(OK)

    def test_project_name_check(self):
        print("- test_name_check\n")

        # Test an invalid project name
        with self.assertRaises(SystemExit) as e:
            newproject.check.project_name_check("invalid name")
        self.assertEqual(e.exception.code, EXIT_FAILURE)

        print(OK)


class TestUtils:
    def test_get_config_path(self):
        assert get_config_path() is not None

    def test_select_config_path(self):
        assert select_config_file() is not None


class TestErrorLogger:
    def test_log_error(self, capfd):
        error_codes = [
            newproject.error_codes.DEVELOPMENT_DIR_NOT_FOUND_ERROR,
            newproject.error_codes.PROJECTS_FOLDER_NOT_FOUND_ERROR,
            newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR,
            newproject.error_codes.INVALID_PROJECT_NAME,
            newproject.error_codes.YAML_CONFIG_FILE_NOT_FOUND_ERROR,
            newproject.error_codes.YAML_CONFIG_FILE_GENERIC_ERROR,
            newproject.error_codes.JSON_SCHEMA_FILE_NOT_FOUND_ERROR,
            newproject.error_codes.PYTHON_VENV_ERROR,
            newproject.error_codes.README_ERROR,
            newproject.error_codes.COMMAND_ERROR,
            newproject.error_codes.COMMAND_NOT_FOUND_ERROR,
            newproject.error_codes.GITIGNORE_ERROR,
            newproject.error_codes.GIT_ERROR,
            newproject.error_codes.GIT_NOT_INSTALLED,
            newproject.error_codes.IDE_NOT_FOUND_ERROR,
            newproject.error_codes.CREATE_OR_WRITE_ERROR
        ]

        for error in error_codes:
            match error:
                case newproject.error_codes.DEVELOPMENT_DIR_NOT_FOUND_ERROR | \
                     newproject.error_codes.PROJECTS_FOLDER_NOT_FOUND_ERROR:
                    log_error(error_code=error, folder="not_existent")
                    out, _ = capfd.readouterr()
                    assert out is not None
                case newproject.error_codes.PROJECT_ALREADY_EXISTS_ERROR:
                    already_existent_project = "project_name"
                    log_error(error_code=error, already_existent_project=already_existent_project)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: {already_existent_project} already exists.\n𝙓 Could not create the project\n"
                    assert out in expected_output
                case newproject.error_codes.INVALID_PROJECT_NAME:
                    invalid_characters = ["spaces", "&&", "||"]
                    for char in invalid_characters:
                        log_error(error_code=error, invalid_character=char)
                        out, _ = capfd.readouterr()
                        expected_output = f"newproject: error: invalid project name. Invalid character: {char}\n"
                        assert out in expected_output
                case newproject.error_codes.YAML_CONFIG_FILE_NOT_FOUND_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: yaml config file not found.\n"
                    assert out in expected_output
                case newproject.error_codes.YAML_CONFIG_FILE_GENERIC_ERROR:
                    yaml_error = "test"
                    log_error(error_code=error, yaml_error=yaml_error)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: yaml config file error: {yaml_error}\n"
                    assert out in expected_output
                case newproject.error_codes.JSON_SCHEMA_FILE_NOT_FOUND_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: json schema file not found.\n"
                    assert out in expected_output
                case newproject.error_codes.PYTHON_VENV_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: can't create python venv.\n"
                    assert out in expected_output
                case newproject.error_codes.README_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: can't create README.md file.\n"
                    assert out in expected_output
                case newproject.error_codes.COMMAND_ERROR:
                    unsuccessful_command = "test_command"
                    log_error(error_code=error, unsuccessful_command=unsuccessful_command)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: {unsuccessful_command} generated an error.\n𝙓 Could not create the project\n"
                    assert out in expected_output
                case newproject.error_codes.COMMAND_NOT_FOUND_ERROR:
                    unsuccessful_command = "test_command"
                    log_error(error_code=error, unsuccessful_command=unsuccessful_command)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: {unsuccessful_command}: command not found.\n"
                    assert out in expected_output
                case newproject.error_codes.GITIGNORE_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: can't create .gitignore file.\n"
                    assert out in expected_output
                case newproject.error_codes.GIT_ERROR:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: can't initialize git repository.\n"
                    assert out in expected_output
                case newproject.error_codes.GIT_NOT_INSTALLED:
                    log_error(error_code=error)
                    out, _ = capfd.readouterr()
                    expected_output = "newproject: error: git is not installed.\n"
                    assert out in expected_output
                case newproject.error_codes.IDE_NOT_FOUND_ERROR:
                    ide_command = "test_ide"
                    log_error(error_code=error, ide_command=ide_command)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: {ide_command}: ide command not found.\n"
                    assert out in expected_output
                case newproject.error_codes.CREATE_OR_WRITE_ERROR:
                    not_writable_file = "test_file"
                    log_error(error_code=error, not_writable_file=not_writable_file)
                    out, _ = capfd.readouterr()
                    expected_output = f"newproject: error: can't create or write {not_writable_file}\n"
                    assert out in expected_output


class TestNewProject(unittest.TestCase):
    @unittest.skipIf(which("code") is None, "Do not run if code is not installed.")
    @patch("shutil.which", return_value="code")
    @patch("subprocess.run")
    def test_open_in_ide_success(self, mock_run, mock_which):
        print("- test_open_in_ide_success\n")

        NewProject.open_in_ide("code", PATH_TO_PROJECT)

        # Assert that code path/to/project was called
        mock_run.assert_called_once_with(["code", PATH_TO_PROJECT])

        print(OK)

    @pytest.mark.usefixtures("capfd")
    @patch("shutil.which")
    def test_open_in_ide_command_not_found(self, mock_which):
        print("- test_open_in_ide_command_not_found\n")

        mock_which.return_value = None

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            NewProject.open_in_ide("invalid_ide", PATH_TO_PROJECT)
            out = mock_stdout.getvalue()

        expected_output = "newproject: error: invalid_ide: ide command not found.\n"
        self.assertIn(expected_output, out)

        print("OK")

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_git_init_command_success(self, mock_which, mock_run):
        print("- test_git_init_command_success\n")
        mock_which.return_value = which("git")

        with tempfile.TemporaryDirectory() as temp_dir:
            content = "sample_content"

            NewProject().git_init_command(temp_dir, content)

            # Get the file size of .gitignore
            check_gitignore = os.path.getsize(os.path.join(temp_dir, ".gitignore"))

            if check_gitignore == 0:
                is_empty = True
            else:
                is_empty = False

            # Assert that the .gitignore is not empty
            self.assertFalse(is_empty)

            # Assert that git init was called
            mock_run.assert_called_once_with(["git", "init", temp_dir])

        print(OK)

    @patch("subprocess.run", side_effect=Exception("Test Exception"))
    @patch("logging.error")
    def test_git_init_command_failure(self, mock_run, mock_logging_error):
        print("- test_git_init_command_failure\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, "test_project")
            content = "sample_content"

            try:
                NewProject().git_init_command(project_dir, content)
            except Exception as e:
                # Assert that logging.error printed the subprocess error
                mock_logging_error.assert_called_once_with(str(e))

            # Assert that .gitignore was not created
            gitignore_path = os.path.join(project_dir, ".gitignore")
            self.assertFalse(os.path.exists(gitignore_path))

        print(OK)

    @patch("builtins.open", new_callable=mock_open)
    def test_create_and_write_file_success(self, mock_file_open):
        print("- test_create_and_write_file\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, "test_project")
            file_name = "test.txt"
            content = "This is a test content."

            NewProject.create_and_write_file(
                new_project_dir=project_dir, file_name=file_name, content=content
            )

            # Check if the file opened correctly
            mock_file_open.assert_called_once_with(f"{project_dir}/{file_name}", "w")

            # Check if the contents were written to the file
            mock_file_open().write.assert_called_once_with(content)

        print(OK)

    @patch("builtins.open", side_effect=Exception("Test Exception"))
    @patch("logging.error")
    def test_create_and_write_file_failure(self, mock_logging_error, mock_file_open):
        print("- test_create_and_write_file_exception\n")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, "test_project")
            file_name = "test.txt"
            content = "This is a test content."

            try:
                NewProject.create_and_write_file(
                    new_project_dir=project_dir, file_name=file_name, content=content
                )
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)

    @patch("subprocess.run")
    def test_create_python_venv_success(self, mock_run):
        print("- test_create_venv_success")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, "test_project")
            NewProject.create_python_venv(new_project_path=project_dir)
            # Assert that 'python3 -m venv f"{project_dir}/venv"' was called
            mock_run.assert_called_once_with(
                ["python3", "-m", "venv", f"{project_dir}/venv"]
            )

        print(OK)

    @patch("subprocess.run", side_effect=Exception("Test Exception"))
    @patch("logging.error")
    def test_create_python_venv_failure(
            self,
            mock_logging_error,
            mock_run,
    ):
        print("- test_create_venv_failure")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = os.path.join(temp_dir, "test_project")
            try:
                NewProject.create_python_venv(new_project_path=project_dir)
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)

    def test_create_readme_success(self):
        print("- test_create_readme_success")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test_project"
            content = f"# {project_name}"

            NewProject.create_readme(
                new_project_dir=temp_dir, project_name=project_name
            )

            readme_path = os.path.join(temp_dir, "README.md")
            self.assertTrue(os.path.exists(readme_path))

            # Check if the contents were written to the file
            with open(readme_path, "r") as readme_file:
                readme_content = readme_file.read()
                self.assertIn(content, readme_content)

        print(OK)

    @patch("builtins.open", side_effect=Exception("Test Exception"))
    @patch("logging.error")
    def test_create_readme_failure(self, mock_logging_error, mock_file_open):
        print("- test_create_readme_failure")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test_project"
            try:
                NewProject.create_readme(
                    new_project_dir=temp_dir, project_name=project_name
                )
            except Exception as e:
                # Assert that logging.error printed the error
                mock_logging_error.assert_called_once_with(str(e))

        print(OK)


if __name__ == "__main__":
    unittest.main()
