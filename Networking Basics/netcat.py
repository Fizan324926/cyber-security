# importing libraries
import imp
import socket
import argparse
import shlex
import subprocess 
import textwrap
import sys
import threading

from matplotlib import cm
from numpy import std

# function to execute command and return output
def execute(cmd):
    cmd=cmd.strip()
    if not cmd:
        return
    # subprocess to execute command on local OS using check_ouput
    # shlex is used for splitting commands in order
    output=subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)

    # return output of command
    return output.decode()
