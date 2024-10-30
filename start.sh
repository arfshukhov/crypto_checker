#!/bin/bash

docker build -t crypto_checker .

docker run -d -p 8000:8000 crypto_checker


