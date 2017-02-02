#!/bin/sh
tmux                ;
cd ~/GoogleDrive/Programs/TCP_New          ;
sleep 1s            ;
python TCPserver.py ;
sleep 1s            ;
tmux splitw         ;
python TCPclient.py  ;