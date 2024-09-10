import requests
import json
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from django.shortcuts import render
from .forms import GameForm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


def image(game_name):
    url=f'https://api.rawg.io/api/games?key=d61045af18f946fd8729ff6c7e7ad45c&search={game_name}'
    response=requests.get(url)
    if response.status_code == 200:
        games = response.json()['results']
        if games:
            game = games[0]
            image_url=game['background_image']
            return image_url
    return None


def currency(amount):
    symbol = amount[0]
    try:
        amount = float(amount.strip(symbol))
    except ValueError:
        return None
    url = 'https://v6.exchangerate-api.com/v6/aa69b25ebb9f080a4e524ebd/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('result') == 'success':
            rate = data['conversion_rates']['INR']
            converted = amount * rate
            converted = f'₹{converted:.2f}'  
            return converted
        else:
            return None
    except Exception as e:
        return None


def steam(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://store.steampowered.com/search/?term={search_query}'
        driver.get(url)
        game_elements = driver.find_elements(By.CLASS_NAME, 'title')
        game_names = [element.text for element in game_elements]
        price_elements = driver.find_elements(By.CLASS_NAME, 'discount_final_price')
        game_prices = [element.text for element in price_elements]
        game_name=game_name.upper()
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename==game_name.upper():
                return game_name.upper(),game_price,url
        return ()
    except Exception as e:
        return ()
    finally:
        driver.quit()

def greenman(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.greenmangaming.com/search?query={search_query}'
        driver.get(url)
        game_elements = driver.find_elements(By.CLASS_NAME, 'prod-name')
        game_names = [element.text for element in game_elements]
        price_elements = driver.find_elements(By.CLASS_NAME, 'current-price')
        game_prices = [element.text for element in price_elements]
        game_name=game_name.upper()
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename.upper()==game_name.upper():
                return game_name.upper(),game_price,url
    except Exception as e:
        return ()
    finally:
        driver.quit()

def gog(game_name):
    search_query = game_name.replace(' ', '+')
    url = f'https://www.gog.com/games/ajax/filtered?search={search_query}&mediaType=game'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'products' in data:
            for product in data['products']:
                name = product.get('title')
                price = product.get('price', {}).get('finalAmount')
                url=f'https://www.gog.com/en/games?query={search_query}'
                if name!=game_name.upper():
                    return ()
                if price[0]=='$':
                    price=currency(price)
                if name and price:
                    return name.upper(), price,url
        else:
            return ()
    else:
        return ()

def fanatical(game_name):
    search_query = game_name.replace(' ', '-')
    url = f'https://www.fanatical.com/en/game/{search_query}'
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")       
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        div_tag = driver.find_element(By.CLASS_NAME, 'PriceContainer__price')
        
        if div_tag:
            span_tag = div_tag.find_element(By.TAG_NAME, 'span')
            if span_tag:
                price = span_tag.text
                if price[0]=='$':
                    price=currency(price)
                    game_name=game_name.upper()
                return game_name.upper(), price,url
            else:
                return ()
        else:
            return ()
    
    except Exception as e:
        return ()
    
    finally:
        driver.quit()


def xbox(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.xbox.com/en-in/Search/Results?q={search_query}'
        driver.get(url)
        game_elements = driver.find_elements(By.CLASS_NAME, 'ProductCard-module__title___nHGIp.typography-module__xdsBody2___RNdGY')
        game_names = [element.text for element in game_elements]
        price_elements = driver.find_elements(By.CLASS_NAME, 'Price-module__boldText___1i2Li.Price-module__moreText___sNMVr.ProductCard-module__price___cs1xr')
        game_prices = [element.text for element in price_elements]
        game_name=game_name.upper()
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename==game_name.upper():
                return game_name.upper(),game_price,url
        return ()
    except Exception as e:
        return ()
    finally:
        driver.quit()

def wingamestore(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.wingamestore.com/search/?SearchWord={search_query}'
        driver.get(url)
        name_elements = driver.find_elements(By.CLASS_NAME, 'overclick.nocolor')
        price_elements = driver.find_elements(By.CLASS_NAME, 'price')
        for name_element, price_element in zip(name_elements, price_elements):
            name = name_element.get_attribute('title')
            price = price_element.find_element(By.TAG_NAME, 'em').text
            if name.upper() == game_name.upper():
                if price[0]=='$':
                    price=currency(price)
                return name.upper(),price,url
        return ()    

    except Exception as e:
        return ()
    finally:
        driver.quit() 

def humblebundle(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.humblebundle.com/store/search?search={search_query}'
        driver.get(url)
        list1=[]
        game_elements = driver.find_elements(By.CLASS_NAME, 'entity-title')
        game_names = [element.text for element in game_elements]
        price_elements = driver.find_elements(By.CLASS_NAME, 'price')
        game_prices = [element.text for element in price_elements]
        game_name=game_name.upper()
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename==game_name.upper():
                list1.append(game_name)
                list1.append(game_price)
        if not list1:
            return ()
        price = list1[1].replace('US', '').strip()
        if price[0]=='$':
            price=currency(price)
        return list1[0], price,url

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def gamestop(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)   
    try:
        search_query = game_name.replace(' ', '%20')
        url = f'https://www.gamestop.com/pc-gaming?q={search_query}&view=new'
        driver.get(url)

        data_elements = driver.find_elements(By.XPATH, "//a[@data-gtmdata]")

        for data in data_elements:
            gtmdata = data.get_attribute("data-gtmdata")
            gtmdata_dict = json.loads(gtmdata)
            name = gtmdata_dict.get("name")
            price = gtmdata_dict.get("price", {}).get("base") 
            if game_name.upper()==name.upper():
                price="$"+price
                price=currency(price)
                return name.upper(),price,url
        return ()
    except Exception as e:
        return ()
    finally:
        driver.quit()

def gamersgate(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.gamersgate.com/games/?query={search_query}'
        driver.get(url)
        
        name= driver.find_elements(By.XPATH, f"//div[contains(@class, 'catalog-item--title')]//a")
        game_names = [element.text for element in name]
        price = driver.find_elements(By.XPATH, f"//div[contains(@class, 'catalog-item--price')]//span")
        game_prices = [element.text for element in price]
        game_name=game_name.upper()
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename==game_name:
                if price[0]=='$':
                    price=currency(price)
                return game_name.upper(),game_price,url

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def epicgames(game_name):
    chrome_options = Options()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    try:
        url = f"https://www.epicgames.com/store/en-US/browse?q={game_name}"
        driver.get(url)
        game_elements = driver.find_elements(By.CSS_SELECTOR, "div.css-rgqwpc")
        names = [element.text for element in game_elements]
        price_elements = driver.find_elements(By.CSS_SELECTOR, "span.eds_1ypbntd0.eds_1ypbntdc.eds_1ypbntdk.css-12s1vua")
        game_prices = [element.text for element in price_elements]
        game_prices=game_prices[1:]
        games = list(zip(names, game_prices))
        for name,game_price in games:
            if name.upper()==game_name.upper():
                if game_price[0]=='$':
                    game_price=currency(game_price)
                return name.upper(),game_price,url
        return ()
        
    except Exception as e:
        return ()
    finally:
        driver.quit()

def dlgamer(game_name):
    chrome_options = Options()
    chrome_options.add_argument("--headless")      
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)    
    try:
        search_query = game_name.replace(' ', '+')
        url = f'https://www.dlgamer.com/us/search?keywords={search_query}'
        driver.get(url)
        name_elements = driver.find_elements(By.CLASS_NAME, 'product-card-title.product-card-link')
        price_elements = driver.find_elements(By.CLASS_NAME, 'product-card-price')
        game_names = [element.text for element in name_elements]
        game_prices = [element.text for element in price_elements]
        games = list(zip(game_names, game_prices))
        for gamename, game_price in games:
            if gamename.upper()==game_name.upper():
                if game_price[0]=='$':
                    price=currency(game_price)
                return gamename.upper(),price,url
        return ()

    except Exception as e:
        return ()
    finally:
        driver.quit()

def parallel(game_name):
    results={}

    with ThreadPoolExecutor() as executor:
        threads={
            'steam':executor.submit(steam,game_name),
            'xbox':executor.submit(xbox,game_name),
            'fanatical':executor.submit(fanatical,game_name),
            'gog':executor.submit(gog,game_name),
            'greenman':executor.submit(greenman,game_name),
            'dlgamer':executor.submit(dlgamer,game_name),
            'gamersgate':executor.submit(gamersgate,game_name),
            # 'gamestop':executor.submit(gamestop,game_name),
            'humblebundle':executor.submit(humblebundle,game_name),
            'wingamestore':executor.submit(wingamestore,game_name),
            'epicgames':executor.submit(epicgames,game_name)
        }
        for key,thread in threads.items():
            try:
                result = thread.result()
                if result:  
                    results[key] = result
            except Exception as e:
                results[key] = None
    return results
def index(request):
    result = {}
    background_image_url = None

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game_name = form.cleaned_data['name']
            result = parallel(game_name)
            background_image_url = image(game_name)

            if not any(result.values()):
                form.add_error(None, "No price information found for the specified game.")
            else:
                result = dict(sorted(result.items(), key=lambda x: float(x[1][1].strip('₹').replace(',', '').replace('+', '').strip()) if x[1] else float('inf')))
    else:
        form = GameForm()

    return render(request, 'tracker/index.html', {
        'form': form,
        'results': result,
        'background_image_url': background_image_url,
    })



