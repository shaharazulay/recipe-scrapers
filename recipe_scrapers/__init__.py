import random
import re
from requests_futures.sessions import FuturesSession
import requests
import datetime

from .allrecipes import AllRecipes
from .bbcfood import BBCFood
from .bbcgoodfood import BBCGoodFood
from .bonappetit import BonAppetit
from .budgetbytes import BudgetBytes
from .closetcooking import ClosetCooking
from .cookstr import Cookstr
from .epicurious import Epicurious
from .finedininglovers import FineDiningLovers
from .foodrepublic import FoodRepublic
from .hundredandonecookbooks import HundredAndOneCookbooks
from .jamieoliver import JamieOliver
from .mybakingaddiction import MyBakingAddiction
from .paninihappy import PaniniHappy
from .realsimple import RealSimple
from .simplyrecipes import SimplyRecipes
from .steamykitchen import SteamyKitchen
from .taste import Taste
from .tastykitchen import TastyKitchen
from .thepioneerwoman import ThePioneerWoman
from .thevintagemixer import TheVintageMixer
from .twopeasandtheirpod import TwoPeasAndTheirPod
from .whatsgabycooking import WhatsGabyCooking

from ._proxy import get_proxies, get_user_agents_generator


SCRAPERS = {
    AllRecipes.host(): AllRecipes,
    BBCFood.host(): BBCFood,
    BBCGoodFood.host(): BBCGoodFood,
    BonAppetit.host(): BonAppetit,
    BudgetBytes.host(): BudgetBytes,
    ClosetCooking.host(): ClosetCooking,
    Cookstr.host(): Cookstr,
    Epicurious.host(): Epicurious,
    FineDiningLovers.host(): FineDiningLovers,
    FoodRepublic.host(): FoodRepublic,
    HundredAndOneCookbooks.host(): HundredAndOneCookbooks,
    JamieOliver.host(): JamieOliver,
    MyBakingAddiction.host(): MyBakingAddiction,
    PaniniHappy.host(): PaniniHappy,
    RealSimple.host(): RealSimple,
    SimplyRecipes.host(): SimplyRecipes,
    SteamyKitchen.host(): SteamyKitchen,
    Taste.host(): Taste,
    TastyKitchen.host(): TastyKitchen,
    ThePioneerWoman.host(): ThePioneerWoman,
    TheVintageMixer.host(): TheVintageMixer,
    TwoPeasAndTheirPod.host(): TwoPeasAndTheirPod,
    WhatsGabyCooking.host(): WhatsGabyCooking,
}

_get_headers = lambda user_agent: {
    'User-Agent': user_agent
}

_get_proxy = lambda proxy: {
    'http': proxy,
    'https': proxy
}


def url_path_to_dict(path):
    pattern = (r'^'
               r'((?P<schema>.+?)://)?'
               r'((?P<user>.+?)(:(?P<password>.*?))?@)?'
               r'(?P<host>.*?)'
               r'(:(?P<port>\d+?))?'
               r'(?P<path>/.*?)?'
               r'(?P<query>[?].*?)?'
               r'$'
               )
    regex = re.compile(pattern)
    matches = regex.match(path)
    url_dict = matches.groupdict() if matches is not None else None

    return url_dict


class AsyncScraper(object):

    def init(self, verbose=True, max_workers=10):
        self._max_workers = max_workers
        self._proxy_list = get_proxies(verbose=verbose)
        self._ua_generator = get_user_agents_generator(verbose=verbose)
        
    def get(self, url_paths, timeout=300, stream=False, use_proxy=False):
        print(datetime.datetime.now())
        url_paths = [u.replace('://www.', '://') for u in url_paths]
        session = FuturesSession(max_workers=self._max_workers)
        
        if use_proxy:
            futures = [
                session.get(
                    url,
                    headers=_get_headers(self._ua_generator.random),
                    proxies=_get_proxy(random.choice(self._proxy_list)),
                    timeout=timeout,
                    stream=stream)
                for url in url_paths]
        else:
            futures = [
                session.get(
                    url,
                    timeout=timeout,
                    stream=stream)
                for url in url_paths]

        scrapers = []
        for f, u in zip(futures, url_paths):
            try:
                r = f.result()
                s = SCRAPERS[url_path_to_dict(u)['host']](r)
            except Exception as e:
                # Tmp: add logging here of failure
                print("FAILURE: %s", e)
                s = SCRAPERS[url_path_to_dict(u)['host']](None)
            scrapers.append(s)

        session.close()
        print(datetime.datetime.now())
        return scrapers

    
__all__ = ['AsyncScraper']
