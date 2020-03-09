#!/bin/bash

process_name=$1

  if [ -z "$process_name" ];then
    echo "insert process name as parameter"
    exit 1
  fi

  ps -xo "user,pid,%cpu,%mem,cmd" | grep $process_name | grep -v grep | awk -f psgrep.awk
