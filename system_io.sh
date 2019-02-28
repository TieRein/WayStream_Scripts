#!/bin/sh

## Jacob Chesley
##
## Control of current to system through a relay using GPIO
## Called by run_system.py
## Last Updated: 2/28/19

SYSTEM=$1
COMMAND=$2

gpio mode $SYSTEM out
gpio write $SYSTEM $COMMAND