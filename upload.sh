#!/bin/bash

git add .
#git rm -rf __pycache__
git commit -m "$1"
git push heroku master