import os
import sched
import time
from discord_webhook import DiscordWebhook

class BaseHook:
    def __init__(self, url : str, testmode : bool = False):
        self.__url = url
        self.__testmode = testmode
        self.__scheduler = None
    @property
    def url(self):
        return self.__url
    
    @property
    def testmode(self):
        return self.__testmode
    
    @url.setter
    def url(self, url : str):
        assert isinstance(url, str), "url must be a string"
        assert url.startswith("https://discord.com/api/webhooks/"), "url must start with https://discord.com/api/webhooks/"
        self.__url = url

    @testmode.setter
    def testmode(self, testmode : bool):
        assert isinstance(testmode, bool), "testmode must be a boolean"
        self.__testmode = testmode

    def construct_content(self):
        return ""
    
    def construct_embed(self):
        return None
    
    def construct_pathes(self):
        return None

    def construct_files(self):
        return None

    def send(self, **kwargs):
        if self.__testmode:
            print(f"supposed to trigger a webhook at {time.time()} for {self.url[-10:]}")
        else:
            webhook = DiscordWebhook(url=self.url)
            embed = self.construct_embed()
            if not embed:
                content = self.construct_content()
                if content:
                    webhook.set_content(content)
            else:
                webhook.add_embed(embed)

            pathes = self.construct_pathes()
            if pathes:
                if isinstance(pathes, str):
                    pathes = [pathes]
                for path in pathes:
                    with open(path, "rb") as f:
                        webhook.add_file(f.read(), os.path.basename(path))

            files = self.construct_files()
            
            if files:
                counter = 0
                if not isinstance(files, list):
                    files = [files]
                for i, file in enumerate(files):
                    if isinstance(file, tuple):
                        webhook.add_file(file[1], file[0])
                    else:
                        webhook.add_file(file, f"file_{counter}.png")
                        counter += 1

            webhook.execute()

    def recurs(self, every : float = 5*60, _block : bool = False, _immediate : bool = True, **kwargs):
        global _scheduler_started

        if self.__scheduler:
            self.__scheduler.cancel()

        self.__scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

        if _immediate:
            self.send(**kwargs)

        def recurs_func(**kwargs):
            self.send(**kwargs)
            self.__scheduler.enter(every, 1, recurs_func, kwargs=kwargs)

        self.__scheduler.enter(every, 1, recurs_func, kwargs=kwargs)

        if _block:
            self.__scheduler.run()
        else:
            self.__scheduler.run(blocking=False)
