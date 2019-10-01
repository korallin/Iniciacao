from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from pprint import pprint
from re import findall, match

url = 'https://www.tjse.jus.br/tjnet/consultas/internet/exibeIntegra.wsp?tmp.numProcesso=201740301376&tmp.dtMovimento=20170726&tmp.seqMovimento=1&tmp.codMovimento=371&tmp.tipoIntegra=2'
url2 = 'https://www.tjse.jus.br/tjnet/consultas/internet/exibeIntegra.wsp?tmp.numProcesso=201740301380&tmp.dtMovimento=20170623&tmp.seqMovimento=2&tmp.codMovimento=371&tmp.tipoIntegra=2'

req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup = soup(webpage, 'html.parser')

dados_processo = page_soup.find_all('b')
cabecalho = dict()

for dado in dados_processo:
    try:
        key = dado.text.strip().replace(':', '')
        info = dado.next_sibling.next_sibling.strip()
        cabecalho[key] = info
    except:
        pass

cabecalho['Número'] = findall('sso=[0-9]*', url)[0].replace('sso=', '')

corpo = dict()
sentenca = page_soup.find_all(
    'p', attrs={'class': 'western', 'align': 'center'})
if len(sentenca) > 0 and sentenca[0].text == 'SENTENÇA':
    corpo['SENTENÇA'] = page_soup.find_all(
        'p', attrs={'style': 'margin-bottom: 0cm;'})
else:
    cabecalho['Juiz'] = page_soup.find_all(
        'p', attrs={'style': 'font-style: normal; margin-bottom: 0.28cm;', 'align': 'justify'})[0].text

    paragrafos = page_soup.find_all(
        'p', attrs={'align': 'justify'})

    for paragrafo in paragrafos:
        if match('[IV]*\s.\s', paragrafo.text):
            key = paragrafo.text.strip()
            corpo[key] = ''
        else:
            try:
                if paragrafo.text != '\xa0':
                    corpo[key] += paragrafo.text
            except:
                pass


pprint(cabecalho)
pprint(corpo)
