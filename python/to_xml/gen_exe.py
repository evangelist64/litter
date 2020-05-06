# -*- coding: gbk -*-
from distutils.core import setup
import py2exe
import sys,os

os.chdir(os.path.dirname(sys.argv[0]))

setup(
    version = "1.0.0",   
    description = "format xlsx",   
    name = "fmt_xlsx",      
    console=["format_xlsx.py"],
    )
