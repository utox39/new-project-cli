#!/bin/bash

CMD_EXIT_STATUS=$?

if [ -f /usr/local/bin/newproject ]; then
  echo "newproject is already installed"
  exit 0
fi

if [ -f ./requirements.txt ]; then
    # installing requirements.txt
    if [ $CMD_EXIT_STATUS -eq 0 ] && command -v pip3; then
      pip3 install -r requirements.txt
    else
      exit 1
    fi

    # creating new_project_cli_tool config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      mkdir ~/.config/newproject
    else
      exit 1
    fi

    # copying config file in config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./newproject_config.json ]; then
          cp ./newproject_config.json ~/.config/newproject/newproject_config.json
      else
          echo "Could not copy newproject_config.json file"
      fi
    fi

    # making new project.py executable and copying it into the bin folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./newproject.py ]; then
          cp ./newproject.py newproject
          chmod +x ./newproject
          sudo mv ./newproject /usr/local/bin/newproject
      else
          echo "Could not install newproject"
      fi
    fi

    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      echo "Installation completed successfully"
    fi

else
    echo "Could not find requirements.txt file"
    exit 1
fi
