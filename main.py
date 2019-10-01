from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from pprint import pprint
from re import findall, match

urls = ['https://www.tjse.jus.br/tjnet/consultas/internet/exibeIntegra.wsp?tmp.numProcesso=201740301376&tmp.dtMovimento=20170726&tmp.seqMovimento=1&tmp.codMovimento=371&tmp.tipoIntegra=2',
        'https://www.tjse.jus.br/tjnet/consultas/internet/exibeIntegra.wsp?tmp.numProcesso=201740301380&tmp.dtMovimento=20170623&tmp.seqMovimento=2&tmp.codMovimento=371&tmp.tipoIntegra=2']


class Scrape:
    def __init__(self, url):
        self.url = url
        self.cabecalho = dict()
        self.corpo = dict()
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        self.page_soup = soup(webpage, 'html.parser')

    def getCabecalho(self):
        dados_processo = self.page_soup.find_all('b')

        for dado in dados_processo:
            try:
                key = dado.text.strip().replace(':', '')
                info = dado.next_sibling.next_sibling.strip()
                self.cabecalho[key] = info
            except:
                pass

        self.cabecalho['Número'] = findall(
            'sso=[0-9]*', self.url)[0].replace('sso=', '')
        return self.cabecalho

    def getCorpo(self):
        sentenca = self.page_soup.find_all(
            'p', attrs={'class': 'western', 'align': 'center'})
        if len(sentenca) > 0 and sentenca[0].text == 'SENTENÇA':
            self.getSetencaTipo1()
        else:
            self.getSetencaTipo2()
        return self.corpo

    def getSetencaTipo1(self):
        print('Not implemented yet.')

    def getSetencaTipo2(self):
        self.cabecalho['Juiz'] = self.page_soup.find_all(
            'p', attrs={'style': 'font-style: normal; margin-bottom: 0.28cm;', 'align': 'center'})[0].text

        paragrafos = self.page_soup.find_all(
            'p', attrs={'align': 'justify'})

        for paragrafo in paragrafos:
            if match('[IV]*\s.\s', paragrafo.text):
                key = paragrafo.text.strip()
                self.corpo[key] = ''
            else:
                try:
                    if paragrafo.text != '\xa0':
                        self.corpo[key] += paragrafo.text
                except:
                    pass
        return self.corpo


scrape = Scrape(urls[0])
pprint(scrape.getCabecalho())
pprint(scrape.getCorpo())
