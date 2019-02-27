import sys
import argparse
from ip_resolver import IPResolver
from ip_resolve_exceptions import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARPing, find IP address from given MAC address")
    parser.add_argument('-i', help="interface name", required=True)
    parser.add_argument('--target', help="target mac address", required=True)
    parser.add_argument('-n', help="Number of repeated attempts", default=2)
    args = parser.parse_args()

    target_ip = None
    cnt = 0

    try:
        ip_resolver = IPResolver(args.i)

    except WrongIFNameExcpetion as e:
        print(e)
        sys.exit(e.code)

    except NoIPAddressINFException as e:
        print(e)
        sys.exit(e.code)

    while cnt < args.n and not target_ip:
        try:
            target_ip = ip_resolver.resolve_ip(args.target)

        except InvalidMACFormatException as e:
            print(e)
            sys.exit(e.code)

        except IPAddressNotFoundException as e:
            print(str(e) + "retry...[{CNT}/{MAX}]".format(CNT=cnt+1, MAX=args.n))

        finally:
            cnt += 1

    if not target_ip:
        print("Fail to resolve IP address from {MAC}".format(MAC=args.target))
    else:
        print("Find IP : {IP} from {MAC}".format(IP=target_ip, MAC=args.target))