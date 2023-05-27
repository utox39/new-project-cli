#!/usr/bin/env python3

import argparse
import os
import subprocess
import textwrap

from pathlib import Path

# rich
from rich.console import Console

# rich config
console = Console()

# Default Development folder
DEV_DIR = f"{Path.home()}/Developer/projects/"


class NewProject:
    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        self.handler()

    def git_init_command(self, project_dir):
        console.print(
            "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
        )
        subprocess.run(["git", "init", f"{project_dir}"])

        with open(f"{project_dir}/.gitignore", "w") as git_ignore_f:
            if self.cli_args.python:
                git_ignore_f.write(
                    """.env
venv/
test/
.vscode/
.idea/"""
                )
            else:
                git_ignore_f.write(
                    """.env
test/
.vscode/
.idea/"""
                )

            console.print("▶ [underline].gitignore[/underline] created.")

        console.print("✓ Done." + "\n")

    @staticmethod
    def open_in_vscode(project_dir):
        subprocess.run(["code", f"{project_dir}"])

    @staticmethod
    def open_in_pycharm(project_dir):
        subprocess.run(["pycharm", f"{project_dir}"])

    # * PYTHON
    def create_python_project(self):
        py_projects_dir_name = "python_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            py_projects_path = os.path.join(shared_dev_dir, py_projects_dir_name)
        else:
            py_projects_path = os.path.join(DEV_DIR, py_projects_dir_name)
        if not os.path.isdir(py_projects_path):
            os.mkdir(py_projects_path)
            console.print("Python projects dir [underline]created.[/underline]")

        # Creating the project folder
        new_py_project_dir = f"{py_projects_path}/{self.cli_args.python}"
        try:
            os.mkdir(new_py_project_dir)

            # python -m venv NEW_PROJECT_DIR/venv
            console.print(
                "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
            )
            with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                subprocess.run(["python3", "-m", "venv", f"{new_py_project_dir}/venv"])
            console.print("✓ Done." + "\n")

            # Creating the file structure
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            os.mkdir(f"{new_py_project_dir}/src")
            with open(f"{new_py_project_dir}/src/__init__.py", "x"):
                console.print("▶ [underline]__init__.py[/underline] created.")
            with open(f"{new_py_project_dir}/src/main.py", "x"):
                console.print("▶ [underline]main.py[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(new_py_project_dir)

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
    def create_java_project(self):
        java_projects_dir_name = "java_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            java_projects_path = os.path.join(shared_dev_dir, java_projects_dir_name)
        else:
            java_projects_path = os.path.join(DEV_DIR, java_projects_dir_name)
        if not os.path.isdir(java_projects_path):
            os.mkdir(java_projects_path)
            console.print("Java projects dir [underline]created.[/underline]")

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
            self.git_init_command(new_java_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_java_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * GO
    def create_go_project(self):
        go_projects_dir_name = "go_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            go_projects_path = os.path.join(shared_dev_dir, go_projects_dir_name)
        else:
            go_projects_path = os.path.join(DEV_DIR, go_projects_dir_name)
        if not os.path.isdir(go_projects_path):
            os.mkdir(go_projects_path)
            console.print("Go projects dir [underline]created.[/underline]")

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
            self.git_init_command(new_go_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_go_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * BASH
    def create_bash_project(self):
        bash_projects_dir_name = "bash_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            bash_projects_path = os.path.join(shared_dev_dir, bash_projects_dir_name)
        else:
            bash_projects_path = os.path.join(DEV_DIR, bash_projects_dir_name)
        if not os.path.isdir(bash_projects_path):
            os.mkdir(bash_projects_path)
            console.print("Bash projects dir [underline]created.[/underline]")

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
            self.git_init_command(new_bash_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_bash_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * RUST
    def create_rust_project(self):
        rust_projects_dir_name = "rust_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            rust_projects_path = os.path.join(shared_dev_dir, rust_projects_dir_name)
        else:
            rust_projects_path = os.path.join(DEV_DIR, rust_projects_dir_name)
        if not os.path.isdir(rust_projects_path):
            os.mkdir(rust_projects_path)
            console.print("Rust projects dir [underline]created.[/underline]")

        # Creating the project folder and file structure for the project
        console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
        new_rust_project_dir = f"{rust_projects_path}/{self.cli_args.rust}"
        subprocess.run(["cargo", "new", new_rust_project_dir])
        console.print("✓ Done." + "\n")

        console.print("[gold1]⫸ Happy Coding![/gold1]")

    # * CPP
    def create_cpp_project(self):
        cpp_projects_dir_name = "cpp_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            cpp_projects_path = os.path.join(shared_dev_dir, cpp_projects_dir_name)
        else:
            cpp_projects_path = os.path.join(DEV_DIR, cpp_projects_dir_name)
        if not os.path.isdir(cpp_projects_path):
            os.mkdir(cpp_projects_path)
            console.print("Cpp projects dir [underline]created.[/underline]")

        # Creating the project folder
        new_cpp_project_dir = f"{cpp_projects_path}/{self.cli_args.cpp}"
        try:
            os.mkdir(new_cpp_project_dir)

            # Creating the file structure for the project
            console.print(f"[dodger_blue1]Creating the file structure...[/dodger_blue1]")
            os.mkdir(f"{new_cpp_project_dir}/src")
            with open(f"{new_cpp_project_dir}/src/main.cpp", "w") as main_f:
                main_f.write(
                    """#include <iostream>

int main()
{
    return 0;
}
            """
                )
                console.print("▶ [underline]main.cpp[/underline] created.")
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(new_cpp_project_dir)

            console.print("[gold1]⫸ Happy Coding![/gold1]")
        except FileExistsError:
            console.print(
                f"[orange3]{new_cpp_project_dir}[/orange3] [bold red3]already exists![/bold red3]"
            )

    # * NON-SPECIFIC PROJECTS
    def create_non_specific_project(self):
        non_specific_projects_dir_name = "non_specific_projects"
        if self.cli_args.shared:
            shared_dev_dir = f"{Path.home()}/Developer/shared_projects/"
            non_specific_projects_path = os.path.join(
                shared_dev_dir,
                non_specific_projects_dir_name,
            )
        else:
            non_specific_projects_path = os.path.join(DEV_DIR, non_specific_projects_dir_name)
        if not os.path.isdir(non_specific_projects_path):
            os.mkdir(non_specific_projects_path)
            console.print("Non-specific projects dir created.")

        # Creating the project folder
        new_non_specific_project_dir = f"{non_specific_projects_path}/{self.cli_args.none}"
        try:
            os.mkdir(new_non_specific_project_dir)
            console.print("✓ Done." + "\n")

            # git init {project dir}
            self.git_init_command(new_non_specific_project_dir)

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
    # TODO: improve information
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
        new_project --shared --python PROJECT_NAME   #create a new shared python project
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
        "--shared",
        action="store_true",
        help="create the project in the shared_projects folder",
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

    new_project = NewProject(args)
    new_project.run()
