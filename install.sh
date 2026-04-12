#!/bin/bash

# Цвета
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--- Maten Auto-Installer ---${NC}"

if [ ! -d ".git" ]; then
    echo -e "[*] Клонирую Maten..."
    git clone https://github.com/darklord-end/Maten.git
    cd Maten || { echo -e "${RED}Ошибка перехода!${NC}"; exit 1; }
fi


if command -v python3.14 &> /dev/null; then
    PYTHON_SYS="python3.14"
else
    PYTHON_SYS="python3"
fi

if [ ! -d ".venv" ]; then
    echo -e "[*] Создаю виртуальное окружение..."
    $PYTHON_SYS -m venv .venv
fi
VENV_PYTHON="./.venv/bin/python"
VENV_PIP="./.venv/bin/pip"

echo -e "[*] Обновляю pip и ставлю зависимости..."
$VENV_PIP install --upgrade pip
$VENV_PIP install -r requirements.txt

if [ -f "setup.py" ]; then
    echo -e "${GREEN}[+] Запускаю настройку конфигурации...${NC}"
    $VENV_PYTHON setup.py
else
    echo -e "${RED}[!] setup.py не найден!${NC}"
fi

echo -e "\n${GREEN}Всё готово!${NC}"
echo -e "Для ручного запуска: ${CYAN}source .venv/bin/activate && python main.py${NC}"