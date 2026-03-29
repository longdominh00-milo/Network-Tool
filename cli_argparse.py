#!/usr/bin/python3.6
import argparse
import sys

def get_list_from_arg(arg_phrase):
    #Funtion get arg_phrase from input
    i = 0
    list_value = []
    for i in range(0, len(arg_phrase)):
        if ',' in arg_phrase[i]:  # If value like ['10.10.10.10,1.1.1.1']
            list = arg_phrase[i].split(',')
            for ip in list:
                list_value.append(ip)
        else:
            list_value.append(arg_phrase[i])
        i += 1
    return list_value


def cli_arguments():
    #Funtion with argparse and return all input result from user
    dict_cli_arg = {
        'dest': '',
        'option': '',
        'source': [],
        'count': '',
        'interval': '',
        'display': '',
    }
    #parser = argparse.ArgumentParser()
    #MTR using ICMP while traceroute is using UDP
    parser = argparse.ArgumentParser(prog='test_route',
                                     usage='%(prog)s <dest ip> [-mtr]|[-ping] [optional arguments]')
    parser.add_argument('dest', metavar="[Dest IP]",
                        help='Destination IP address')
    parser.add_argument('-mtr', action="store_true",
                        help='Option mtr/traceroute (default export report, and ICMP echo request)')
    parser.add_argument('-ping', action="store_true",
                        help='Option ping (default count:10 packets, interval:0.02s)')
    parser.add_argument('-s', '--source', metavar='', nargs='+',
                        help="Source IP address (default 101.53.2.0/24) with fotmat: iptp-sgp (IPTP SGN), iptp-hkg (IPTP HongKong), ntt-hkg, pccwg-sgp (PCCW-Full), pccweu-sgp (PCCW-EU), ntt-hkg, viettel-ipt, cmc-ipt, fttx-viettel, fttx-vnpt, xxx.xxx.xxx.xxx'")
    parser.add_argument('-c', '--count', metavar='', default=10,
                        help='Stop after sending count ECHO_REQUEST packets, default 20')
    parser.add_argument('-i', '--interval', metavar='', default=0.02,
                        help='Wait  interval seconds between sending each packet, default 0.02.')
    parser.add_argument('-upstream', '--upstream', action="store_true",
                        help='Ping from source test upstream (default count:10 packets, interval:0.02s)')
    parser.add_argument('-all', '--all', action="store_true",
                        help='Ping from all source (default count:20 packets, interval:0.02s)')
    parser.add_argument('-raw', '--raw', action="store_true",
                        help='Display raw text (default display table)')

    args = parser.parse_args()

    #Check and get destination ip
    dict_cli_arg['dest'] = args.dest

    #Check ping or mtr
    if args.mtr and args.ping:
        print('Error: You can only run -mtr|-ping in one sesion (default mtr)')
        sys.exit()
    elif not args.mtr and not args.ping:
        dict_cli_arg['option'] = 'mtr'
    else:
        if args.mtr:
            dict_cli_arg['option'] = 'mtr'
        if args.ping:
            dict_cli_arg['option'] = 'ping'

    #Check and get source IP
    if (args.source and args.all) or (args.source and args.upstream) or (args.all and args.upstream):
        print('Error: You can only run -s|-all|-upstream in one session')
        sys.exit()
    elif args.source:
        list_source = get_list_from_arg(args.source)
        dict_cli_arg['source'] = list_source
    elif args.all:
        dict_cli_arg['source'] = 'all'
    elif args.upstream:
        dict_cli_arg['source'] = 'upstream'
    else:
        dict_cli_arg['source'] = ['101.53.2.0']
    #Get count packets
    dict_cli_arg['count'] = args.count
    #Get interval time
    dict_cli_arg['interval'] = args.interval
    #Get display option
    if args.raw:
        dict_cli_arg['display'] = 'raw'

    return dict_cli_arg

if __name__ == "__main__":
    dict_arg = cli_arguments()

    print (dict_arg)