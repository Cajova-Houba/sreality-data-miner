#!/bin/bash

JAVA_HOME={{ java_home }}
PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
export JAVA_HOME
export PATH