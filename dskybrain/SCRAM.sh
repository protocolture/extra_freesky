#!/bin/bash

kasa --type strip --host 192.168.20.148 on --index 1
sleep 2
kasa --type strip --host 192.168.20.148 off --index 0
kasa --type strip --host 192.168.20.63 off --index 0
kasa --type strip --host 192.168.20.64 off --index 0
kasa --type strip --host 192.168.20.64 off --index 1
kasa --type strip --host 192.168.20.64 off --index 2
sleep 2
kasa --type strip --host 192.168.20.148 off --index 1

