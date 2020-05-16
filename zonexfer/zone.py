import dns.query
import dns.zone
import dns.resolver
import re


def domain_lookup(domain_name):
    """ takes a domain name and returns nameserver hostnames """
    record_types = ['NS']
    ns_records = []

    for qtype in record_types:
        answer = dns.resolver.query(
            domain_name, qtype, raise_on_no_answer=False)

        if answer.rrset is not None:
            regex_search = r'\s([^\s]*?\.' + str(domain_name) + r')\.'
            m = re.findall(regex_search, str(answer.rrset))
            ns_records.extend(m)

    return ns_records


def a_record_lookup(nameserver):
    """ takes a nameserver hostname and returns IPs """
    record_types = ['A']
    nameserver_ips = []

    for qtype in record_types:
        answer = dns.resolver.query(
            nameserver, qtype, raise_on_no_answer=False)

        if answer.rrset is not None:
            regex_search = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
            m = re.findall(regex_search, str(answer.rrset))
            nameserver_ips.extend(m)

        return nameserver_ips


def zone_transfer(nameserver_ip, domain_name):
    """ takes nameserver IP and domain name and attempts a zone transfer """
    print(f'[+] dnsfunctions.zone_transfer :: Attempting transfer using',
          f'nameserver [{nameserver_ip}] and domain [{domain_name}]')

    transfer_request = dns.query.xfr(nameserver_ip, domain_name)
    zone_output = []
    try:
        z = dns.zone.from_xfr(transfer_request)
        names = z.nodes.keys()

        for n in names:
            m = re.search(r'([0-9\.]*)$', z[n].to_text(n))
            ip_address = m.group(0)
            if len(ip_address) != 0:
                print(f'[+] [{n}.{domain_name}] is at [{ip_address}]')
                zone_output.append(f'{n}.{domain_name} is at {ip_address}')

    except Exception:
        print(f'[-] dnsfunctions.zone_transfer :: A DNS Zone transfer',
              f'is not possible for [{nameserver_ip}] at [{domain_name}]')

    finally:
        return zone_output
