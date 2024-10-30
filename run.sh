#!/bin/bash

uvicorn main:app --host=$HOST --port=$PORT &
python3 -m crypto_setter.src.setter
