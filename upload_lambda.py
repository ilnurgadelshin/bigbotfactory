#!/usr/bin/python

from optparse import OptionParser
import json
import os

def upload_lambda(lambda_name, options):
    handler_path = 'aws_lambdas.' + lambda_name + '.index'
    if options.handler_path is not None:
        handler_path = options.handler_path

    lambda_starter = 'lambda_starter'

    if os.path.exists(lambda_starter + '.py'):
        raise Exception(lambda_starter + '.py already exists, Cannot override')
    f = open(lambda_starter + '.py', 'w')
    print >> f, 'from ' + handler_path + ' import lambda_handler as lambda_handler' + '\n'
    f.close()

    json_config = json.loads(open(options.config).read())

    json_config['name'] = lambda_name + "__" + options.api_version
    if options.description is not None:
        json_config['description'] = options.description
    json_config['handler'] = 'lambda_starter.lambda_handler'
    if not isinstance(json_config['requirements'], list):
        raise Exception('requirement must be a list')
    for line in open(options.requirements):
        json_config['requirements'].append(line.strip())
    print json_config

    final_config = 'lambda.json'
    if os.path.exists(final_config):
        raise Exception(final_config + ' already exists, Cannot override')
    f = open(final_config, 'w')
    print >> f, json.dumps(json_config)
    f.close()

    os.system('lambda-uploader')
    os.system('rm -f ' + lambda_starter + '.py')
    os.system('rm -f ' + final_config)


def main():
    parser = OptionParser()
    parser.add_option("-c", "--config", help="default config filename", default="default_lambda_config.json")
    parser.add_option("--handler-path", help="full path to lambda handler", default=None)
    parser.add_option("-d", "--description", help="lambda description", default=None)
    parser.add_option("-r", "--requirements", help="file with requirements", default='requirements.txt')
    parser.add_option("-v", "--api-version", help="api version, use prod for production deployment", default="beta")
    parser.add_option("-a", "--all", action="store_true", help="upload all lambdas", default=False)

    (options, args) = parser.parse_args()

    lambdas = []
    if options.all:
        lambdas_dir = "aws_lambdas"
        lambdas.extend([o for o in os.listdir(lambdas_dir) if os.path.isdir(os.path.join(lambdas_dir, o))])
    else:
        lambdas.append(args[0])

    for l in lambdas:
        upload_lambda(l, options)


if __name__ == '__main__':
    main()
