#!/usr/bin/env bash

cd layers/common-layer
rm -rf package.zip
zip -r package.zip python/
cd ../..

sam build