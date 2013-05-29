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
GDIALOG=`which gdialog 2>/dev/null`
DIALOG=`which dialog 2>/dev/null`
if [ "x$GDIALOG" = "x" -a "x$DIALOG" = "x" ]; then
    echo "Abortando instalación. Ni dialog ni gdialog instalados en el sistema"
    exit 1
fi

if [ "x$DIALOG" = "x" ]; then
    DIAG="$GDIALOG"
else
    DIAG="$DIALOG --stdout"
fi

GDIAG_BGTITLE="Instalación gCuadraditos"


if [ "x$DEFAULT_INSTALL_DIR" = "x" ]; then
	INSTALL_DIR_INPUT=`$DIAG --title "$GDIAG_BGTITLE" --inputbox "Ingrese directorio de instalación para gCuadraditos" 6 100 2>&1`
else
	INSTALL_DIR_INPUT=`$DIAG --title "$GDIAG_BGTITLE" --inputbox "Ingrese directorio de instalación para gCuadraditos" 6 100 "$DEFAULT_INSTALL_DIR" 2>&1`
fi

if [ "x$INSTALL_DIR_INPUT" = "x" ]; then
    exit 1
fi

if [ -d "$INSTALL_DIR_INPUT" -a -w "$INSTALL_DIR_INPUT" ]; then
	$DIAG --title "$GDIAG_BGTITLE" --yesno "El directorio \"$INSTALL_DIR_INPUT\" ya existe, borrar directorio y realizar nueva instalación?" 5 100
	if [ "$?" = "0" ]; then
		rm -fr "$INSTALL_DIR_INPUT"
	else
		exit 1
	fi
fi

mkdir "$INSTALL_DIR_INPUT"

if [ "$?" != "0" ]; then
	$DIAG --title "$GDIAG_BGTITLE" --msgbox "No se pudo crear \"$INSTALL_DIR_INPUT\", abortando instalación" 5 100
	exit 1 
fi

ALL_FILES='aplay.py constants.py media COPYING gCuadraditos.py LEEME.txt README.md gCuadraditos lib ui.xml'

for one_file in $ALL_FILES; do
	cp -r "$DIR/$one_file" "$INSTALL_DIR_INPUT/"
	if [ "$?" != "0" ]; then 
		$DIAG --title "$GDIAG_BGTITLE" --msgbox "Fallo la copia del archivo `pwd`/$one_file, abortando instalación." 10 100
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

$DIAG --title "$GDIAG_BGTITLE" --msgbox "Instalación completada.\nInicie el programa desde el menú \"Sonido y Video\" o desde consola ejecutando \"$INSTALL_DIR_INPUT/gCuadraditos\"" 6 100
exit 0
