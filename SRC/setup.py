#!/usr/bin/env python
from setuptools import setup

setup(name='moodmusic',
version='1.0', 
description='CompE Stub Library', 
author= 'Anthony Lam and Sally Kim', 
author_email = 'al4995@nyu.edu and ek2777@nyu.edu',
py_modules=['moodmusic'],
install_requires=['pyserial']
)


#Template taken from lecture 8 slides: Writing a Software Library for a HAT
#https://newclasses.nyu.edu/access/lessonbuilder/item/29117559/group/3947d0f1-ec3b-401f-86fb-388be6a711b3/Lessons/8:%20Software%20library/Software%20library.pdf
