#!/bin/bash
# Только для пользователей линукса/хостинга
# Цвета
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--- Maten Userbot Installer ---${NC}"

# 1. Проверяем Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}[!] Git не установлен. Ставлю...${NC}"
    # Пытаемся поставить (для Debian/Ubuntu/Arch)
    sudo apt update && sudo apt install git -y
fi

# 2. Скачиваем проект, если мы не в нем
if [ ! -d ".git" ]; then
    echo -e "[*] Клонирование репозитория Maten..."
    git clone https://github.com/darklord-end/Maten.git
    cd Maten || exit
else
    echo -e "[*] Проект уже скачан, проверяю обновления..."
    git pull origin main
fi

# 3. Ищем Python 3.14
if command -v python3.14 &> /dev/null; then
    PYTHON_BIN="python3.14"
else
    PYTHON_BIN="python3"
    echo -e "${RED}[!] Использую стандартный python3 (рекомендуется 3.14)${NC}"
fi

# 4. Создаем окружение
if [ ! -d ".venv" ]; then
    echo -e "[*] Создание окружения .venv..."
    $PYTHON_BIN -m venv .venv
fi

# 5. Ставим зависимости
echo -e "[*] Установка либ..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. Запускаем твой setup.py
if [ -f "setup.py" ]; then
    echo -e "${GREEN}[+] Запуск настройки базы данных и конфига...${NC}"
    python setup.py
else
    echo -e "${RED}[!] setup.py не найден. Создай его для настройки токенов!${NC}"
fi

echo -e "\n${GREEN}[✅] Maten готов к работе!${NC}"
echo -e "Запуск: ${CYAN}source .venv/bin/activate && python main.py${NC}"