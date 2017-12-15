#!/bin/bash
BASE_DIR=$(cd `dirname $0`; pwd)
TJBOT_DIR=$BASE_DIR/../tjbot

if [ -x $TJBOT_DIR ]; then  
    cd $TJBOT_DIR/bootstrap/tests
    echo "Installing support libraries for TJBot. This may take few minutes."
    npm install > install.log 2>&1

    cd $BASE_DIR 
fi 

python3 jasper.py --debug
