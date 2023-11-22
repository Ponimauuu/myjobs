#!/bin/bash
AWS_ACCESS_KEY="Your_Key"
AWS_SECRET_ACCESS_KEY="Your_Secret_Key"
DEFAULT_REGION="eu-east-1"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  if command -v apt; then
    echo "Установка AWS CLI на ваш Ubuntu"
    sudo apt install pip -y
    pip install awscli
    sudo apt update
    sudo apt install awscli -y
    aws configure set aws_access_key_id $AWS_ACCESS_KEY
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
elif command -v yum; then
    echo "Установка AWS CLI на ваш RedHat."
    sudo yum install python3-pip
    pip install awscli
    aws configure set aws_access_key_id $AWS_ACCESS_KEY
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
fi
elif [[ "$OSTYPE" == "msys" ]]; then
    msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
    aws configure set aws_access_key_id $AWS_ACCESS_KEY
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
elif [[ "$OSTYPE"=="darwin" ]]; then 
    brew install awscli
    aws configure set aws_access_key_id $AWS_ACCESS_KEY
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
else
    echo "Не поддерживается,попробуйте вручную: $OSTYPE"
fi
