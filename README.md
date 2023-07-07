# new-project-cli

## Description

Create a new project from the terminal

You can create new:

- python projects
- java projects
- go projects
- bash projects
- cpp projects
- clang projects
- rust projects
- non-specific projects

## Installation

Easy as you can see here:

```console
$ cd path/to/this/repo
$ make install
```

## Usage

### Create a new python project

```console
$ new-project --python project_name
```

### Create a non-specific project

```console
$ new-project --none project_name
```

### Create a new project and open it in Visual Studio Code

```console
$ new-project --code --python project_name
```

### Customize the Development folder

In ~/.config/new_project_cli_tool/new_project_config.json:

```json
{
  "dev_dir": "path/to/your/development/folder"
}
```

### Customize a programming language projects folder

In ~/.config/new_project_cli_tool/new_project_config.json:

```json
{
  "py_projects_dir_name": "name/of/the/folder"
}
```

## Roadmap

This is my first public project and I know I can improve it so much

## Contributing

If you would like to contribute to this project just create a pull request which I will try to review as soon as
possible.