#!/bin/bash
set -e
set -x
pip install -r requirements_tests.txt
gem install sass
npm install -g less
npm install -g coffee-script
