#!/bin/sh -e

## Jacob Chesley
##
## Control of GPIO17 for solenoid valve
## Proof of concept and command reference
## Last Updated: 1/25/19

PIN=0

gpio mode $PIN out


gpio write $PIN 1
sleep 0.5
gpio write $PIN 0
sleep 0.5