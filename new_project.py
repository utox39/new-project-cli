#!/usr/bin/env python3

import argparse
import os
import json
import sys
import subprocess
import sys
import textwrap

from pathlib import Path
from typing import Final

# rich
from rich.console import Console

# rich config
console = Console()

# Default Development folder
DEV_DIR = f"{Path.home()}/Developer/projects/"

# Projects folder names
PY_PROJECTS_DIR_NAME: Final = "python_projects"
JAVA_PROJECTS_DIR_NAME: Final = "java_projects"
GO_PROJECTS_DIR_NAME: Final = "go_projects"
BASH_PROJECTS_DIR_NAME: Final = "bash_projects"
RUST_PROJECTS_DIR_NAME: Final = "rust_projects"
CPP_PROJECTS_DIR_NAME: Final = "cpp_projects"
NON_SPECIFIC_PROJECTS_DIR_NAME: Final = "non_specific_projects"


class NewProject:
    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        self.handler()

    @staticmethod
    def dev_dir_check() -> None:
        if not os.path.isdir(DEV_DIR):
            choice = input("This directory doesn't exists!\nDo you want to create it? [Y/n]: ").lower()
            if choice == "y":
                os.mkdir(DEV_DIR)
                console.print(f"{DEV_DIR} dir [underline]created.[/underline]")
            else:
                sys.exit()

    def projects_path_check(self, projects_dir_name: str) -> None:
        """
        Check if the parsed programming language projects folder exists
        :param projects_dir_name: (str) name of the programming language projects folder
        """
        self.dev_dir_check()
        projects_path = os.path.join(DEV_DIR, projects_dir_name)
        if not os.path.isdir(projects_path):
            os.mkdir(projects_path)
            console.print(f"{projects_dir_name} dir [underline]created.[/underline]")

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
                    .env
                    .vscode/
                    .idea/
                    test/"""
                    )
                )

            console.print("▶ [underline].gitignore[/underline] created.")

        console.print("✓ Done." + "\n")

    # * PYTHON
    def create_python_project(self) -> None:
        """
        Creates a python project and generates a venv
        """
        self.projects_path_check(projects_dir_name=PY_PROJECTS_DIR_NAME)

        py_projects_path = os.path.join(DEV_DIR, PY_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_py_project_dir = f"{py_projects_path}/{self.cli_args.python}"
        try:
            os.mkdir(new_py_project_dir)

            # python -m venv NEW_PROJECT_DIR/venv
            console.print(
                "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
            )
            # MacOS/Linux
            if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    subprocess.run(["python3", "-m", "venv", f"{new_py_project_dir}/venv"])
            # Windows
            if sys.platform.startswith("win32"):
                with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                    subprocess.run(["virtualenv", f"{new_py_project_dir}/venv"])
            console.print("✓ Done." + "\n")

            # Creating the file structure
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            with open(f"{new_py_project_dir}/main.py", "x"):
                console.print("▶ [underline]main.py[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_py_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_py_project_dir)

            if self.cli_args.pycharm:
                self.open_in_pycharm(project_dir=new_py_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")

            # cd into the new project dir
        except FileExistsError:
            console.print(
                f"[orange3]{new_py_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * JAVA
    def create_java_project(self) -> None:
        """
        Create a java projects
        """
        self.projects_path_check(projects_dir_name=JAVA_PROJECTS_DIR_NAME)

        java_projects_path = os.path.join(DEV_DIR, JAVA_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_java_project_dir = f"{java_projects_path}/{self.cli_args.java}"
        try:
            os.mkdir(new_java_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            os.mkdir(f"{new_java_project_dir}/src")
            with open(f"{new_java_project_dir}/src/Main.java", "x"):
                console.print("▶ [underline]Main.java[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_java_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_java_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_java_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * GO
    def create_go_project(self) -> None:
        """
        Create a go projects
        """
        self.projects_path_check(projects_dir_name=GO_PROJECTS_DIR_NAME)

        go_projects_path = os.path.join(DEV_DIR, GO_PROJECTS_DIR_NAME)
        # Creating the project folder
        new_go_project_dir = f"{go_projects_path}/{self.cli_args.go}"
        try:
            os.mkdir(new_go_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            with open(f"{new_go_project_dir}/main.go", "x"):
                console.print("▶ [underline]main.go[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(project_dir=new_go_project_dir)

            if self.cli_args.code:
                self.open_in_vscode(project_dir=new_go_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_go_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * BASH
    def create_bash_project(self) -> None:
        """
        Create a bash project
        """
        self.projects_path_check(projects_dir_name=BASH_PROJECTS_DIR_NAME)

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
                f"[orange3]{new_bash_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * RUST
    def create_rust_project(self) -> None:
        """
        Create a rust project
        """
        self.projects_path_check(projects_dir_name=RUST_PROJECTS_DIR_NAME)

        rust_projects_path = os.path.join(DEV_DIR, RUST_PROJECTS_DIR_NAME)
        # Creating the project folder and file structure for the project
        console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
        new_rust_project_dir = f"{rust_projects_path}/{self.cli_args.rust}"
        subprocess.run(["cargo", "new", new_rust_project_dir])
        console.print("✓ Done." + "\n")

        if self.cli_args.code:
            self.open_in_vscode(project_dir=new_rust_project_dir)

        console.print("[gold1]⫸ Happy Coding![/gold1]")

    # * CPP
    def create_cpp_project(self) -> None:
        """
        Create a cpp project
        """
        self.projects_path_check(projects_dir_name=CPP_PROJECTS_DIR_NAME)

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
                f"[orange3]{new_cpp_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * NON-SPECIFIC PROJECTS
    def create_non_specific_project(self) -> None:
        """
        Create a non specific project
        """
        self.projects_path_check(projects_dir_name=NON_SPECIFIC_PROJECTS_DIR_NAME)

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
                f"[orange3]{new_non_specific_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
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
