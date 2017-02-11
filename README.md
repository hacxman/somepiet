# Something to Piet (not yet) compiler

Will be compiler from not yet determined language into
[Piet programming language](http://www.dangermouse.net/esoteric/piet.html) by David Morgan-Mar.
It is intended to have some artistic output. Right now it's incomplete code generator, capable
of pushing a number on stack and printing it out as a number or character. It is able to
create Hello World example.

## Prerequisities
* python2.7
* ImageMagick (for resizing resulting images)

## Usage
Use `$ ./cc.py` to run it. Currently it runs just a few tests and produces png images.

Resulting images can be run in some of the Piet interpreters such as:
* [npiet](http://www.bertnase.de/npiet/) written in C
* [PietDev](http://www.rapapaing.com/blog/?page_id=6) which is web based. It can load an image and supports program stepping (which is advised so you won't freeze your tab/browser in case program loops indefinitely).

## Goals
* arty output
* complete code generator with "trampolines" for calling functions
* language parser and translator
* metaPiet and parallelPiet support (these are not yet implemented)

Copyright (C) hexo, 2017
