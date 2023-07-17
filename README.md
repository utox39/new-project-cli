# new-project-cli

[![asciicast](https://asciinema.org/a/RduB1EVKNj1zp9Gw0kCbptpFZ.svg)](https://asciinema.org/a/RduB1EVKNj1zp9Gw0kCbptpFZ)

## Description

Create a new project from the terminal.

This tool will help you create a minimal structure for your new project.

You can create new:

- Bash projects
- C projects
- Cpp projects
- Dart projects
- Flutter projects
- Go projects
- Java projects
- Lua projects
- OCaml projects
- PHP projects
- Python projects
- Ruby projects
- Rust projects
- Vlang projects
- Web projects

and open them in:

- Visual Studio Code
- PyCharm
- IntelliJ IDEA

### Why this programming languages? (Yes, I know Flutter is a Framework)

I mainly based myself on the percentages reported by
[Stackoverflow's 2023 Developer Survey](https://survey.stackoverflow.co/2023/)
for the
["Programming, scripting, and markup languages"](https://survey.stackoverflow.co/2023/#section-most-popular-technologies-programming-scripting-and-markup-languages)
section, and I selected the most used languages and those
that I consider to be the most promising or interesting

### Default development directories tree

```
$HOME
└──Developer
   └── projects
       ├── bash_projects
       ├── c_projects 
       ├── cpp_projects
       ├── dart_projects
       ├── flutter_projects 
       ├── go_projects
       ├── java_projects
       ├── lua_projects
       ├── ocaml_projects
       ├── php_projects
       ├── python_projects
       ├── ruby_projects
       ├── rust_projects
       ├── vlang_projects
       └── web_projects 
```

### Projects created via commands

E.g: To create a new Rust project, newproject use the following command:

```console
$ cargo new project_name
```

So it use the default command to create a new cargo package.

The same is for Ruby, Dart, Flutter, OCaml and Vlang.

## Requirements

- [Python](https://www.python.org/)
- [pip3](https://packaging.python.org/en/latest/tutorials/installing-packages/)

#### To create a Rust projects

- [Rust](https://www.rust-lang.org/learn/get-started)

#### To create a Ruby projects

- [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
- [bundler](https://rubygems.org/gems/bundler)

#### To create a Dart projects

- [Dart](https://dart.dev/get-dart)

#### To create a Flutter projects

- [Flutter](https://docs.flutter.dev/get-started/install)

#### To create a OCaml projects

- [OCaml](https://ocaml.org/install)
- [dune](https://ocaml.org/install)

## Installation

Easy as you can see here:

#### macOS / Linux:

```console
$ cd path/to/this/repo
$ ./install.sh
```

#### Windows:

RUN AS ADMINISTRATOR

```console
$ cd path\to\this\repo
$ .\install.ps1
```

## Usage

#### Create a new python project

```console
$ newproject --python project_name
```

#### Create a new web project

```console
$ newproject --web project_name
```

This command will create a very simple web project with this structure:

```
project_name
├── README.md
├── index.html
├── scripts
│   └── index.js
└── styles
    └── style.css 
```

#### Create a new project and open it in Visual Studio Code

ATTENTION: In order to open the new project in your favorite IDE you need to have the shell command

```console
$ newproject --code --python project_name
```

### Customization

#### Customize the Development folder

In ~/.config/newproject/newproject_config.yaml:

```yaml
development_dir_path: path/to/your/development/folder/
```

E.g:

```yaml
development_dir_path: Documents/projects/
```

#### Customize a programming language projects folder

In ~/.config/newproject/newproject_config.json:

```yaml
project_folder_names:
  python_projects_dir_name: python_projects
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