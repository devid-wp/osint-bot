#!/bin/bash

echo "=== 1. Установка GNOME и базовых зависимостей ==="
# Ставим минимальный GNOME, утилиты для расширений и dconf
sudo apt update
sudo apt install -y gnome-shell gnome-session pipx dconf-cli python3-pip

echo "=== 2. Настройка среды для CLI-менеджера расширений ==="
pipx ensurepath
export PATH="$HOME/.local/bin:$PATH"
# Устанавливаем менеджер расширений
pipx install gnome-extensions-cli --include-deps

echo "=== 3. Установка расширений GNOME ==="
# Скачиваем нужные расширения
gnome-extensions-cli install dash-to-dock@micxgx.gmail.com
gnome-extensions-cli install blur-my-shell@aunetx
gnome-extensions-cli install forge@jmmaranan.com

echo "=== 4. Формирование и применение dconf-конфига ==="
# Создаем временный ini-файл со всеми параметрами (док, блюр, тайлинг, темная тема)
cat << 'EOF' > /tmp/gnome_rice.ini
[/]
enabled-extensions=['dash-to-dock@micxgx.gmail.com', 'blur-my-shell@aunetx', 'forge@jmmaranan.com', 'apps-menu@gnome-shell-extensions.gcampax.github.com', 'places-menu@gnome-shell-extensions.gcampax.github.com']

[org/gnome/shell/extensions/dash-to-dock]
dock-position='BOTTOM'
extend-height=false
dock-fixed=false
autohide=true
intellihide=true
custom-theme-shrink=true
background-opacity=0.25
transparency-mode='FIXED'
dash-max-icon-size=36
show-apps-at-top=false
show-favorites=true
show-running=true

[org/gnome/shell/extensions/blur-my-shell/panel]
blur=true
sigma=30

[org/gnome/shell/extensions/forge]
tiling-mode-enabled=true
window-gap-size=8
no-window-controls=true

[org/gnome/desktop/interface]
color-scheme='prefer-dark'
EOF

# Загружаем настройки напрямую в базу dconf
dconf load / < /tmp/gnome_rice.ini

echo "=== Установка завершена! ==="
echo "Важно: Поскольку расширения были установлены из-под Cinnamon, их активация потребует перезапуска."
echo "План действий:"
echo "1. Заверши текущий сеанс (Log Out)."
echo "2. На экране ввода пароля нажми на иконку шестеренки и выбери 'GNOME'."
echo "3. Войди в систему. Если расширения не подхватились с первого раза, открой терминал и выполни:"
echo "   gnome-extensions-cli enable dash-to-dock@micxgx.gmail.com blur-my-shell@aunetx forge@jmmaranan.com"
