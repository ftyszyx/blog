#coding: utf-8
from numpy import *
from os import listdir
import  operator
from collections import Counter

def file2matrix(filename):
    fr=open(filename)

