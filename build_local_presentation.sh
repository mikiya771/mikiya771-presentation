#!/bin/bash
set -eoux
npx @marp-team/marp-cli@latest lambda-archs/lambda_local.md -o lambda-archs/lambda_local.html --theme marp-themes/ord.css --html
npx @marp-team/marp-cli@latest docker/docker-tips/docker-tips.md -o docker/docker-tips/docker-tips.html --html
