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


# TODO: beautify the output with rich
class NewProject:
    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        self.handler()

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
            console.print(
                "[gold1]Pyt[/gold1][blue1]hon[/blue1] projects dir [bold green4]created.[/bold green4]"
            )

        # Creating the project folder
        new_py_project_dir = f"{py_projects_path}/{self.cli_args.python}"
        try:
            os.mkdir(new_py_project_dir)

            # python -m venv NEW_PROJECT_DIR/venv
            console.print("[dodger_blue1]Generating the venv for your project...[/dodger_blue1]")
            subprocess.run(["python3", "-m", "venv", f"{new_py_project_dir}/venv"])
            console.print("[bold green4]Done.[/bold green4]\n")

            # Creating the project folder
            console.print(
                f"[dodger_blue1]Creating the file structure for:[/dodger_blue1] [gold1]{self.cli_args.python}[/gold1]"
                + "\n"
            )
            os.mkdir(f"{new_py_project_dir}/src")
            with open(f"{new_py_project_dir}/src/__init__.py", "x"):
                console.print("[bold green4]__init__.py created.[/bold green4]")
            with open(f"{new_py_project_dir}/src/main.py", "x"):
                console.print("[bold green4]main.py created.[/bold green4]" + "\n")
            subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_py_project_dir])
            console.print("\n[bold green4]Done.[bold green4]\n")

            console.print("[gold1]Happy Coding![/gold1]")
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
            console.print(
                "[dark_orange3]Ja[/dark_orange3][bright_white]va[/bright_white] projects dir [bold green4]created.[/bold green4]"
            )

        # Creating the project folder
        new_java_project_dir = f"{java_projects_path}/{self.cli_args.java}"
        try:
            os.mkdir(new_java_project_dir)

            # Creating the file structure for the project
            console.print(
                f"[dodger_blue1]Creating the file structure for:[/dodger_blue1] [gold1]{self.cli_args.java}[/gold1]"
                + "\n"
            )
            os.mkdir(f"{new_java_project_dir}/src")
            with open(f"{new_java_project_dir}/src/Main.java", "x"):
                console.print("[bold green4]Main.java created.[/bold green4]")
            subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_java_project_dir])
            console.print("\n[bold green4]Done.[bold green4]")

            console.print("[gold1]Happy Coding![/gold1]")
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
            console.print(
                "[dark_turquoise]Go[/dark_turquoise] projects dir [bold green4]created.[/bold green4]"
            )

        # Creating the project folder
        new_go_project_dir = f"{go_projects_path}/{self.cli_args.go}"
        try:
            os.mkdir(new_go_project_dir)

            # Creating the file structure for the project
            console.print(
                f"[dodger_blue1]Creating the file structure for:[/dodger_blue1] [gold1]{self.cli_args.go}[/gold1]"
                + "\n"
            )
            with open(f"{new_go_project_dir}/main.go", "x"):
                console.print("main.go created.")
            subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_go_project_dir])
            console.print("\nDone.")

            console.print("Happy Coding!")
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
            console.print("Bash projects dir created.")

        # Creating the project folder
        new_bash_project_dir = f"{bash_projects_path}/{self.cli_args.bash}"
        try:
            os.mkdir(new_bash_project_dir)

            # Creating the file structure for the project
            console.print(f"Creating the file structure for: {self.cli_args.bash}" + "\n")
            with open(f"{new_bash_project_dir}/{self.cli_args.bash}.sh", "w") as main_f:
                main_f.write("#!/bin/bash")
                console.print("Bash script created.")
            subprocess.run(["chmod", "+x", f"{new_bash_project_dir}/{self.cli_args.bash}.sh"])
            subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_bash_project_dir])
            console.print("\nDone.")

            console.print("Happy Coding!")
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
            console.print("Rust projects dir created.")

        # Creating the project folder and file structure for the project
        new_rust_project_dir = f"{rust_projects_path}/{self.cli_args.rust}"
        subprocess.run(["cargo", "new", new_rust_project_dir])
        subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_rust_project_dir])
        console.print("\nDone.")

        console.print("Happy Coding!")

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
            console.print("Cpp projects dir created.")

        # Creating the project folder
        new_cpp_project_dir = f"{cpp_projects_path}/{self.cli_args.cpp}"
        try:
            os.mkdir(new_cpp_project_dir)

            # Creating the file structure for the project
            console.print(f"Creating the file structure for: {self.cli_args.cpp}" + "\n")
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
                console.print("Main.cpp created.")
            subprocess.run(["exa", "--all", "--header", "--icons", "--long", new_cpp_project_dir])
            console.print("\nDone.")

            print("Happy Coding!")
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
            console.print("\nDone.")

            console.print("Happy Coding!")
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
    args = parser.parse_args()

    new_project = NewProject(args)
    new_project.run()
