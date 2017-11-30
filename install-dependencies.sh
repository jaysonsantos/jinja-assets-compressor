#!/bin/bash
set -e
set -x
which sass || gem install sass
which lessc || npm install -g less
which coffee || npm install -g coffeescript
