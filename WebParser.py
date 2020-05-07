from bs4 import BeautifulSoup
import urllib.request


class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"

# Both these sources have different HTML formats so i need to parse them differently
# Ark throws everything into one HTML section while d20 just puts it in all different places
# Both are nightmares, I like therafim better

def PrintPageArk(URL):
        
        opener = AppURLopener()
                    
        page = opener.open(URL)
        soup = BeautifulSoup(page, "html.parser")

        content = soup.find('div', attrs={'id': 'content'})
        print(content)
        content = content.text.strip()
        content = content.replace('\n\n', '\n')
        content = content[:2000] + (content[2000:] and '..')

        return content

def PrintPageD(URL):
        
        opener = AppURLopener()
                    
        page = opener.open(URL)
        soup = BeautifulSoup(page, "html.parser")

        title = soup.find('h1')
        title = title.text.strip()

        stitle = soup.find('h4')
        stitle = stitle.text.strip()

        table = soup.find('table', attrs={'class': 'statBlock'})
        table = table.text.strip()
        table = table.replace('\n\n\n', '\r')
        table = table.replace('\n', ' ')

        desc = soup.findAll('p')
        descp = ''
        for para in desc:
                para = para.text.strip()
                if para.__contains__("Hypertext"):
                        break
                descp += '\n' + para + '\n'
        total = title + '\n' + stitle + '\n' + table + '\n' + descp
        return total
