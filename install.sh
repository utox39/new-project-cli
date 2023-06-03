#!/bin/bash

UNAME=$(uname)

check_if_already_installed () {
    if [ "$UNAME" == "Linux" ]; then
        if [ -f /usr/local/bin/new-project ]; then
            echo "new-project is already installed"
            exit 0
        fi
    elif [ "$UNAME" == "Darwin" ]; then
        if [ -f ~/bin/new-project ]; then
            echo "new-project is already installed"
            exit 0
        fi
    fi
}

check_if_already_installed

if [ -f ./requirements.txt ]; then
    # installing requirements.txt
    pip3 install -r requirements.txt

    # creating new_project_cli_tool config folder
    mkdir ~/.config/new_project_cli_tool

    # copying config file in config folder
    if [ -f ././new_project_config.json ]; then
        cp ./new_project_config.json ~/.config/new_project_cli_tool/new_project_config.json
    else
        echo "Could not find new_project_config.json file"
        exit 1
    fi

    # making new project.py executable and copying it into the bin folder
    if [ -f ./new_project.py ]; then
        chmod +x ./new_project.py
        mv ./new_project.py new_project
        if [ "$UNAME" == "Linux" ]; then
            sudo cp ./new_project /usr/local/bin/new-project
        elif [ "$UNAME" == "Darwin" ]; then
            cp ./new_project ~/bin/
        fi
    else
        echo "Could not find new_project.py file"
        exit 1
    fi

    echo "Installation completed successfully"
else
    echo "Could not find requirements.txt file"
    exit 1
fi