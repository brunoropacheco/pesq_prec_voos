#Importando bibliotecas
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from time import sleep

'''
busca_voos.py
Bruno Rodrigues Pacheco
28/09/2023

Esta versao esta fazendo o seguinte:
    - usa o selenium para navegar no gooogle flights e buscar os precos de passagens
        - o selenium precisa da aplicacao chromedriver.exe colocado em alguma pasta do path
'''

#Função para achar elementos na página
def find(driver,css):
    return driver.find_elements(By.CSS_SELECTOR, css)

#Função para preencher os campos
def write(element,text):
    element.send_keys(Keys.CONTROL, 'A')
    element.send_keys(text)
    sleep(1)

#Função para clicar em elementos da página
def click(driver,css):
    driver.find_element(By.CSS_SELECTOR, css).click()
    sleep(1)

#função para aguardar os elementos aparacerem na tela
def wait(driver,css):
    while len(driver.find_elements(By.CSS_SELECTOR, css)) <1:
        sleep(0.3)

#Programa de Controle de busca de passagens
def google_scrapy(dep, arr, dep_dt):
    #Abrir Chrome Browser e Google Flights
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('https://www.google.com/flights?hl=pt&curr=BRL#flt=')

    #Aguardar abetura da página
    wait(driver,'[type="text"]')

    #Identificar o elemento correspondente aos campos a serem preenchidos
    comboboxes = find(driver, '[role ="combobox"]') #verificando as comboboxes para achar a do tipo da passagem

    #comboboxes[0] eh a caixa de selecao do tipo de passagem: somente ida, ida e volta, etc
    comboboxes[0].click() #cclicando nela
    #sleep(0.5)
    options = find(driver, '[role ="option"]') #procando as roles options para ver as opcoes de tipo de passagem
    options[1].click() #clicando na opcao somente ida
    #sleep(0.5)
    
    inputs = find(driver, '[type="text"]')

    #Decolagem
    departure = inputs[0]
    write(departure, dep)
    click(driver,'[class="P1pPOe"]')

    #Retorno
    arrival = inputs[2]
    write(arrival,arr)
    click(driver,'[class="P1pPOe"]')

    #Data da Decolagem
    date_dep = inputs[4]
    write(date_dep, dep_dt)

    #Inciar pesquisa
    
    click(driver,'[aria-label="Pesquisar"]')
    sleep(1.5)
    click(driver,'[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 z18xM rtW97 Q74FEc dAwNDc"]')
    click(driver,'[aria-label="Pesquisar"]')

    #Aguardar processo
    wait(driver,'[class="JMc5Xc"]')

    #Armazendo informação da melhor passagem
    info = find(driver, '[class="JMc5Xc"]')[0]
    info = info.get_attribute("aria-label")[:-15]
    print(info)

    '''
    #Armazendo informação extra sobre o preço da passagem
    add_info = find(driver,'[class="frOi8 AdWm1c fVSoi"]')[0].text
    print(add_info)

     #Procurando por passagens baratas no período próximo
    tickets = [elements.text.split('\n') for elements in find(driver, '[class="mrywM"]')]
    print(tickets)
    value = tickets[0][15:-15]
    price = [float(v.replace('R$ ',"").replace('.','')) for v in value]
    min_price = min(price)

    #Interface de Saída
    print(f'Melhor voo:')
    print(info,'\n')
    print(add_info)
    print(f'\nO menor valor encontrado próximo da data foi de R${min_price}')
    '''
    #Fechando o Browser
    driver.quit()

google_scrapy("CDG", "GIG", "25/02/2024")
google_scrapy("CDG", "GIG", "26/02/2024")
google_scrapy("CDG", "GIG", "27/02/2024")