#!/bin/bash

# Param validation
if [ -z "$1" ] 
    then 
        echo "No questions repository has been provided" 
        exit 1
fi

if [ -z "$2" ]
    then 
        echo "No custom logic script has been provided"
        exit 1
fi

# Get paths
PARENT_PATH=$(dirname $(dirname $(readlink -fm "$0")))

# Clean path
rm -rf "$PARENT_PATH/artifacts/"

# Make artifacts if doens;t exist
mkdir -p "$PARENT_PATH/artifacts"


# Prepare DIR
mkdir -p "$PARENT_PATH/artifacts/extra_py_files"
mkdir -p "$PARENT_PATH/artifacts/extra_py_files/questions"
mkdir -p "$PARENT_PATH/artifacts/extra_py_files/logic"
mkdir -p "$PARENT_PATH/artifacts/extra_packages"

# Copy files for addtional py files
cp -r "$PARENT_PATH/src/bootstrap" "$PARENT_PATH/artifacts/extra_py_files/bootstrap"
cp -r "$(readlink -e $1)/." "$PARENT_PATH/artifacts/extra_py_files/questions"
cp -r "$(readlink -e $2)" "$PARENT_PATH/artifacts/extra_py_files/logic/executor.py"

# Copy built packages for additional modules
cp "$PARENT_PATH/src/litedq/dist/litedq-0.2-py3-none-any.whl" "$PARENT_PATH/artifacts/extra_packages/litedq-0.2-py3-none-any.whl"

# Prepare as packages
# We'll use a custom __init__ for this one, as we need to execute everything in that package
# to bypass the need to create subpackages
cp "$PARENT_PATH/src/utils/runall.py" "$PARENT_PATH/artifacts/extra_py_files/questions/__init__.py"

# Regular init
echo "from .executor import Executor" >> "$PARENT_PATH/artifacts/extra_py_files/logic/__init__.py"


# Make zip for depencies
cd "$PARENT_PATH/artifacts/extra_py_files"
zip -q -r "../extra_py_files.zip" .

# Get value
hash=($(md5sum ../extra_py_files.zip))

# Return hash
echo "{\"hash\": \"$hash\"}"