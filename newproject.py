#!/usr/bin/env python3

import errno
import json
import jsonschema
import logging
import os
import subprocess
import sys
import typer
import yaml

from pathlib import Path
from rich.console import Console
from shutil import which
from typing_extensions import Annotated
from typing import Final

# rich config
console = Console()

# Config file
CONFIG_FILE: Final[str] = f"{Path.home()}/.config/newproject/newproject_config.yaml"
JSON_SCHEMA: Final[str] = f"{Path.home()}/.config/newproject/schemas/json_schema.json"

# Logging config
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Loads YAML config file
try:
    with open(CONFIG_FILE) as config_file:
        new_project_config = yaml.safe_load(config_file)
except FileNotFoundError as yaml_file_not_found_error:
    logger.error(yaml_file_not_found_error)
    sys.exit(errno.ENOENT)

# Default Development folder
DEV_DIR: Final[str] = f"{Path.home()}/{new_project_config['development_dir_path']}"

# Project folder names
PROJECTS_DIR_NAMES: Final[dict] = {
    "bash": new_project_config["bash"]["projects_dir_name"],
    "c_lang": new_project_config["c_lang"]["projects_dir_name"],
    "cpp": new_project_config["cpp"]["projects_dir_name"],
    "dart": new_project_config["dart"]["projects_dir_name"],
    "flutter": new_project_config["flutter"]["projects_dir_name"],
    "go": new_project_config["go"]["projects_dir_name"],
    "java": new_project_config["java"]["projects_dir_name"],
    "lua": new_project_config["lua"]["projects_dir_name"],
    "ocaml": new_project_config["ocaml"]["projects_dir_name"],
    "php": new_project_config["php"]["projects_dir_name"],
    "python": new_project_config["python"]["projects_dir_name"],
    "ruby": new_project_config["ruby"]["projects_dir_name"],
    "rust": new_project_config["rust"]["projects_dir_name"],
    "vlang": new_project_config["vlang"]["projects_dir_name"],
    "web": new_project_config["web"]["projects_dir_name"],
}

# Outputs
DONE: Final[str] = "✓ Done.\n"
PROJECT_STRUCTURE_GEN: Final[str] = "[dodger_blue1]Creating the project structure...[/dodger_blue1]"
HAPPY_CODING: Final[str] = "[gold1]⫸ Happy Coding![/gold1]"
COULD_NOT_CREATE_PROJECT: Final[str] = "[red3]𝙓 Could not create the project[/red3]"


def config_file_validator():
    try:
        with open(JSON_SCHEMA) as json_schema_f:
            json_schema = json.load(json_schema_f)
    except FileNotFoundError as json_schema_not_found_error:
        logger.error(json_schema_not_found_error)
        sys.exit(errno.ENOENT)

    try:
        jsonschema.validate(instance=new_project_config, schema=json_schema)
        return True
    except jsonschema.ValidationError as validation_error:
        if validation_error.relative_path:
            print(f"{validation_error.relative_path[0]}:")

            message_len = len(validation_error.relative_path) - 1
            if validation_error.validator == "required":
                print(f"  {validation_error.message[1:-24]} (missing)\n")
            else:
                print(f"  {validation_error.relative_path[message_len]}:(type error)\n")

        print(f"YAML Config File Error: {validation_error.message}")
        # print(json.dumps(validation_error.instance, indent=4))
        if validation_error.context:
            print(validation_error.context)
        if validation_error.cause:
            print(validation_error.cause)


def dev_dir_check() -> bool:
    """
    Check if the development folder exists
    :return bool: True if the development folder exists
    """
    try:
        if not os.path.isdir(DEV_DIR):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), DEV_DIR)
    except FileNotFoundError as dev_dir_not_found_error:
        logging.error(dev_dir_not_found_error)
        console.print(f"[red3]{DEV_DIR} does not exist[/red3]")
        console.print("[dark_orange3]Change it the YAML config file[/dark_orange3]")
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
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), projects_path)
    except FileNotFoundError as projects_path_not_found_error:
        logging.error(projects_path_not_found_error)
        console.print(f"[red3]{projects_dir_to_check} does not exist[/red3]")
        console.print("[dark_orange3]Change it the YAML config file[/dark_orange3]")
        sys.exit(errno.ENOENT)


def open_in_ide(ide_command: str, project_dir: str) -> None:
    """
    Open the project in the specified IDE
    :param ide_command: (str) the console command to open the IDE
    :param project_dir: (str) the project directory to open in the IDE
    """
    if ide_command in ["code", "pycharm", "idea"]:
        if which(f"{ide_command}") is not None:
            try:
                subprocess.run([f"{ide_command}", project_dir])
            except Exception as open_in_ide_error:
                logging.error(open_in_ide_error)
        else:
            console.print(f"[red][underline]{ide_command}[/underline]: command not found...[/red]")


def git_init_command(project_dir: str, content: str) -> None:
    """
    Initialize a local git repository
    :param project_dir: (str) project directory
    :param content: (str) the content of the .gitignore file
    """
    console.print(
        "[dodger_blue1]Initializing [underline]git[/underline] repository[/dodger_blue1]"
    )
    if which("git") is not None:
        try:
            subprocess.run(["git", "init", project_dir])

            # Creating .gitignore file
            try:
                with open(f"{project_dir}/.gitignore", "w") as gitignore_f:
                    if content != "":
                        gitignore_f.write(content)
                    else:
                        gitignore_f.write(new_project_config["default_gitignore_content"])

                    console.print("▶ [underline].gitignore[/underline] created.")

                    print(DONE)

            except Exception as gitignore_error:
                logging.error(gitignore_error)
                console.print("[red3]𝙓 Can't create .gitignore file[/red3]")

        except Exception as git_error:
            logging.error(git_error)
            console.print("[red3]𝙓 git repository not initialized[/red3]")


def create_and_write_file(new_project_dir: str, file_name: str, content: str) -> None:
    """
    Creates and writes a file
    :param new_project_dir: (str) the directory of the new project
    :param file_name: (str) file's name
    :param content: (str) content to write to file
    """
    # Creating the file structure
    console.print(PROJECT_STRUCTURE_GEN)
    try:
        with open(f"{new_project_dir}/{file_name}", "w") as project_file:
            project_file.write(content)
            console.print(f"▶ [underline]{file_name}[/underline] created.")
        print(DONE)
    except Exception as create_and_write_file_error:
        logging.error(create_and_write_file_error)


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
        logging.error(venv_exception)
        console.print("[red3]𝙓 Can't create venv [/red3]")


def create_readme(new_project_dir, project_name):
    try:
        with open(f"{new_project_dir}/README.md", "w") as readme:
            readme.write(f"# {project_name}")
    except Exception as readme_error:
        logging.error(readme_error)
        console.print("[red3]𝙓 Can't create README.md file[/red3]")


def create_project(
        projects_dir_name: str,
        project_name: str,
        file_name: str,
        file_content: str,
        gitignore_content: str,
        ide: str = "",
):
    """
    Create a new project
    :param projects_dir_name: (str) the name of the specified programming language's directory
    :param project_name: (str) the name of the new project
    :param file_name: (str) the name of the file
    :param file_content: (str) content to write to file
    :param gitignore_content: (str) the content of the .gitignore file
    :param ide: (str) the name of the IDE where you want to open the new project
    """
    # check if the specified projects folder exists
    projects_path_check(projects_dir_to_check=projects_dir_name)

    projects_path = os.path.join(DEV_DIR, projects_dir_name)
    # Creating the project folder
    new_project_dir = f"{projects_path}/{project_name}"

    try:
        console.print(PROJECT_STRUCTURE_GEN)

        os.mkdir(new_project_dir)

        if projects_dir_name == PROJECTS_DIR_NAMES["python"]:
            # Generating a python venv for the project
            create_python_venv(new_project_path=new_project_dir)

        # Creating the file structure
        create_and_write_file(new_project_dir=new_project_dir, file_name=file_name, content=file_content)

        # Creating the README for the new project
        create_readme(new_project_dir=new_project_dir, project_name=project_name)

        # git init
        git_init_command(project_dir=new_project_dir, content=gitignore_content)

        # Open in IDE
        open_in_ide(ide_command=ide, project_dir=new_project_dir)

        console.print(HAPPY_CODING)

    except FileExistsError:
        console.print(
            f"{new_project_dir} [bold red3]already exists![/bold red3]"
        )
        console.print(COULD_NOT_CREATE_PROJECT)
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

    if projects_dir_name == PROJECTS_DIR_NAMES["rust"]:
        commands = ["cargo", "new", new_project_dir]
    elif projects_dir_name == PROJECTS_DIR_NAMES["ruby"]:
        commands = ["bundler", "gem", new_project_dir]
    elif projects_dir_name == PROJECTS_DIR_NAMES["ocaml"]:
        commands = ["dune", "init", "project", new_project_dir]
    elif projects_dir_name == PROJECTS_DIR_NAMES["vlang"]:
        commands = ["v", "new", new_project_dir]

    if which(commands[0]) is not None:
        try:
            subprocess.run(commands)
            print(DONE)
            # Open in IDE
            open_in_ide(ide_command=ide, project_dir=new_project_dir)

            console.print(HAPPY_CODING)
        except Exception as command_exception:
            logging.error(command_exception)
            console.print(COULD_NOT_CREATE_PROJECT)
    else:
        console.print(f"[red][underline]{commands[0]}[/underline]: command not found...[/red]")


def create_web_project(
        projects_dir_name: str,
        project_name: str,
        html_file_content: str,
        css_file_content: str,
        javascript_file_content: str,
        gitignore_content: str,
        ide: str = "",
):
    """
    Create a basic new web project
    :param projects_dir_name: (str) the name of the specified programming language's directory
    :param project_name: (str) the name of the new project
    :param html_file_content: (str) the content of the html file
    :param css_file_content: (str) the content of the css file
    :param javascript_file_content: (str) the content of the javascript file
    :param gitignore_content: (str) the content of the .gitignore file
    :param ide: (str) the name of the IDE where you want to open the new project
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
        create_and_write_file(new_project_dir=new_project_dir, file_name="index.html", content=html_file_content)
        # Creating Css file
        create_and_write_file(new_project_dir=f"{new_project_dir}/styles", file_name="style.css",
                              content=css_file_content)
        # Creating Javascript file
        create_and_write_file(new_project_dir=f"{new_project_dir}/scripts", file_name="index.js",
                              content=javascript_file_content)

        # Creating the README for the new project
        create_readme(new_project_dir=new_project_dir, project_name=project_name)

        # git init
        git_init_command(project_dir=new_project_dir, content=gitignore_content)

        # Open in IDE
        open_in_ide(ide_command=ide, project_dir=new_project_dir)

        console.print(HAPPY_CODING)

    except FileExistsError:
        console.print(
            f"{new_project_dir} [bold red3]already exists![/bold red3]"
        )
        console.print(COULD_NOT_CREATE_PROJECT)
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

    if config_file_validator() and dev_dir_check():
        project_mapping = {
            python: (create_project,
                     PROJECTS_DIR_NAMES["python"],
                     project_name,
                     "main.py",
                     new_project_config["python"]["file_content"],
                     new_project_config["python"]["gitignore_content"],
                     ide_name
                     ),
            java: (create_project,
                   PROJECTS_DIR_NAMES["java"],
                   project_name,
                   "Main.java",
                   new_project_config["java"]["file_content"],
                   new_project_config["java"]["gitignore_content"],
                   ide_name
                   ),
            go: (create_project,
                 PROJECTS_DIR_NAMES["go"],
                 project_name,
                 "main.go",
                 new_project_config["go"]["file_content"],
                 new_project_config["go"]["gitignore_content"],
                 ide_name
                 ),
            bash: (create_project,
                   PROJECTS_DIR_NAMES["bash"],
                   project_name,
                   f"{project_name}.sh",
                   new_project_config["bash"]["file_content"],
                   new_project_config["bash"]["gitignore_content"],
                   ide_name
                   ),
            cpp: (create_project,
                  PROJECTS_DIR_NAMES["cpp"],
                  project_name,
                  "main.cpp",
                  new_project_config["cpp"]["file_content"],
                  new_project_config["cpp"]["gitignore_content"],
                  ide_name
                  ),
            clang: (create_project,
                    PROJECTS_DIR_NAMES["c_lang"],
                    project_name,
                    "main.c",
                    new_project_config["c_lang"]["file_content"],
                    new_project_config["c_lang"]["gitignore_content"],
                    ide_name
                    ),
            php: (create_project,
                  PROJECTS_DIR_NAMES["php"],
                  project_name,
                  "index.php",
                  new_project_config["php"]["file_content"],
                  new_project_config["php"]["gitignore_content"],
                  ide_name
                  ),
            lua: (create_project,
                  PROJECTS_DIR_NAMES["lua"],
                  project_name,
                  "main.lua",
                  new_project_config["lua"]["file_content"],
                  new_project_config["lua"]["gitignore_content"],
                  ide_name
                  ),
            rust: (create_project_with_commands,
                   PROJECTS_DIR_NAMES["rust"],
                   project_name,
                   ide_name
                   ),
            ruby: (create_project_with_commands,
                   PROJECTS_DIR_NAMES["ruby"],
                   project_name,
                   ide_name
                   ),
            ocaml: (create_project_with_commands,
                    PROJECTS_DIR_NAMES["ocaml"],
                    project_name,
                    ide_name
                    ),
            vlang: (create_project_with_commands,
                    PROJECTS_DIR_NAMES["vlang"],
                    project_name,
                    ide_name),
            web: (create_web_project,
                  PROJECTS_DIR_NAMES["web"],
                  project_name,
                  new_project_config["web"]["html_file_content"],
                  new_project_config["web"]["css_file_content"],
                  new_project_config["web"]["javascript_file_content"],
                  new_project_config["web"]["gitignore_content"],
                  ide_name
                  )
        }

        for flag, func_and_proj_info in project_mapping.items():
            if flag:
                create_func, *args = func_and_proj_info
                create_func(*args)
                break
        else:
            console.print("[bold red]No option provided[/bold red]")


def main():
    typer.run(handle)


if __name__ == "__main__":
    main()
