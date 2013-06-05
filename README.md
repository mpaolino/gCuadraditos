Copyright (C) 2013, Miguel Paolino (http://www.ideal.com.uy)

About gCuadraditos Activity
==========================

This is a QR scanner for GNOME.


Usage
=====

This activity was developed with ease of use in mind. 

Just fire the app and point the camera to QR target and gCuadraditos will
automatically decode it. Right now it only detects two kind of data, URLs
and text.

Clicking on the detected URL will open it on the default browser, text will
be displayed in a pop up window.


Dependencies
============
This software uses the power of gstreamer, it's plugin system and zbar library
for the hard working job of decoding every captured video frame.

Since this software is intended to be used in Latin american OLPC laptops
that don't have root access for their users all binary libs required are included.

All the needed libraries are compiled for 32bits x86 and for ARMv7 archs,
so if you have a 64 bits x86 or another different one, and you want to give
it a try just make sure gstreamer0.10-plugins-bad with the zbar plugin is installed
on your system.


Authors
=======
* Miguel Paolino (mpaolino@ideal.com.uy), Uruguay


Contributors
============
* Plan Ceibal Uruguay (XO 1.5, XO 1.75, JumPC Olidata and Magalhaes test laptops)


License
=======
See COPYING file.

