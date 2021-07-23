ROOT_DIR:=(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
REQUIREMENTS=requirements.txt

VENV_ROOT=env

# Detects which OS is being used
# Only relevant for virtual environment creation
ifeq ($(OS), Windows_NT)
	SYSTEM_PYTHON=python
	VENV_BIN=$(VENV_ROOT)/Scripts
else
	SYSTEM_PYTHON=python3
	VENV_BIN=$(VENV_ROOT)/bin
endif

VENV_PIP=$(VENV_BIN)/pip3
VENV_PYTHON=$(VENV_BIN)/python
SRC_ROOT=src

virtualenv:
	@echo "Making virtual environment..."
	@$(SYSTEM_PYTHON) -m venv env
	@echo "Installing all dependencies..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r $(REQUIREMENTS)

all: uninstall install

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

.PHONY: pipeline
pipeline: fetch prep train nn infer

.PHONY: test
test: train nn infer

.PHONY: fetch
fetch:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/fetch_data.py ./data/raw/research_data.accdb interim_data
	@printf "\n"

.PHONY: prep
prep:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/prep_data.py
	@printf "\n"

.PHONY: train
train: clean
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/train.py
	@printf "\n"

.PHONY: infer
infer:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/inference.py

.PHONY: vis
vis:
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/vis.py

.PHONY: nn
nn:
	@printf "Launching tensorflow...\n"
	@$(SYSTEM_PYTHON) $(SRC_ROOT)/train_nn.py

.PHONY: clean
clean:
	@$(RM) ./models/*
	@printf "deleting prior models\n"
