# -*- coding: UTF-8 -*-
# Copyright (c) 2012, Miguel Paolino <mpaolino@ideal.com.uy>
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
from os.path import abspath, dirname, join

PROJECT_DIR = dirname(abspath(__file__))

MEDIA_PATH = join(PROJECT_DIR, "media")

sound_click = join(MEDIA_PATH, 'photoShutter.wav')
icon_file = join(MEDIA_PATH, 'gCuadraditos_icon.png')
