# -*- mode: python; coding: utf-8 -*-
#
# Copyright (c) 2015 Andrej Antonov <polymorphm@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

assert str is not bytes

import argparse
from . import ipaddr_mgr

def subnet_argument(val):
    if val is None:
        return ()
    
    assert isinstance(val, str)
    
    return tuple(val.split())

def main():
    parser = argparse.ArgumentParser(
        description='calculator for add or subtract IPv6\IPv4 subnetwork addresses'
    )
    parser.add_argument(
        'add_nets',
        metavar='ADDING-SUBNETWORKS',
        nargs='?',
        help='IPv6\IPv4 subnetwork addresses (space separated) for calculation operation add',
    )
    parser.add_argument(
        'sub_nets',
        metavar='SUBTRACTING-SUBNETWORKS',
        nargs='?',
        help='IPv6\IPv4 subnetwork addresses (space separated) for calculation operation subtract',
    )
    
    args = parser.parse_args()
    
    add_user_net_list = subnet_argument(args.add_nets)
    sub_user_net_list = subnet_argument(args.sub_nets)
    
    add_math_net_list = ipaddr_mgr.user_to_math_net_list(add_user_net_list)
    sub_math_net_list = ipaddr_mgr.user_to_math_net_list(sub_user_net_list)
    
    raw_res_math_net_list = ipaddr_mgr.calculate(add_math_net_list, sub_math_net_list)
    res_math_net_list = ipaddr_mgr.optimize(raw_res_math_net_list)
    
    res_user_net_list = ipaddr_mgr.math_to_user_net_list(res_math_net_list)
    
    print('\n'.join(res_user_net_list))
