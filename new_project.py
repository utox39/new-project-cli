#!/usr/bin/env python3

import argparse
import errno
import os
import json
import subprocess
import sys
import textwrap

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


class NewProject:
    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        self.dev_dir_check()
        self.handler()

    @staticmethod
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

    @staticmethod
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

    def create_project(self, projects_dir_name: str, project_name: str, file_name: str):
        # check if the specified projects folder exists
        self.projects_path_check(projects_dir_to_check=projects_dir_name)

        projects_path = os.path.join(DEV_DIR, projects_dir_name)
        # Creating the project folder
        new_project_dir = f"{projects_path}/{project_name}"

        try:
            os.mkdir(new_project_dir)

            if self.cli_args.python:
                # python -m venv NEW_PROJECT_DIR/venv
                console.print(
                    "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
                )
                # MacOS/Linux
                if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
                    with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                        subprocess.run(["python3", "-m", "venv", f"{new_project_dir}/venv"])
                # Windows
                if sys.platform.startswith("win32"):
                    with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                        subprocess.run(["virtualenv", f"{new_project_dir}/venv"])
                console.print("✓ Done." + "\n")

            # Creating the file structure
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            with open(f"{new_project_dir}/{file_name}", "x"):
                console.print(f"▶ [underline]{file_name}[/underline] created.")
            console.print("✓ Done." + "\n")

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
            file_name="Main.java")

    # * GO
    def create_go_project(self) -> None:
        """
        Create a go projects
        """

        self.create_project(
            projects_dir_name=GO_PROJECTS_DIR_NAME,
            project_name=self.cli_args.go,
            file_name="main.go")

    # * RUST
    def create_rust_project(self) -> None:
        """
        Create a rust project
        """
        self.projects_path_check(projects_dir_to_check=RUST_PROJECTS_DIR_NAME)

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
        self.projects_path_check(projects_dir_to_check=BASH_PROJECTS_DIR_NAME)

        bash_projects_path = os.path.join(DEV_DIR, BASH_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_bash_project_dir = f"{bash_projects_path}/{self.cli_args.bash}"
        try:
            os.mkdir(new_bash_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            with open(f"{new_bash_project_dir}/{self.cli_args.bash}.sh", "w") as main_f:
                main_f.write("#!/bin/bash")
                console.print(f"▶ [underline]{self.cli_args.bash}.sh[/underline] created.")
            subprocess.run(["chmod", "+x", f"{new_bash_project_dir}/{self.cli_args.bash}.sh"])
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_bash_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_bash_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"{new_bash_project_dir} [bold red3]already exists![/bold red3]"
            )
            sys.exit(errno.EEXIST)

    # * CPP
    def create_cpp_project(self) -> None:
        """
        Create a cpp project
        """
        self.projects_path_check(projects_dir_to_check=CPP_PROJECTS_DIR_NAME)

        cpp_projects_path = os.path.join(DEV_DIR, CPP_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_cpp_project_dir = f"{cpp_projects_path}/{self.cli_args.cpp}"
        try:
            os.mkdir(new_cpp_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            os.mkdir(f"{new_cpp_project_dir}/src")
            with open(f"{new_cpp_project_dir}/src/main.cpp", "w") as main_f:
                main_f.write(
                    textwrap.dedent(
                        """\
                    #include <iostream>

                    int main()
                    {
                        return 0;
                    }"""
                    )
                )
                console.print("▶ [underline]main.cpp[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_cpp_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_cpp_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"{new_cpp_project_dir} [bold red3]already exists![/bold red3]"
            )
            sys.exit(errno.EEXIST)

    # * C
    def create_clang_project(self) -> None:
        """
        Create a c project
        """
        self.projects_path_check(projects_dir_to_check=CLANG_PROJECTS_DIR_NAME)

        c_projects_path = os.path.join(DEV_DIR, CLANG_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_c_project_dir = f"{c_projects_path}/{self.cli_args.clang}"
        try:
            os.mkdir(new_c_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            os.mkdir(f"{new_c_project_dir}/src")
            with open(f"{new_c_project_dir}/src/main.c", "w") as main_f:
                main_f.write(
                    textwrap.dedent(
                        """\
                    #include <iostream>

                    int main()
                    {
                        return 0;
                    }"""
                    )
                )
                console.print("▶ [underline]main.c[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_c_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_c_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"{new_c_project_dir} [bold red3]already exists![/bold red3]"
            )
            sys.exit(errno.EEXIST)

    # * NON-SPECIFIC PROJECTS
    def create_non_specific_project(self) -> None:
        """
        Create a non specific project
        """
        self.projects_path_check(projects_dir_to_check=NON_SPECIFIC_PROJECTS_DIR_NAME)

        non_specific_projects_path = os.path.join(DEV_DIR, NON_SPECIFIC_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_non_specific_project_dir = f"{non_specific_projects_path}/{self.cli_args.none}"
        try:
            os.mkdir(new_non_specific_project_dir)
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_non_specific_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_non_specific_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"{new_non_specific_project_dir} [bold red3]already exists![/bold red3]"
            )
            sys.exit(errno.EEXIST)

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
    args = parser.parse_args()

    new_project = NewProject(cli_args=args)
    new_project.run()
