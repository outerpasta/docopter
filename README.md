## Synopsis

A script runner that parses scripts that use docopt and creates web forms for executing them.
Script output is shown in realtime using websockets.

Currently only python and bash are supported.

![DEMO](https://raw.githubusercontent.com/outerpasta/docopter/master/demo/Screen%20Shot%202016-02-01%20at%2012.24.10%20AM.png)

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

## Running
```
python docopter.py
```

## Caveats
- There is currently no support for docopt 'command' argument type.
- There is currently no suport for more than just simple args/options/default-options. 
Things like mutually exclusive arguments or multiple use cases aren't working yet.