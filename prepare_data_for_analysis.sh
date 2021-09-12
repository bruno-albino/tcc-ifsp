#!/bin/sh

echo "Checking if a virtual environment is active."

INVENV=$(python -c 'import sys; print(0 if sys.prefix == sys.base_prefix else 1)')

if [ $INVENV -eq 1 ]; then
  echo "Virtual environment detected! Proceeding..."
elif [ -f 'env/bin/activate' ]; then
  echo "Trying to activating environment..."
  source ,/bin/activate
  echo "Proceeding..."
else
  echo "Cannot run 'env/bin/activate'."
  echo "Please activate or create your virtual environment."
  exit 1
fi

python -m src.processing --cache
