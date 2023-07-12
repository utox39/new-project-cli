# new-project-cli

[![asciicast](https://asciinema.org/a/Qf5FmiHBwkqpQCm6CDrEIMKEu.svg)](https://asciinema.org/a/Qf5FmiHBwkqpQCm6CDrEIMKEu)

## Description

Create a new project from the terminal.

This tool will help you create a minimal structure for your new project.

You can create new:

- python projects
- java projects
- go projects
- bash projects
- cpp projects
- clang projects
- rust projects
- ruby projects
- non-specific projects

and open them in:

- Visual Studio Code
- PyCharm
- IntelliJ IDEA

#### Default development directories tree

```
$HOME
└──Developer
   └── projects
       ├── bash_projects
       ├── c_projects 
       ├── cpp_projects 
       ├── go_projects
       ├── java_projects
       ├── non_specific_projects
       ├── python_projects
       └── rust_projects 
```

#### Rust projects

To create a new rust project, newproject use the following command:

```console
$ cargo new project_name
```

So it use the default command to create a new cargo package

## Requirements

#### To create a rust projects

- [Rust](https://www.rust-lang.org/learn/get-started)

#### To create a ruby projects

- [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
- [bundler](https://rubygems.org/gems/bundler)

## Installation

Easy as you can see here:

#### macOS / Linux:

```console
$ cd path/to/this/repo
$ ./install.sh
```

#### Windows:

Run as administrator

```console
$ cd path\to\this\repo
$ .\install.ps1
```

## Usage

### Create a new python project

```console
$ newproject --python project_name
```

### Create a non-specific project

```console
$ newproject --none project_name
```

### Create a new project and open it in Visual Studio Code

ATTENTION: In order to open the new project in your favorite IDE you need to have the shell command

```console
$ newproject --code --python project_name
```

### Customize the Development folder

In ~/.config/newproject/newproject_config.json:

```json
{
  "dev_dir": "path/to/your/development/folder"
}
```

### Customize a programming language projects folder

In ~/.config/newproject/newproject_config.json:

```json
{
  "py_projects_dir_name": "name/of/the/folder"
}
```

## Roadmap

- Improve customization
- Add more programming languages
- Add more IDE
- Improve user output and experience
- Publish this project to package managers

## Contributing

If you would like to contribute to this project just create a pull request which I will try to review as soon as
possible.