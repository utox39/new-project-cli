#!/usr/bin/env python3

import argparse
import errno
import os
import json
import subprocess
import sys
import textwrap
import venv

from pathlib import Path
from typing import Final

# rich
from rich.console import Console

# rich config
console = Console()

# Config file
CONFIG_FILE: Final[str] = f"{Path.home()}/.config/new_project_cli_tool/new_project_config.json"

# Load json config file
try:
    with open(CONFIG_FILE) as config_file:
        dir_name = json.load(config_file)
except FileNotFoundError:
    print(f"Error: Json config file not found")
    sys.exit(errno.ENOENT)

# Default Development folder
DEV_DIR: Final[str] = f"{Path.home()}/{dir_name['dev_dir']}"

# Projects folder names
PY_PROJECTS_DIR_NAME: Final[str] = dir_name["py_projects_dir_name"]
JAVA_PROJECTS_DIR_NAME: Final[str] = dir_name["java_projects_dir_name"]
GO_PROJECTS_DIR_NAME: Final[str] = dir_name["go_projects_dir_name"]
BASH_PROJECTS_DIR_NAME: Final[str] = dir_name["bash_projects_dir_name"]
RUST_PROJECTS_DIR_NAME: Final[str] = dir_name["rust_projects_dir_name"]
CPP_PROJECTS_DIR_NAME: Final[str] = dir_name["cpp_projects_dir_name"]
CLANG_PROJECTS_DIR_NAME: Final[str] = dir_name["clang_projects_dir_name"]
NON_SPECIFIC_PROJECTS_DIR_NAME: Final[str] = dir_name["non_specific_projects_dir_name"]


def argparse_config():
    # argparse config
    parser = argparse.ArgumentParser(
        description="A CLI tool to create a new project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
        Examples:
        new_project --python PROJECT_NAME            #create a new python project
        new_project --java PROJECT_NAME              #create a new java project
        new_project --go PROJECT_NAME                #create a new go project
        new_project --none PROJECT_NAME              #create a new non-specific project
        new_project --code --python PROJECT_NAME     #open the new project in VSCode
        new_project --pycharm --python PROJECT_NAME  #open the new project in PyCharm
        """
        ),
    )
    parser.add_argument(
        "--python",
        type=str,
        help="create a new python project",
    )
    parser.add_argument(
        "--java",
        type=str,
        help="create a new java project",
    )
    parser.add_argument(
        "--go",
        type=str,
        help="create a new go project",
    )
    parser.add_argument(
        "--bash",
        type=str,
        help="create a new bash project",
    )
    parser.add_argument(
        "--rust",
        type=str,
        help="create a new rust project",
    )
    parser.add_argument(
        "--cpp",
        type=str,
        help="create a new cpp project",
    )
    parser.add_argument(
        "--clang",
        type=str,
        help="create a new c project",
    )
    parser.add_argument(
        "--none",
        type=str,
        help="create a non-specific project",
    )
    parser.add_argument(
        "--code",
        action="store_true",
        help="open the project in Visual Studio Code",
    )
    parser.add_argument(
        "--pycharm",
        action="store_true",
        help="open the project in PyCharm",
    )

    return parser.parse_args()


def dev_dir_check() -> None:
    """
    Check if the development folder exists
    """
    try:
        if not os.path.isdir(DEV_DIR):
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"Error: {DEV_DIR} does not exists")
        sys.exit(errno.ENOENT)


def projects_path_check(projects_dir_to_check: str) -> None:
    """
    Check if the specified programming language project folder exists
    :param projects_dir_to_check: (str) name of the programming language projects folder
    """
    projects_path = os.path.join(DEV_DIR, projects_dir_to_check)
    try:
        if not os.path.isdir(projects_path):
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"{projects_path} does not exists")
        sys.exit(errno.ENOENT)


class NewProject:
    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        dev_dir_check()
        self.handler()

    @staticmethod
    def open_in_vscode(project_dir: str) -> None:
        """
        Open the project in Visual Studio Code
        :param project_dir: (str) project directory
        """
        subprocess.run(["code", f"{project_dir}"])

    @staticmethod
    def open_in_pycharm(project_dir: str) -> None:
        """
        Open the python project in PyCharm
        :param project_dir: (str) project directory
        """
        subprocess.run(["pycharm", f"{project_dir}"])

    def git_init_command(self, project_dir: str) -> None:
        """
        Initialize a local git repository
        :param project_dir: (str) project directory
        """
        console.print(
            "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
        )
        subprocess.run(["git", "init", f"{project_dir}"])

        with open(f"{project_dir}/.gitignore", "w") as git_ignore_f:
            if self.cli_args.python:
                git_ignore_f.write(
                    textwrap.dedent(
                        """\
                    .DS_Store
                    .env
                    .vscode/
                    .idea/
                    test/
                    venv/"""
                    )
                )
            else:
                git_ignore_f.write(
                    textwrap.dedent(
                        """\
                    .DS_Store
                    .env
                    .vscode/
                    .idea/
                    test/"""
                    )
                )

            console.print("▶ [underline].gitignore[/underline] created.")

        console.print("✓ Done." + "\n")

    @staticmethod
    def create_and_write_file(new_project_dir, file_name, content):
        # Creating the file structure
        console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
        with open(f"{new_project_dir}/{file_name}", "w") as project_file:
            project_file.write(content)
            console.print(f"▶ [underline]{file_name}[/underline] created.")
        console.print("✓ Done." + "\n")

    @staticmethod
    def create_python_venv(new_project_path):
        console.print(
            "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
        )
        try:
            venv.create(f"{new_project_path}/venv")
            console.print("✓ Done." + "\n")
        except Exception as venv_exception:
            print(f"Error: {venv_exception}")
            sys.exit(1)

    def create_project(self, projects_dir_name: str, project_name: str, file_name: str = "", file_content: str = ""):
        # check if the specified projects folder exists
        projects_path_check(projects_dir_to_check=projects_dir_name)

        projects_path = os.path.join(DEV_DIR, projects_dir_name)
        # Creating the project folder
        new_project_dir = f"{projects_path}/{project_name}"

        try:
            os.mkdir(new_project_dir)

            if self.cli_args.python:
                # Generating a python venv for the project
                self.create_python_venv(new_project_path=new_project_dir)

            # Creating the file structure
            if not self.cli_args.none:
                self.create_and_write_file(new_project_dir=new_project_dir, file_name=file_name, content=file_content)

            # git init
            self.git_init_command(project_dir=new_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_project_dir)

            if self.cli_args.pycharm:
                self.open_in_pycharm(project_dir=new_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")

            # cd into the new project dir
        except FileExistsError:
            console.print(
                f"{new_project_dir} [bold red3]already exists![/bold red3]"
            )
            sys.exit(errno.EEXIST)

    # * PYTHON
    def create_python_project(self) -> None:
        """
        Creates a python project and generates a venv
        """

        self.create_project(
            projects_dir_name=PY_PROJECTS_DIR_NAME,
            project_name=self.cli_args.python,
            file_name="main.py"
        )

    # * JAVA
    def create_java_project(self) -> None:
        """
        Create a java projects
        """

        self.create_project(
            projects_dir_name=JAVA_PROJECTS_DIR_NAME,
            project_name=self.cli_args.java,
            file_name="Main.java"
        )

    # * GO
    def create_go_project(self) -> None:
        """
        Create a go projects
        """

        self.create_project(
            projects_dir_name=GO_PROJECTS_DIR_NAME,
            project_name=self.cli_args.go,
            file_name="main.go"
        )

    # * RUST
    def create_rust_project(self) -> None:
        """
        Create a rust project
        """
        projects_path_check(projects_dir_to_check=RUST_PROJECTS_DIR_NAME)

        rust_projects_path = os.path.join(DEV_DIR, RUST_PROJECTS_DIR_NAME)
        # Creating the project folder and file structure for the project
        console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
        new_rust_project_dir = f"{rust_projects_path}/{self.cli_args.rust}"
        subprocess.run(["cargo", "new", new_rust_project_dir])
        console.print("✓ Done." + "\n")

        if self.cli_args.code:
            self.open_in_vscode(project_dir=new_rust_project_dir)

        console.print("[gold1]⫸ Happy Coding![/gold1]")

    # * BASH
    def create_bash_project(self) -> None:
        """
        Create a bash project
        """

        bash_file_content: Final[str] = "#!/bin/bash"

        self.create_project(
            projects_dir_name=BASH_PROJECTS_DIR_NAME,
            project_name=self.cli_args.bash,
            file_name=f"{self.cli_args.bash}.sh",
            file_content=bash_file_content
        )

    # * CPP
    def create_cpp_project(self) -> None:
        """
        Create a cpp project
        """

        cpp_file_content: Final[str] = textwrap.dedent(
            """\
           #include <iostream>
   
           int main()
           {
               return 0;
           }"""
        )

        self.create_project(
            projects_dir_name=CPP_PROJECTS_DIR_NAME,
            project_name=self.cli_args.cpp,
            file_name=f"main.cpp",
            file_content=cpp_file_content
        )

    # * C
    def create_clang_project(self) -> None:
        """
        Create a c project
        """

        c_file_content: Final[str] = textwrap.dedent(
            """\
           #include <stdio.h>

           int main()
           {
               return 0;
           }"""
        )

        self.create_project(
            projects_dir_name=CLANG_PROJECTS_DIR_NAME,
            project_name=self.cli_args.clang,
            file_name=f"main.c",
            file_content=c_file_content
        )

    # * NON-SPECIFIC PROJECTS
    def create_non_specific_project(self) -> None:
        """
        Create a non specific project
        """

        self.create_project(
            projects_dir_name=NON_SPECIFIC_PROJECTS_DIR_NAME,
            project_name=self.cli_args.none,
        )

    def handler(self):
        if self.cli_args.python:
            self.create_python_project()
        elif self.cli_args.java:
            self.create_java_project()
        elif self.cli_args.go:
            self.create_go_project()
        elif self.cli_args.bash:
            self.create_bash_project()
        elif self.cli_args.rust:
            self.create_rust_project()
        elif self.cli_args.cpp:
            self.create_cpp_project()
        elif self.cli_args.clang:
            self.create_clang_project()
        elif self.cli_args.none:
            self.create_non_specific_project()


if __name__ == "__main__":
    args = argparse_config()

    new_project = NewProject(cli_args=args)
    new_project.run()
