#!/usr/bin/env bash

aws s3 cp swagger.yaml s3://minha-carteira-bucket/api/swagger.yaml

cd layers/common-layer
pip3 install -r requirements.txt -t ./python
rm -rf package.zip
zip -r package.zip python/
cd ../..

sam build