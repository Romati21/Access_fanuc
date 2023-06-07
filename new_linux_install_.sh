#!/bin/bash

# Обновляем систему и устанавливаем основные пакеты
sudo pacman -Syu --noconfirm
sudo pacman -S --needed --noconfirm base-devel git

# Установка AUR-хелпера yay
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si --noconfirm
cd ..
rm -rf yay

# Установка основных программ
sudo pacman -S --needed --noconfirm package1 package2 package3

# Установка библиотек
sudo pacman -S --needed --noconfirm library1 library2 library3

# Установка AUR-пакетов с помощью yay
yay -S --needed --noconfirm aur-package1 aur-package2 aur-package3

# Установка Python-пакетов с помощью pip
sudo pacman -S --needed --noconfirm python-pip
pip install package1 package2 package3

# Дополнительные настройки и установки

# Завершение скрипта
echo "Установка программ и пакетов завершена."

# В этом скрипте:

# 1.Сначала мы обновляем систему и устанавливаем основные пакеты и утилиты, включая base-devel и git.
# 2.Затем мы клонируем репозиторий AUR-хелпера yay и устанавливаем его с помощью makepkg.
# 3.Далее идет установка основных программ, библиотек и пакетов с помощью pacman.
# 4.Затем мы устанавливаем AUR-пакеты с помощью yay.
# 5.После этого мы устанавливаем Python-пакеты с помощью pip.
# 6.В разделе "Дополнительные настройки и установки" вы можете добавить дополнительные команды,
# которые вам необходимы для настройки системы или установки конкретных программ.
# 7.В конце скрипт выводит сообщение о завершении установки.

# Прежде чем запустить скрипт, убедитесь, что у вас есть права на выполнение (chmod +x script.sh),
# и адаптируйте его под свои нужды, добавив или удалив программы и пакеты, которые вам требуются.
