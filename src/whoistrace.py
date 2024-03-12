from Trace import Trace
from Whois import Whois
import argparse
import prettytable


def main():
    parser = argparse.ArgumentParser(prog='whoistrace',
                                     description='Trace to IP and do Whois for each participant IP in trace path.',
                                     epilog='WARNING! Use at your own risk')
    parser.add_argument('dst_ip', type=str, help='Destination IP address')
    args = parser.parse_args()

    table = prettytable.PrettyTable()
    table.field_names = ['IP', 'AS', 'Country', 'Description']

    trace = Trace(args.dst_ip).trace()
    whois = Whois().get_info_list_ip(trace)

    for ip, descr in whois.items():
        table.add_row([ip, descr['AS'], descr['Country'], descr['Description']])

    print(table)


if __name__ == "__main__":
    main()
