import random
import re
from requests_futures.sessions import FuturesSession
import requests
import datetime

from .allrecipes import AllRecipes, AllRecipesUKAsia
from .bbcfood import BBCFood
from .bbcgoodfood import BBCGoodFood
from .bonappetit import BonAppetit
from .budgetbytes import BudgetBytes
from .closetcooking import ClosetCooking
from .cookstr import Cookstr
from .eatsmarter import EatSmarter
from .epicurious import Epicurious
from .finedininglovers import FineDiningLovers
from .foodrepublic import FoodRepublic
from .foodnetwork import FoodNetwork
from .hundredandonecookbooks import HundredAndOneCookbooks
from .jamieoliver import JamieOliver
from .mybakingaddiction import MyBakingAddiction
from .paninihappy import PaniniHappy
from .realsimple import RealSimple
from .seriouseats import SeriousEats
from .simplyrecipes import SimplyRecipes
from .steamykitchen import SteamyKitchen
from .taste import Taste
from .tastykitchen import TastyKitchen
from .thepioneerwoman import ThePioneerWoman
from .thevintagemixer import TheVintageMixer
from .twopeasandtheirpod import TwoPeasAndTheirPod
from .whatsgabycooking import WhatsGabyCooking

from ._proxy import get_proxies, get_user_agents_generator


SCRAPERS = {}

SCRAPERS.update(dict.fromkeys(AllRecipes.host(), AllRecipes))
SCRAPERS.update(dict.fromkeys(AllRecipesUKAsia.host(), AllRecipesUKAsia))
SCRAPERS.update(dict.fromkeys(BBCFood.host(), BBCFood))
SCRAPERS.update(dict.fromkeys(BBCGoodFood.host(), BBCGoodFood))
SCRAPERS.update(dict.fromkeys(BonAppetit.host(), BonAppetit))
SCRAPERS.update(dict.fromkeys(BudgetBytes.host(), BudgetBytes))
SCRAPERS.update(dict.fromkeys(ClosetCooking.host(), ClosetCooking))
SCRAPERS.update(dict.fromkeys(Cookstr.host(), Cookstr))
SCRAPERS.update(dict.fromkeys(EatSmarter.host(), EatSmarter))
SCRAPERS.update(dict.fromkeys(Epicurious.host(), Epicurious))
SCRAPERS.update(dict.fromkeys(FineDiningLovers.host(), FineDiningLovers))
SCRAPERS.update(dict.fromkeys(FoodRepublic.host(), FoodRepublic))
SCRAPERS.update(dict.fromkeys(FoodNetwork.host(), FoodNetwork))
SCRAPERS.update(dict.fromkeys(HundredAndOneCookbooks.host(), HundredAndOneCookbooks))
SCRAPERS.update(dict.fromkeys(JamieOliver.host(), JamieOliver))
SCRAPERS.update(dict.fromkeys(MyBakingAddiction.host(), MyBakingAddiction))
SCRAPERS.update(dict.fromkeys(PaniniHappy.host(), PaniniHappy))
SCRAPERS.update(dict.fromkeys(RealSimple.host(), RealSimple))
SCRAPERS.update(dict.fromkeys(SeriousEats.host(), SeriousEats))
SCRAPERS.update(dict.fromkeys(SimplyRecipes.host(), SimplyRecipes))
SCRAPERS.update(dict.fromkeys(SteamyKitchen.host(), SteamyKitchen))
SCRAPERS.update(dict.fromkeys(Taste.host(), Taste))
SCRAPERS.update(dict.fromkeys(TastyKitchen.host(), TastyKitchen))
SCRAPERS.update(dict.fromkeys(ThePioneerWoman.host(), ThePioneerWoman))
SCRAPERS.update(dict.fromkeys(TheVintageMixer.host(), TheVintageMixer))
SCRAPERS.update(dict.fromkeys(TwoPeasAndTheirPod.host(), TwoPeasAndTheirPod))
SCRAPERS.update(dict.fromkeys(WhatsGabyCooking.host(), WhatsGabyCooking))


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
