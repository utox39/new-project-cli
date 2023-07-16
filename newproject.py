#!/usr/bin/env python3

import errno
import os
import json
import subprocess
import sys
import textwrap
import typer

from pathlib import Path
from rich.console import Console
from shutil import which
from typing_extensions import Annotated
from typing import Final

# rich config
console = Console()

# Config file
CONFIG_FILE: Final[str] = f"{Path.home()}/.config/newproject/newproject_config.json"

# Load json config file
try:
    with open(CONFIG_FILE) as config_file:
        new_project_config = json.load(config_file)
except FileNotFoundError:
    print("Error: Json config file not found")
    sys.exit(errno.ENOENT)

# Default Development folder
DEV_DIR: Final[str] = f"{Path.home()}/{new_project_config['dev_dir']}"

# Projects folder names
PY_PROJECTS_DIR_NAME: Final[str] = new_project_config["py_projects_dir_name"]
JAVA_PROJECTS_DIR_NAME: Final[str] = new_project_config["java_projects_dir_name"]
GO_PROJECTS_DIR_NAME: Final[str] = new_project_config["go_projects_dir_name"]
BASH_PROJECTS_DIR_NAME: Final[str] = new_project_config["bash_projects_dir_name"]
RUST_PROJECTS_DIR_NAME: Final[str] = new_project_config["rust_projects_dir_name"]
CPP_PROJECTS_DIR_NAME: Final[str] = new_project_config["cpp_projects_dir_name"]
CLANG_PROJECTS_DIR_NAME: Final[str] = new_project_config["clang_projects_dir_name"]
PHP_PROJECTS_DIR_NAME: Final[str] = new_project_config["php_projects_dir_name"]
LUA_PROJECTS_DIR_NAME: Final[str] = new_project_config["lua_projects_dir_name"]
RUBY_PROJECTS_DIR_NAME: Final[str] = new_project_config["ruby_projects_dir_name"]
DART_PROJECTS_DIR_NAME: Final[str] = new_project_config["dart_projects_dir_name"]
FLUTTER_PROJECTS_DIR_NAME: Final[str] = new_project_config["flutter_projects_dir_name"]
OCAML_PROJECTS_DIR_NAME: Final[str] = new_project_config["ocaml_projects_dir_name"]
VLANG_PROJECTS_DIR_NAME: Final[str] = new_project_config["vlang_projects_dir_name"]
WEB_PROJECTS_DIR_NAME: Final[str] = new_project_config["web_projects_dir_name"]

# Outputs
DONE: Final[str] = "✓ Done.\n"
PROJECT_STRUCTURE_GEN: Final[str] = "[dodger_blue1]Creating the project structure...[/dodger_blue1]"
HAPPY_CODING: Final[str] = "[gold1]⫸ Happy Coding![/gold1]"


def dev_dir_check() -> bool:
    """
    Check if the development folder exists
    :return bool: True if the development folder exists
    """
    try:
        if not os.path.isdir(DEV_DIR):
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"Error: {DEV_DIR} does not exists")
        sys.exit(errno.ENOENT)
    else:
        return True


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


def open_in_ide(ide_command: str, project_dir: str) -> None:
    """
    Open the project in the specified IDE
    :param ide_command: (str) the console command to open the IDE
    :param project_dir: (str) the project directory to open in the IDE
    """
    if ide_command == "code" or ide_command == "pycharm" or ide_command == "idea":
        if which(f"{ide_command}") is not None:
            try:
                subprocess.run([f"{ide_command}", f"{project_dir}"])
            except Exception as open_in_ide_error:
                print(f"Error: {open_in_ide_error}\nCould not open project in IDE")
        else:
            console.print(f"[red][underline]{ide_command}[/underline]: command not found...[/red]")


def git_init_command(project_dir: str, projects_dir_name: str) -> None:
    """
    Initialize a local git repository
    :param project_dir: (str) project directory
    :param projects_dir_name: (str) projects directory name
    """
    console.print(
        "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
    )
    if which("git") is not None:
        subprocess.run(["git", "init", f"{project_dir}"])

        with open(f"{project_dir}/.gitignore", "w") as git_ignore_f:
            if projects_dir_name == PY_PROJECTS_DIR_NAME:
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

        print(DONE)


def create_and_write_file(new_project_dir: str, file_name: str, content: str) -> None:
    """
    Creates and writes a file
    :param new_project_dir: (str) the directory of the new project
    :param file_name: (str) file's name
    :param content: (str) content to write to file
    """
    # Creating the file structure
    console.print(PROJECT_STRUCTURE_GEN)
    with open(f"{new_project_dir}/{file_name}", "w") as project_file:
        project_file.write(content)
        console.print(f"▶ [underline]{file_name}[/underline] created.")
    print(DONE)


def create_python_venv(new_project_path: str) -> None:
    """
    Create a python venv
    :param new_project_path: (str) path of the new python project
    """
    console.print(
        "[dodger_blue1]Generating the [underline]venv[/underline]...[/dodger_blue1]"
    )
    try:
        if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
            with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
            # Windows
        if sys.platform.startswith("win32"):
            with console.status("[dodger_blue1]Generating...[/dodger_blue1]", spinner="aesthetic"):
                if which("virtualenv") is not None:
                    subprocess.run(["virtualenv", f"{new_project_path}/venv"])
                else:
                    subprocess.run(["python3", "-m", "venv", f"{new_project_path}/venv"])
        print(DONE)
    except Exception as venv_exception:
        print(f"Error: {venv_exception}")
        sys.exit(1)


def create_readme(new_project_dir, project_name):
    with open(f"{new_project_dir}/README.md", "w") as readme:
        readme.write(f"# {project_name}")


def create_project(
        projects_dir_name: str,
        project_name: str,
        file_name: str = "",
        file_content: str = "",
        ide: str = "",
):
    """
    Create a new project
    :param projects_dir_name: (str) the name of the specified programming language's directory
    :param project_name: (str) the name of the new project
    :param file_name: (str) the name of the file
    :param file_content: (str) content to write to file
    :param ide: (str) the name of the IDE where you want to open the new project
    """
    # check if the specified projects folder exists
    projects_path_check(projects_dir_to_check=projects_dir_name)

    projects_path = os.path.join(DEV_DIR, projects_dir_name)
    # Creating the project folder
    new_project_dir = f"{projects_path}/{project_name}"

    try:
        console.print("[dodger_blue1]Creating the project structure...[/dodger_blue1]")

        os.mkdir(new_project_dir)

        if projects_dir_name == PY_PROJECTS_DIR_NAME:
            # Generating a python venv for the project
            create_python_venv(new_project_path=new_project_dir)

        # Creating the file structure
        create_and_write_file(new_project_dir=new_project_dir, file_name=file_name, content=file_content)

        # Creating the README for the new project
        create_readme(new_project_dir=new_project_dir, project_name=project_name)

        # git init
        git_init_command(project_dir=new_project_dir, projects_dir_name=projects_dir_name)

        # Open in IDE
        open_in_ide(ide_command=ide, project_dir=new_project_dir)

        console.print(HAPPY_CODING)

    except FileExistsError:
        console.print(
            f"{new_project_dir} [bold red3]already exists![/bold red3]"
        )
        sys.exit(errno.EEXIST)


def create_project_with_commands(
        projects_dir_name: str,
        project_name: str,
        ide: str = "",
):
    """
    Create a new project via dedicated commands.
    :param projects_dir_name: (str) the name of the specified programming language's directory
    :param project_name: (str) the name of the new project
    :param ide: (str) the name of the IDE where you want to open the new project
    """
    projects_path_check(projects_dir_to_check=projects_dir_name)

    projects_path = os.path.join(DEV_DIR, projects_dir_name)
    # Creating the project folder
    new_project_dir = f"{projects_path}/{project_name}"

    # Creating the project folder and file structure for the project
    console.print(PROJECT_STRUCTURE_GEN)

    commands = []

    if projects_dir_name == RUST_PROJECTS_DIR_NAME:
        commands = ["cargo", "new", new_project_dir]
    elif projects_dir_name == RUBY_PROJECTS_DIR_NAME:
        commands = ["bundler", "gem", new_project_dir]
    elif projects_dir_name == DART_PROJECTS_DIR_NAME:
        commands = ["dart", "create", new_project_dir]
    elif projects_dir_name == FLUTTER_PROJECTS_DIR_NAME:
        commands = ["flutter", "create", new_project_dir]
    elif projects_dir_name == OCAML_PROJECTS_DIR_NAME:
        commands = ["dune", "init", "project", new_project_dir]
    elif projects_dir_name == VLANG_PROJECTS_DIR_NAME:
        commands = ["v", "new", new_project_dir]

    if which(commands[0]) is not None:
        try:
            subprocess.run(commands)
            print(DONE)
            # Open in IDE
            open_in_ide(ide_command=ide, project_dir=new_project_dir)

            console.print(HAPPY_CODING)
        except Exception as command_exception:
            print(f"Error: {command_exception}\nCould not create the project")
    else:
        console.print(f"[red][underline]{commands[0]}[/underline]: command not found...[/red]")


def create_web_project(
        projects_dir_name: str,
        project_name: str,
        file_content: str = "",
        ide: str = "",
):
    """
    Create a basic new web project
    :param projects_dir_name:
    :param project_name:
    :param file_content:
    :param ide:
    """
    # check if the specified projects folder exists
    projects_path_check(projects_dir_to_check=projects_dir_name)

    projects_path = os.path.join(DEV_DIR, projects_dir_name)
    # Creating the project folder
    new_project_dir = f"{projects_path}/{project_name}"

    try:
        console.print(PROJECT_STRUCTURE_GEN)

        os.mkdir(new_project_dir)
        os.mkdir(f"{new_project_dir}/styles")
        os.mkdir(f"{new_project_dir}/scripts")

        # Creating the file structure

        # Creating Html file
        create_and_write_file(new_project_dir=new_project_dir, file_name="index.html", content=file_content)
        # Creating Css file
        create_and_write_file(new_project_dir=f"{new_project_dir}/styles", file_name="style.css", content=file_content)
        # Creating Javascript file
        create_and_write_file(new_project_dir=f"{new_project_dir}/scripts", file_name="index.js", content=file_content)

        # Creating the README for the new project
        create_readme(new_project_dir=new_project_dir, project_name=project_name)

        # git init
        git_init_command(project_dir=new_project_dir, projects_dir_name=projects_dir_name)

        # Open in IDE
        open_in_ide(ide_command=ide, project_dir=new_project_dir)

        console.print(HAPPY_CODING)

    except FileExistsError:
        console.print(
            f"{new_project_dir} [bold red3]already exists![/bold red3]"
        )
        sys.exit(errno.EEXIST)


def handle(
        project_name: Annotated[str, typer.Argument(help="The name of the new project")],
        python: Annotated[bool, typer.Option(help="create a python project")] = False,
        java: Annotated[bool, typer.Option(help="create a java project")] = False,
        go: Annotated[bool, typer.Option(help="create a go project")] = False,
        bash: Annotated[bool, typer.Option(help="create a bash project")] = False,
        cpp: Annotated[bool, typer.Option(help="create a cpp project")] = False,
        clang: Annotated[bool, typer.Option(help="create a c project")] = False,
        php: Annotated[bool, typer.Option(help="create a php project")] = False,
        lua: Annotated[bool, typer.Option(help="create a lua project")] = False,
        rust: Annotated[bool, typer.Option(help="create a rust project")] = False,
        ruby: Annotated[bool, typer.Option(help="create a ruby project")] = False,
        dart: Annotated[bool, typer.Option(help="create a dart project")] = False,
        flutter: Annotated[bool, typer.Option(help="create a flutter project")] = False,
        ocaml: Annotated[bool, typer.Option(help="create an ocaml project")] = False,
        vlang: Annotated[bool, typer.Option(help="create a vlang project")] = False,
        web: Annotated[bool, typer.Option(help="create a basic web project")] = False,
        code: Annotated[bool, typer.Option(help="open the project in VS Code")] = False,
        pycharm: Annotated[bool, typer.Option(help="open the project in PyCharm")] = False,
        idea: Annotated[bool, typer.Option(help="open the project in Intellij IDEA")] = False
):
    """
    Create a new project via terminal

    Coded with <3 by utox39
    """
    ide_name = ""
    if code:
        ide_name = "code"
    elif pycharm:
        ide_name = "pycharm"
    elif idea:
        ide_name = "idea"

    if dev_dir_check():
        if python:
            create_project(
                projects_dir_name=PY_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="main.py",
                file_content=new_project_config["file_content"][0]["python_content"],
                ide=ide_name,
            )
        elif java:
            create_project(
                projects_dir_name=JAVA_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="Main.java",
                ide=ide_name,
            )
        elif go:
            create_project(
                projects_dir_name=GO_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="main.go",
                ide=ide_name,
            )
        elif bash:
            create_project(
                projects_dir_name=BASH_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name=f"{project_name}.sh",
                file_content=new_project_config["file_content"][0]["bash_content"],
                ide=ide_name,
            )
        elif cpp:
            create_project(
                projects_dir_name=CPP_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="main.cpp",
                file_content=new_project_config["file_content"][0]["cpp_content"],
                ide=ide_name,
            )

        elif clang:
            create_project(
                projects_dir_name=CLANG_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="main.c",
                file_content=new_project_config["file_content"][0]["c_lang_content"],
                ide=ide_name,
            )
        elif php:
            create_project(
                projects_dir_name=PHP_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="index.php",
                ide=ide_name,
            )
        elif lua:
            create_project(
                projects_dir_name=LUA_PROJECTS_DIR_NAME,
                project_name=project_name,
                file_name="main.lua",
                ide=ide_name,
            )
        elif rust:
            create_project_with_commands(
                projects_dir_name=RUST_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        elif ruby:
            create_project_with_commands(
                projects_dir_name=RUBY_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        elif dart:
            create_project_with_commands(
                projects_dir_name=DART_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        elif flutter:
            create_project_with_commands(
                projects_dir_name=FLUTTER_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        elif ocaml:
            create_project_with_commands(
                projects_dir_name=OCAML_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )

        elif web:
            create_web_project(
                projects_dir_name=WEB_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        elif vlang:
            create_project_with_commands(
                projects_dir_name=VLANG_PROJECTS_DIR_NAME,
                project_name=project_name,
                ide=ide_name
            )
        else:
            console.print("[bold red]No option provided[/bold red]")


def main():
    typer.run(handle)


if __name__ == "__main__":
    main()
