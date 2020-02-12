import requests
from bs4 import BeautifulSoup
from deadjson import Util


class Webtoon(object):

    def __init__(self):
        super(Webtoon, self).__init__()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
                          "/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 "
                          "Safari/537.36",
            "Referer": "https://www.webtoons.com/en"
        }

    def get(self, url):
        r = requests.get(url, headers=self.header)
        return r.text

    def genre(self):
        r = self.get("https://www.webtoons.com/en/genre")
        soup = BeautifulSoup(r, "lxml")
        result = soup.select("div.card_wrap.genre")
        genre = result[0].select("h2.sub_title")
        result_genre = result[0].select("ul.card_lst")
        response = {}
        for i in range(14):
            __genre = genre[i].get_text()
            response[__genre] = {}
            j = result_genre[i]
            for k in j.select("li"):
                info = k.select("div.info")[0]
                status = info.find(class_="icon_area").get_text()
                response[__genre][info.find(class_="subj").get_text()] = {
                    "url": k.find("a").get("href"),
                    "author": info.find(class_="author").get_text(),
                    "love": info.find(class_="grade_area").get_text().replace("like", ""),
                    "status": status if status else "Pending",
                }
        return Util(response)


if __name__ == '__main__':
    a = Webtoon().genre()
    print(a)
