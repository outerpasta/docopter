## Synopsis

A script runner that parses scripts that use docopt and creates web forms for executing them.
Script output is shown in realtime using websockets.

Currently only python and bash are supported.

![DEMO](https://raw.githubusercontent.com/outerpasta/docopter/master/demo/Screen%20Shot%202016-02-01%20at%201.01.00%20AM.png)

## Installation
Requires python 2.7 - https://www.python.org/downloads/release/python-2710/

Install python dependencies:
```
$ cd docopter
$ pip install -r requirements.txt
```
Or use Python Virtualenv
```
$ virtualenv tmp
$ ./tmp/bin/pip install -r requirements.txt
```

Put your scripts in docopter/scripts
Don't forget, you'll have to -
```
$ chmod +x scripts/*
```
for them to work.

## Running
```
python docopter.py
```

## Caveats
- Options within bash scripts are not working yet.
- There is currently no support for docopt 'command' argument type.
- There is currently no suport for more than just simple args/options/default-options. 
Things like mutually exclusive arguments or multiple use cases aren't working yet.