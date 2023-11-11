#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import struct
import time
import select
import socket


def check_sum(strings):
    csum = 0
    countTo = (len(strings) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = strings[count + 1] * 256 + strings[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(strings):
        csum = csum + strings[len(strings) - 1]
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
