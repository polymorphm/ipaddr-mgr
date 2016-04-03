ipaddr-mgr
==========

``ipaddr-mgr`` is a calculator for add or subtract IPv6\IPv4 subnetwork
addresses.


Status
------

Release: ipaddr-mgr-0.1.1 .


Using Example
-------------

IPv4 calculation example
========================

Getting all global IPv4-addresses except ``108.61.175.14`` and except standard
special addresses:

    $ ./ipaddr-mgr '0.0.0.0/0' '108.61.175.14 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 169.254.0.0/16 224.0.0.0/4'
    
    0.0.0.0/5
    8.0.0.0/7
    11.0.0.0/8
    12.0.0.0/6
    16.0.0.0/4
    32.0.0.0/3
    64.0.0.0/3
    96.0.0.0/5
    104.0.0.0/6
    108.0.0.0/11
    108.32.0.0/12
    108.48.0.0/13
    108.56.0.0/14
    108.60.0.0/16
    108.61.0.0/17
    108.61.128.0/19
    108.61.160.0/21
    108.61.168.0/22
    108.61.172.0/23
    108.61.174.0/24
    108.61.175.0/29
    108.61.175.8/30
    108.61.175.12/31
    108.61.175.15
    108.61.175.16/28
    108.61.175.32/27
    108.61.175.64/26
    108.61.175.128/25
    108.61.176.0/20
    108.61.192.0/18
    108.62.0.0/15
    108.64.0.0/10
    108.128.0.0/9
    109.0.0.0/8
    110.0.0.0/7
    112.0.0.0/4
    128.0.0.0/3
    160.0.0.0/5
    168.0.0.0/8
    169.0.0.0/9
    169.128.0.0/10
    169.192.0.0/11
    169.224.0.0/12
    169.240.0.0/13
    169.248.0.0/14
    169.252.0.0/15
    169.255.0.0/16
    170.0.0.0/7
    172.0.0.0/12
    172.32.0.0/11
    172.64.0.0/10
    172.128.0.0/9
    173.0.0.0/8
    174.0.0.0/7
    176.0.0.0/4
    192.0.0.0/9
    192.128.0.0/11
    192.160.0.0/13
    192.169.0.0/16
    192.170.0.0/15
    192.172.0.0/14
    192.176.0.0/12
    192.192.0.0/10
    193.0.0.0/8
    194.0.0.0/7
    196.0.0.0/6
    200.0.0.0/5
    208.0.0.0/4
    240.0.0.0/4

IPv6 calculation example
========================

Getting all global IPv6-addresses except subnet ``2001:19f0:7400:8421:4242::/80``:

    $ ./ipaddr-mgr '2000::/3' '2001:19f0:7400:8421:4242::/80'
    
    2000::/16
    2001::/20
    2001:1000::/21
    2001:1800::/24
    2001:1900::/25
    2001:1980::/26
    2001:19c0::/27
    2001:19e0::/28
    2001:19f0::/34
    2001:19f0:4000::/35
    2001:19f0:6000::/36
    2001:19f0:7000::/38
    2001:19f0:7400::/49
    2001:19f0:7400:8000::/54
    2001:19f0:7400:8400::/59
    2001:19f0:7400:8420::/64
    2001:19f0:7400:8421::/66
    2001:19f0:7400:8421:4000::/71
    2001:19f0:7400:8421:4200::/74
    2001:19f0:7400:8421:4240::/79
    2001:19f0:7400:8421:4243::/80
    2001:19f0:7400:8421:4244::/78
    2001:19f0:7400:8421:4248::/77
    2001:19f0:7400:8421:4250::/76
    2001:19f0:7400:8421:4260::/75
    2001:19f0:7400:8421:4280::/73
    2001:19f0:7400:8421:4300::/72
    2001:19f0:7400:8421:4400::/70
    2001:19f0:7400:8421:4800::/69
    2001:19f0:7400:8421:5000::/68
    2001:19f0:7400:8421:6000::/67
    2001:19f0:7400:8421:8000::/65
    2001:19f0:7400:8422::/63
    2001:19f0:7400:8424::/62
    2001:19f0:7400:8428::/61
    2001:19f0:7400:8430::/60
    2001:19f0:7400:8440::/58
    2001:19f0:7400:8480::/57
    2001:19f0:7400:8500::/56
    2001:19f0:7400:8600::/55
    2001:19f0:7400:8800::/53
    2001:19f0:7400:9000::/52
    2001:19f0:7400:a000::/51
    2001:19f0:7400:c000::/50
    2001:19f0:7401::/48
    2001:19f0:7402::/47
    2001:19f0:7404::/46
    2001:19f0:7408::/45
    2001:19f0:7410::/44
    2001:19f0:7420::/43
    2001:19f0:7440::/42
    2001:19f0:7480::/41
    2001:19f0:7500::/40
    2001:19f0:7600::/39
    2001:19f0:7800::/37
    2001:19f0:8000::/33
    2001:19f1::/32
    2001:19f2::/31
    2001:19f4::/30
    2001:19f8::/29
    2001:1a00::/23
    2001:1c00::/22
    2001:2000::/19
    2001:4000::/18
    2001:8000::/17
    2002::/15
    2004::/14
    2008::/13
    2010::/12
    2020::/11
    2040::/10
    2080::/9
    2100::/8
    2200::/7
    2400::/6
    2800::/5
    3000::/4
