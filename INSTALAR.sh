#!/bin/bash
# Copyright (c) 2013, Miguel Paolino <mpaolino@ideal.com.uy>
# This file is part of gCuadraditos.
#
# gCuadraditos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gCuadraditos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gCuadraditos.  If not, see <http://www.gnu.org/licenses/>.

DEFAULT_INSTALL_DIR="$HOME/.gCuadraditos"

DESKTOP_FILES_PATH="$HOME/.local/share/applications"

SOURCE="${BASH_SOURCE[0]}"

# resolve $SOURCE until the file is no longer a symlink
while [ -h "$SOURCE" ]; do
	DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
	SOURCE="$(readlink "$SOURCE")"
  	# if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  	[[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

if [ "x$DEFAULT_INSTALL_DIR" = "x" ]; then
	echo -n "Ingrese directorio de instalación: "
else
	echo -n "Ingrese directorio de instalación o presione ENTER para usar la ruta por defecto [$DEFAULT_INSTALL_DIR]: "
fi
	read INSTALL_DIR_INPUT
	echo -n -e "\n"

if [ "x$INSTALL_DIR_INPUT" = "x" ]; then
	INSTALL_DIR_INPUT=$DEFAULT_INSTALL_DIR
fi

if [ -d "$INSTALL_DIR_INPUT" -a -w "$INSTALL_DIR_INPUT" ]; then
	echo -n "El directorio "$INSTALL_DIR_INPUT" ya existe, borrar directorio y realizar nueva instalación? s/[n]: "
        read -s -t 10 -n 1 ANSWER
	if [ "x$ANSWER" = "xs" -o "x$ANSWER" = "xS" ]; then
		echo "s"
		rm -fr "$INSTALL_DIR_INPUT"
	else
		echo "n"
		echo "Abortando"
		exit 1
	fi
fi

mkdir "$INSTALL_DIR_INPUT"

if [ "$?" != "0" ]; then
	echo "Abortando instalación" 
fi

ALL_FILES='aplay.py constants.py media COPYING gCuadraditos.py LEEME.txt README.md gCuadraditos lib ui.xml'

for one_file in $ALL_FILES; do
	cp -r "$DIR/$one_file" "$INSTALL_DIR_INPUT/"
	if [ "$?" != "0" ]; then 
		echo "Fallo la copia del archivo `pwd`/$one_file, abortando."
	        exit 1
	fi
done


chmod u+x "$INSTALL_DIR_INPUT/gCuadraditos"

# Install and setup desktop file with right paths
cp "$DIR/gCuadraditos.desktop" "$DESKTOP_FILES_PATH"
sed -i '/^Exec\=.*$/d' "$DESKTOP_FILES_PATH/gCuadraditos.desktop"
sed -i '/^Icon\=.*$/d' "$DESKTOP_FILES_PATH/gCuadraditos.desktop"
sed -i '/^$/d' "$DESKTOP_FILES_PATH/gCuadraditos.desktop"
echo -e "Exec=$INSTALL_DIR_INPUT/gCuadraditos" >> "$DESKTOP_FILES_PATH/gCuadraditos.desktop"
echo -e "Icon=$INSTALL_DIR_INPUT/media/activity-cuadraditos.svg" >> "$DESKTOP_FILES_PATH/gCuadraditos.desktop"

# Remove default installed path from bashrc
sed -i '/^PATH\=\$PATH:.*gCuadraditos$/d' "$HOME/.bashrc"
# Set path to binary
echo -e "\nPATH=\$PATH:$INSTALL_DIR_INPUT" >> "$HOME/.bashrc"

echo "Instalación completada. Inicie el programa desde el menú \"Sonido y Video\" o desde consola ejecutando \"$INSTALL_DIR_INPUT/gCuadraditos\""
exit 0
