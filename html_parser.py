from csv import Error
import requests as req
from bs4 import BeautifulSoup
import re
from random import choice


class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def download_soup(self):
        if self.soup is None:
            res = req.get(self.url)
            self.soup = BeautifulSoup(res.text, features="html.parser")

    def get_link(self):
        if self.soup is None:
            raise Error("download soup first!!!")
        buttons = self.soup.find_all("button", class_="small-button")
        button = choice(buttons)
        onclick = button.get("onclick")
        match = re.search(r"play\('([^']+)'", onclick)
        sound_path = match.group(1)
        return "https://www.myinstants.com" + sound_path
