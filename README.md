# [BigBotFactory]

BigBotFactory is now open source! Take all advantages of creating your own bot constructor platform for telegram messenger.

## How to install

1. Create AWS account
2. Create lambda_basic_execution role
3. Make sure your backend server (e.g. EC2) supports https
4. Map your own damain name to your backend server
5. Replace all example.com occurrences with your own domain name
6. Configure your proxy (e.g. nginx) to proxy_pass port 443 to port some_port
7. Clone repo to your backend server and start start_balancer.py -p some_port -c config.ini
8. Configure local awscli with your local credentials
9. Install boto3 and lambda-uploader
10. Turn on dynamodb support in AWS console 
11. run lib/dynamodb/tables/makefile to create necessary dynamodb tables
12. Use result of upload_lambda.py in lambda-uploader to create necessary lambdas
13. Enjoy

## Contribution Guidelines

You are welcome to request changes and improve BigBotFactory!