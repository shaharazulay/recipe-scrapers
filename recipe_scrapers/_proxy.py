import requests
from lxml.html import fromstring
from fake_useragent import UserAgent

proxy_list_url = 'https://free-proxy-list.net/'


def get_proxies(verbose=False):

    if verbose:
        print("retriving updated proxy list...")
    url = proxy_list_url
    response = requests.get(url, verify=False)
    
    parser = fromstring(response.text)

    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if not i.xpath('.//td[7][contains(text(),"yes")]'):

            proxy = ":".join([
                i.xpath('.//td[1]/text()')[0],
                i.xpath('.//td[2]/text()')[0]])
            proxies.add('http://' + proxy)

    if verbose:
        print("Found %s avaliable proxies." % len(proxies))
    return list(proxies)


__all__ = ['get_proxies']


def get_user_agents_generator(verbose=False, verify_ssl=False):
    if verbose:
        print("retriving updated user-agent list...")

    ua = UserAgent(verify_ssl=verify_ssl)
    ua.update()

    if verbose:
        print("Done.")

    return ua


__all__ += ['get_user_agents_generator']
