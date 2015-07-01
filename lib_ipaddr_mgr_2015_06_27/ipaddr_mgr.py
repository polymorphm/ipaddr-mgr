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

import socket

class MathNet:
    math_addr_limit = None
    math_addr = None
    math_net_len = None

def math_net_assert(math_net):
    assert isinstance(math_net, MathNet)
    assert math_net.math_addr_limit is not None
    assert math_net.math_addr is not None
    assert math_net.math_net_len is not None

def math_net_list_assert(math_net_list):
    for math_net in math_net_list:
        math_net_assert(math_net)

def user_to_math_net(user_net):
    assert isinstance(user_net, str)
    
    user_net_split = user_net.rsplit(sep='/', maxsplit=1)
    
    net_addr = user_net_split[0]
    
    if len(user_net_split) >= 2:
        net_bits = int(user_net_split[1])
    else:
        net_bits = None
    
    try:
        net_addr_n = socket.inet_pton(socket.AF_INET6, net_addr)
    except (OSError, ValueError) as e:
        try:
            net_addr_n = socket.inet_pton(socket.AF_INET, net_addr)
        except (OSError, ValueError):
            raise e
    
    math_net = MathNet()
    
    math_net.math_addr_limit = 2 ** (len(net_addr_n) * 8)
    
    if net_bits is None:
        net_bits = len(net_addr_n) * 8
    
    math_net.math_net_len = 2 ** (len(net_addr_n) * 8 - net_bits)
    
    if math_net.math_net_len < 1:
        math_net.math_net_len = 1
    
    math_net.math_addr = 0
    
    for b in net_addr_n:
        math_net.math_addr = math_net.math_addr * 256 + b
    
    math_net.math_addr = math_net.math_addr // math_net.math_net_len * math_net.math_net_len
    
    return math_net

def math_to_user_net(math_net):
    math_net_assert(math_net)
    
    net_addr_n_list = []
    
    math_addr_limit = math_net.math_addr_limit
    math_addr = math_net.math_addr
    
    while math_addr_limit >= 256:
        b = math_addr % 256
        
        net_addr_n_list.insert(0, b)
        
        math_addr_limit //= 256
        math_addr //= 256
    
    net_addr_n = bytes(net_addr_n_list)
    
    try:
        net_addr = socket.inet_ntop(socket.AF_INET6, net_addr_n)
    except (OSError, ValueError) as e:
        try:
            net_addr = socket.inet_ntop(socket.AF_INET, net_addr_n)
        except (OSError, ValueError):
            raise e
    
    if math_net.math_net_len > 1:
        net_bits = len(net_addr_n) * 8
        
        while \
                net_bits > 0 and \
                math_net.math_net_len > 2 ** (len(net_addr_n) * 8 - net_bits):
            net_bits -= 1
        
        user_net = '{}/{}'.format(net_addr, net_bits)
    else:
        user_net = net_addr
    
    return user_net

def user_to_math_net_list(user_net_list):
    return tuple(user_to_math_net(user_net) for user_net in user_net_list)

def math_to_user_net_list(math_net_list):
    return tuple(math_to_user_net(math_net) for math_net in math_net_list)

def calculate(add_math_net_list, sub_math_net_list):
    math_net_list_assert(add_math_net_list)
    math_net_list_assert(sub_math_net_list)
    
    res_math_net_list = []
    add_math_net_list = list(add_math_net_list)
    del_math_net_list = []
    
    while add_math_net_list or del_math_net_list:
        for del_math_net in del_math_net_list:
            res_math_net_list.remove(del_math_net)
        del_math_net_list.clear()
        res_math_net_list.extend(add_math_net_list)
        add_math_net_list.clear()
        
        for a_math_net in res_math_net_list:
            for b_math_net in sub_math_net_list:
                if \
                        a_math_net in del_math_net_list or \
                        a_math_net.math_addr_limit != b_math_net.math_addr_limit:
                    continue
                
                if \
                        a_math_net.math_addr <= b_math_net.math_addr and \
                        b_math_net.math_addr < a_math_net.math_addr + a_math_net.math_net_len:
                    del_math_net_list.append(a_math_net)
                    
                    if a_math_net.math_addr < b_math_net.math_addr:
                        res_math_net = MathNet()
                        res_math_net.math_addr_limit = a_math_net.math_addr_limit
                        res_math_net.math_addr = a_math_net.math_addr
                        res_math_net.math_net_len = \
                                b_math_net.math_addr - a_math_net.math_addr
                        
                        add_math_net_list.append(res_math_net)
                    
                    if a_math_net.math_addr + a_math_net.math_net_len > b_math_net.math_addr + b_math_net.math_net_len:
                        res_math_net = MathNet()
                        res_math_net.math_addr_limit = a_math_net.math_addr_limit
                        res_math_net.math_addr = b_math_net.math_addr + b_math_net.math_net_len
                        res_math_net.math_net_len = \
                                (a_math_net.math_addr + a_math_net.math_net_len) - (b_math_net.math_addr + b_math_net.math_net_len)
                        
                        add_math_net_list.append(res_math_net)
                elif \
                        b_math_net.math_addr < a_math_net.math_addr and \
                        a_math_net.math_addr < b_math_net.math_addr + b_math_net.math_net_len:
                    del_math_net_list.append(a_math_net)
                    
                    res_math_net = MathNet()
                    res_math_net.math_addr_limit = a_math_net.math_addr_limit
                    res_math_net.math_addr = b_math_net.math_addr + b_math_net.math_net_len
                    res_math_net.math_net_len = (a_math_net.math_addr + a_math_net.math_net_len) - (b_math_net.math_addr + b_math_net.math_net_len)
                    
                    add_math_net_list.append(res_math_net)
    
    return tuple(res_math_net_list)

def merge_optimize(math_net_list):
    math_net_list_assert(math_net_list)
    
    res_math_net_list = []
    add_math_net_list = list(math_net_list)
    del_math_net_list = []
    
    while add_math_net_list or del_math_net_list:
        for del_math_net in del_math_net_list:
            res_math_net_list.remove(del_math_net)
        del_math_net_list.clear()
        res_math_net_list.extend(add_math_net_list)
        add_math_net_list.clear()
        
        for a_math_net in res_math_net_list:
            for b_math_net in res_math_net_list:
                if \
                        a_math_net is b_math_net or \
                        a_math_net in del_math_net_list or \
                        b_math_net in del_math_net_list or \
                        a_math_net.math_addr_limit != b_math_net.math_addr_limit or \
                        a_math_net.math_addr > b_math_net.math_addr or \
                        b_math_net.math_addr > a_math_net.math_addr + a_math_net.math_net_len:
                    continue
                
                add_math_net = MathNet()
                add_math_net.math_addr_limit = a_math_net.math_addr_limit
                add_math_net.math_addr = a_math_net.math_addr
                add_math_net.math_net_len = max(
                    a_math_net.math_net_len,
                    b_math_net.math_addr - a_math_net.math_addr + b_math_net.math_net_len,
                )
                
                del_math_net_list.append(a_math_net)
                del_math_net_list.append(b_math_net)
                add_math_net_list.append(add_math_net)
    
    return tuple(res_math_net_list)

def split_optimize(math_net_list):
    math_net_list_assert(math_net_list)
    
    queue_math_net_list = list(math_net_list)
    res_math_net_list = []
    
    while queue_math_net_list:
        curr_queue_math_net_list = queue_math_net_list
        queue_math_net_list = []
        
        for math_net in curr_queue_math_net_list:
            res_math_net_len = 1
            
            while \
                    res_math_net_len * 2 <= math_net.math_net_len \
                    and \
                    math_net.math_addr // (res_math_net_len * 2) * (res_math_net_len * 2) == math_net.math_addr:
                res_math_net_len *= 2
            
            if res_math_net_len == math_net.math_net_len:
                res_math_net_list.append(math_net)
                
                continue
            
            assert res_math_net_len < math_net.math_net_len
            
            a_math_net = MathNet()
            a_math_net.math_addr_limit = math_net.math_addr_limit
            a_math_net.math_addr = math_net.math_addr
            a_math_net.math_net_len = res_math_net_len
            
            b_math_net = MathNet()
            b_math_net.math_addr_limit = math_net.math_addr_limit
            b_math_net.math_addr = math_net.math_addr + res_math_net_len
            b_math_net.math_net_len = math_net.math_net_len - res_math_net_len
            
            res_math_net_list.append(a_math_net)
            queue_math_net_list.append(b_math_net)
    
    return tuple(res_math_net_list)

def sort_optimize(math_net_list):
    math_net_list_assert(math_net_list)
    
    res_math_net_list = sorted(math_net_list, key=lambda math_net: math_net.math_addr)
    
    return tuple(res_math_net_list)

def optimize(math_net_list):
    math_net_list = merge_optimize(math_net_list)
    math_net_list = split_optimize(math_net_list)
    math_net_list = sort_optimize(math_net_list)
    
    return math_net_list
