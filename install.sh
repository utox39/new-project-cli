#!/bin/bash

# Colors
RED='\033[0;31m'
LIGHT_GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


CMD_EXIT_STATUS=$?

if [ -f /usr/local/bin/newproject ]; then
  echo -e "${YELLOW}newproject is already installed${NC}"
  exit 0
fi

if [ -f ./requirements.txt ]; then
    # installing requirements.txt
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if command -v pip3; then
        pip3 install -r requirements.txt
      else
        echo -e "${RED}pip3 is not installed${NC}"
        echo -e "${RED}Could not install newproject${NC}"
        exit 127
      fi
    else
      echo -e "${RED}Could not install newproject${NC}"
      exit 1
    fi

    # creating new_project_cli_tool config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -d ~/.config/ ]; then
        mkdir ~/.config/newproject
      else
        echo -e "${RED}~/.config/ does not exist${NC}"
        echo -e "${RED}Could not install newproject${NC}"
        exit 2
      fi
    else
      echo -e "${RED}Could not install newproject${NC}"
      exit 1
    fi

    # copying config file in config folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./newproject_config.yaml ]; then
          cp ./newproject_config.yaml ~/.config/newproject/newproject_config.yaml
      else
          echo -e "${RED}newproject_config.yaml does not exist${NC}"
          echo -e "${RED}Could not install newproject${NC}"
          exit 2
      fi
    else
      echo -e "${RED}Could not install newproject${NC}"
      exit 1
    fi

    # making new project.py executable and copying it into the bin folder
    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      if [ -f ./newproject.py ]; then
          cp ./newproject.py newproject
          chmod +x ./newproject
          sudo mv ./newproject /usr/local/bin/newproject
      else
        echo -e "${RED}newproject.py does not exist${NC}"
        echo -e "${RED}Could not install newproject${NC}"
        exit 2
      fi
    else
      echo -e "${RED}Could not install newproject${NC}"
      exit 1
    fi

    if [ $CMD_EXIT_STATUS -eq 0 ]; then
      echo -e "${LIGHT_GREEN}Installation completed successfully${NC}"
    fi

else
    echo -e "${RED}Could not find requirements.txt file${NC}"
    echo -e "${RED}Could not install newproject${NC}"
    exit 1
fi
