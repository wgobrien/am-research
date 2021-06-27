ROOT_DIR:=(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
REQUIREMENTS=requirements.txt
# Detects which OS is being used
# Only relevant for virtual environment creation
ifeq ($(OS), Windows_NT)
	SYSTEM_PYTHON=py
else
	SYSTEM_PYTHON=python3
endif

VENV_ROOT=env
VENV_BIN=$(VENV_ROOT)/bin
VENV_PIP=$(VENV_BIN)/pip
VENV_PYTHON=$(VENV_BIN)/python

virtualenv:
	@echo "Making virtual environment..."
	@$(SYSTEM_PYTHON) -m venv env
	@echo "Installing all dependencies..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r $(REQUIREMENTS)

all:  uninstall install

install: virtualenv
	@echo "Installing package into the system"
	@$(VENV_PIP) install -e .
	@echo "  ______     ___      .______       __       _______ .___________.  ______   .__   __. " 
	@echo " /      |   /   \     |   _  \     |  |     |   ____||           | /  __  \  |  \ |  | " 
	@echo "|  ,----'  /  ^  \    |  |_)  |    |  |     |  |__   `---|  |----`|  |  |  | |   \|  | "
	@echo "|  |      /  /_\  \   |      /     |  |     |   __|      |  |     |  |  |  | |  . `  | " 
	@echo "|  `----./  _____  \  |  |\  \----.|  `----.|  |____     |  |     |  `--'  | |  |\   | "
	@echo " \______/__/     \__\ | _| `._____||_______||_______|    |__|      \______/  |__| \__| "
	@echo "                                                                                       "
	@echo " __          ___      .______                                                          "
	@echo "|  |        /   \     |   _  \                                                         "
	@echo "|  |       /  ^  \    |  |_)  |                                                        "
	@echo "|  |      /  /_\  \   |   _  <                                                         "
	@echo "|  `----./  _____  \  |  |_)  |                                                        "
	@echo "|_______/__/     \__\ |______/                                                         "
	@echo "                                                                                       "
	@echo "     ___      .___  ___.                    ___       __                               "
	@echo "    /   \     |   \/   |      ___          /   \     |  |                              "
	@echo "   /  ^  \    |  \  /  |     ( _ )        /  ^  \    |  |                              "
	@echo "  /  /_\  \   |  |\/|  |     / _ \/\     /  /_\  \   |  |                              "
	@echo " /  _____  \  |  |  |  |    | (_>  <    /  _____  \  |  |                              "
	@echo "/__/     \__\ |__|  |__|     \___/\/   /__/     \__\ |__|                              "


uninstall:
	@echo "Uninstalling package from the system"
	$(VENV_PIP) uninstall am-research
	@echo "Succesfully uninstalled am-research"
