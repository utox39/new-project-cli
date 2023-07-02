#!/bin/bash

CMD_EXIT_STATUS=$?

if [ -f /usr/local/bin/new-project ]; then
  echo "new-project is already installed"
  exit 0
fi

if [ -f ./requirements.txt ]; then
    # installing requirements.txt
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      pip3 install -r requirements.txt
    else
      exit 1
    fi

    # creating new_project_cli_tool config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      mkdir ~/.config/new_project_cli_tool
    else
      exit 1
    fi

    # copying config file in config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./new_project_config.json ]; then
          cp ./new_project_config.json ~/.config/new_project_cli_tool/new_project_config.json
      else
          echo "Could not find new_project_config.json file"
          exit 1
      fi
    fi

    # making new project.py executable and copying it into the bin folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./new_project.py ]; then
          cp ./new_project.py new-project
          chmod +x ./new-project
          sudo mv ./new-project /usr/local/bin/new-project
      else
          echo "Could not find new_project.py file"
          exit 1
      fi
    fi

    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      echo "Installation completed successfully"
    fi

else
    echo "Could not find requirements.txt file"
    exit 1
fi
