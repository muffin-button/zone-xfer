""" Python Flask App for performing zone transfers. Do not use this on
any systems you don't have permission to test. Provided for educational
purposes only. """
import json
import os
from flask import Flask, jsonify, request
from zonexfer.zone import domain_lookup, a_record_lookup, zone_transfer


if __name__ == '__main__':
    app = Flask(__name__)


    @app.route('/')
    def hello_world():
        user = os.environ['NAME']
        return f'Hello, {user}!'


    @app.route('/zone', methods=['POST'])
    def banana():
        print(f'main.banana :: [{request.data}]')
        dto = json.loads(request.data)
        domain_name = dto["domain"]

        nameserver_list = domain_lookup(domain_name)
        nameserver_ips = []
        zone_output = []

        for server in nameserver_list:
            ips = a_record_lookup(server)
            nameserver_ips.extend(ips)

        for ip_addr in nameserver_ips:
            results = zone_transfer(ip_addr, domain_name)
            zone_output.extend(results)

        return jsonify(zone_output)


    app.run(debug=True, host='0.0.0.0')
