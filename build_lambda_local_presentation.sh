#!/bin/bash
set -eoux
npx @marp-team/marp-cli@latest lambda-archs/lambda_local.md -o lambda-archs/lambda_local.html --theme marp-themes/ord.css --html
