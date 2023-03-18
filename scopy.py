#!/usr/bin/env python3

import tldextract
import argparse
import sys

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
END = "\033[0m"

def extract_url_components(url, mode):
    parsed_url = tldextract.extract(url)
    return parsed_url.subdomain + '.' + parsed_url.registered_domain if mode == 'fqdn' else parsed_url.domain + '.' + parsed_url.suffix

def get_scope(scope_file, mode='wildcard'):
    try:
        with open(scope_file, 'r') as f:
            scope_input = f.read().splitlines()
    except:
        print(f'{RED}[!]{END} {BROWN}Invalid scope file specified.{END}')
        exit(3)
    return {extract_url_components(item, mode=mode) for item in scope_input}

def get_input(input_file=None):
    if input_file is None:
        if not sys.stdin.isatty():
            # if input is piped, read from standard input
            input = sys.stdin.read().splitlines()
        else:
            input = []
    else:
        try:
            with open(input_file, 'r') as f:
                input = f.read().splitlines()
        except:
            print(f'{RED}[!]{END} {BROWN}Invalid input file specified.{END}')
            exit(3)
    return input

def main():
    parser = argparse.ArgumentParser(description='Filter URLs that match your scope file.')
    parser.add_argument('-s', '--scope', required=True, help='Scope for the URLs')
    parser.add_argument('-i', '--input', help='Input file containing URLs')
    parser.add_argument('-m', '--mode', default='wildcard', help='Mode to run in (wildcard or fqdn)')
    args = parser.parse_args()
    if args.mode not in ['fqdn', 'wildcard']:
            print('Invalid mode specified. Mode must be "fqdn" or "wildcard".')
            return
    scope = get_scope(args.scope, mode=args.mode)
    urls = get_input(args.input if args.input else None)
    if len(urls) == 0:
        print(f'{RED}[!]{END} {BROWN}Input is empty.{END}')
        return
    for url in urls:
        scoped = extract_url_components(url, mode=args.mode)
        if scoped in scope:
            print(url)

if __name__ == '__main__':
    main()
