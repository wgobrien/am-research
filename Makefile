ROOT_DIR:=(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
REQUIREMENTS=requirements.txt
# Detects which OS is being used
# Only relevant for virtual environment creation
ifeq ($(OS), Windows_NT)
	SYSTEM_PYTHON=py
else
	SYSTEM_PYTHON=python3
endif

SRC_ROOT=src
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
	@echo "====================================================================================== "
	@echo "                                                                                       "
	@echo "  ______     ___      .______       __       _______ .___________.  ______   .__   __. "
	@echo " /      |   /   \     |   _  \     |  |     |   ____||           | /  __  \  |  \ |  | "
	@echo "|  ,----'  /  ^  \    |  |_)  |    |  |     |  |__   \`---|  |----\`|  |  |  | |   \|  | "
	@echo "|  |      /  /_\  \   |      /     |  |     |   __|      |  |     |  |  |  | |  . \`  | "
	@echo "|  \`----./  _____  \  |  |\  \----.|  \`----.|  |____     |  |     |  \`--'  | |  |\   | "
	@echo " \______/__/     \__\ | _| \`._____||_______||_______|    |__|      \______/  |__| \__| "
	@echo "                                                                                       "
	@echo " __          ___      .______                                                          "
	@echo "|  |        /   \     |   _  \                                                         "
	@echo "|  |       /  ^  \    |  |_)  |                                                        "
	@echo "|  |      /  /_\  \   |   _  <                                                         "
	@echo "|  \`----./  _____  \  |  |_)  |                                                        "
	@echo "|_______/__/     \__\ |______/                                                         "
	@echo "                                                                                       "
	@echo "     ___      .___  ___.                    ___       __                               "
	@echo "    /   \     |   \/   |      ___          /   \     |  |                              "
	@echo "   /  ^  \    |  \  /  |     ( _ )        /  ^  \    |  |                              "
	@echo "  /  /_\  \   |  |\/|  |     / _ \/\     /  /_\  \   |  |                              "
	@echo " /  _____  \  |  |  |  |    | (_>  <    /  _____  \  |  |                              "
	@echo "/__/     \__\ |__|  |__|     \___/\/   /__/     \__\ |__|                              "
	@echo "                                                                                       "
	@echo "                                                                                       "
	@echo "====================================================================================== "


uninstall:
	@echo "Uninstalling package from the system"
	$(VENV_PIP) uninstall am-research
	@rm -rf env
	@echo "Succesfully uninstalled am-research"

.PHONY: pipe-test
pipe-test: fetch prep train infer

.PHONY: test
test: train infer

.PHONY: fetch
fetch:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/fetch_data.py

.PHONY: prep
prep:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/prep_data.py

.PHONY: train
train:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/train.py

.PHONY: infer
infer:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/inference.py

.PHONY: clean
clean:
	@$(RM) ./models/*
	@echo "deleting binary files"