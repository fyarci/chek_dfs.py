#!/usr/bin/python

"""

This nagios plug is checks Hadoop Datanodes 

__author__ = "Fatih N. YARCI"
__license__ = "GPL"
__version__ = "0.1"
__email__ = "fatih.yarci@comodo.com"
__status__ = "alpha"

"""

from sys import argv, exit
from getopt import GetoptError, getopt
from subprocess import Popen, PIPE
from re import search


OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

HUSER = "hadoop"
DFSREPORTCMD = "sudo su - %s -c 'hadoop dfsadmin -report'"


def help():
    print("help")


def get_dfs_report(huser=HUSER):
    cmd = DFSREPORTCMD % (huser)
    out = Popen('%s' % (cmd), shell=True, stdout=PIPE, stderr=None)

    return (out.stdout.read().decode("utf-8"))


def description(text):
    out = search("Datanodes[ \S+]+", text)
    parsed_data = out.group()

    return (parsed_data)


def live_nodes(text):
    out = search("Datanodes[ \S+]+", text)
    parsed_data = out.group()
    l_nodes = search("[\d]", parsed_data)
    return (l_nodes.group())


def main(argv):
    try:
        opts, args = getopt(argv, 'hw:c:', ['help', 'warning=', 'critical='])
    except GetoptError:
        help()
        exit(UNKNOWN)

    current = int(live_nodes(get_dfs_report()))
    desc = description(get_dfs_report())
    status = 'O'

    for opt, arg in opts:

        if opt in ('-h', '--help'):
            help()
            exit()

        elif opt in ('-w', '--warning'):
            w_limit = int(arg)
            if current <= w_limit:
                status = 'W'
                print "WARNING - %s" % (desc)
                exit(WARNING)

        elif opt in ('-c', '--critical'):
            c_limit = int(arg)

            if current <= c_limit:
                status = 'C'
                print "CRITICAL - %s" % (desc)
                exit(CRITICAL)

        else:
            help()
            exit(UNKNOWN)

    if status == 'O':
        print "OK - %s" % (desc)
        exit(OK)


if __name__ == '__main__':
    main(argv[1:])
