#Importando bibliotecas
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from time import sleep
import pandas as pd
import re
from datetime import datetime, timedelta
import pyautogui

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
    sleep(0.5)

#Função para clicar em elementos da página
def click(driver,css):
    driver.find_element(By.CSS_SELECTOR, css).click()
    sleep(0.5)

#função para aguardar os elementos aparacerem na tela
def wait(driver,css):
    var = 0
    while (len(driver.find_elements(By.CSS_SELECTOR, css)) <1) and var < 3:
        sleep(0.3)
        var = var + 0.3
    if var > 3:
        return False
    return True

#Programa de Controle de busca de passagens
def google_scrapy(dep, arr, dep_dt, driver):
    
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
    #sleep(1.5)
    click(driver,'[class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 z18xM rtW97 Q74FEc dAwNDc"]')
    click(driver,'[aria-label="Pesquisar"]')

    #Aguardar processo
    existe = wait(driver,'[class="JMc5Xc"]')

    if existe:
        #Armazendo informação da melhor passagem
        info = find(driver, '[class="JMc5Xc"]')[0]
        info = info.get_attribute("aria-label")[:-15]
        #print(info)
        return info
    else: 
        #print('nao ha voos')
        return 'Nao ha voos'

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
    
def coloca_continente(row):
    paises_europeus = [
    'alemanha', 'austria', 'belgica', 'bosnia', 'bulgaria', 'croacia',
    'dinamarca', 'espanha', 'finlandia', 'franca', 'grecia',
    'holanda', 'hungria', 'inglaterra', 'irlanda', 'italia', 'noruega',
    'polonia', 'portugal', 'rep tcheca', 'romenia', 'russia', 'servia',
    'suecia', 'suica', 'ucrania']
    if row['pais'] in paises_europeus:
        return 'europa'

def pega_dados_resposta(string_voo):

    # Expressões regulares para extrair os valores desejados
    valor_match = re.search(r"A partir de (\d+) Reais brasileiros", string_voo)
    origem_match = re.search(r"Sai do aeroporto (.+?) às", string_voo)
    #destino_match = re.search(r"chega no aeroporto (.+?) às", string_voo)
    data_saida_match = re.search(r"(\d{2}:\d{2}) do dia (.+?) (\d+)", string_voo)
    tempo_total_match = re.search(r"Duração total: (.+?)\. Parada", string_voo)

    # Extrair os valores correspondentes das correspondências
    valor = valor_match.group(1) if valor_match else None
    origem = origem_match.group(1) if origem_match else None
    #destino = destino_match.group(1) if destino_match else None
    hora_saida, dia_saida, mes_saida = data_saida_match.groups() if data_saida_match else (None, None, None)
    tempo_total = tempo_total_match.group(1) if tempo_total_match else None

    # Criar uma lista com os valores extraídos
    lista_voo = [valor, origem, f"{dia_saida}, {mes_saida}", hora_saida, tempo_total]
    return lista_voo

def cria_lista_datas(data_ini, data_fin):
    lista_de_datas = []
    
    data_atual = data_ini
    delta = timedelta(days=1)
    
    while data_atual <= data_fin:
        lista_de_datas.append(data_atual.strftime("%d/%m/%Y"))
        data_atual += delta
    
    return lista_de_datas

def ajusta_caracteres(coluna):
    coluna = coluna.str.lower()
    coluna = coluna.str.replace('ç', 'c')    
    coluna = coluna.str.replace('-', '_')
    coluna = coluna.str.replace(' ', '_')
    coluna = coluna.str.replace('á', 'a')
    coluna = coluna.str.replace('é', 'e')
    coluna = coluna.str.replace('í', 'i')
    coluna = coluna.str.replace('ó', 'o')
    coluna = coluna.str.replace('ú', 'u')
    coluna = coluna.str.replace('à', 'a')
    coluna = coluna.str.replace('è', 'e')
    coluna = coluna.str.replace('ì', 'i')
    coluna = coluna.str.replace('ò', 'o')
    coluna = coluna.str.replace('ù', 'u')
    coluna = coluna.str.replace('â', 'a')
    coluna = coluna.str.replace('ê', 'e')
    coluna = coluna.str.replace('î', 'i')
    coluna = coluna.str.replace('ô', 'o')
    coluna = coluna.str.replace('û', 'u')
    coluna = coluna.str.replace('ã', 'a')
    coluna = coluna.str.replace('õ', 'o')
    coluna = coluna.str.replace('ç', 'c')
    coluna = coluna.str.replace('ä', 'a')
    coluna = coluna.str.replace('ë', 'e')
    coluna = coluna.str.replace('ï', 'i')
    coluna = coluna.str.replace('ö', 'o')
    coluna = coluna.str.replace('ü', 'u')
    return coluna


if __name__ == '__main__':
    
    df_aeroportos = pd.read_csv('.\\aeroportos.csv', delimiter=",")
    df_aeroportos.columns = df_aeroportos.columns.str.lower()
    df_aeroportos = df_aeroportos.apply(lambda x: x.astype(str).str.lower() if x.dtype == 'object' else x)
    df_aeroportos['continente'] = df_aeroportos.apply(coloca_continente, axis=1)

    #print(df_aeroportos)

    valor = 'europa'
    df_aeroportos['codigo'] = df_aeroportos['codigo'].str.upper()
    lista_codigos_europeus = df_aeroportos.query('continente == @valor')['codigo'].to_list()  
    
    df_respostas = pd.DataFrame(columns=['valor', 'origem','data_saida'
                                , 'hora_saida','tempo_total'])

    data_inicial = datetime.strptime(input('Data inicial - formato DD/MM/AAAA: '), "%d/%m/%Y")
    data_final = datetime.strptime(input('Data final - formato DD/MM/AAAA: '), "%d/%m/%Y")

    lista_datas = cria_lista_datas(data_inicial, data_final)

    #Abrir Chrome Browser e Google Flights
    # Configurar a posição e tamanho da janela
    largura_tela, altura_tela = pyautogui.size()
    posicao_x = 0
    posicao_y = 0
    largura_janela = largura_tela // 2
    altura_janela = altura_tela

    options = webdriver.ChromeOptions()
    options.add_argument(f"--window-position={posicao_x},{posicao_y}")
    options.add_argument(f"--window-size={largura_janela},{altura_janela}")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome('chromedriver', options=options)


    for data in lista_datas:
        for cod_aerop in lista_codigos_europeus:
            resposta = google_scrapy(cod_aerop, 'GIG', data, driver)
            if resposta == 'Nao ha voos':
                print('nao ha voos de '+cod_aerop+' na data '+data)
            
            else:
                dados_resposta = pega_dados_resposta(resposta)
                dict_resposta = [{'valor': dados_resposta[0], 'origem': dados_resposta[1], 
                'data_saida': dados_resposta[2], 'hora_saida': dados_resposta[3], 
                'tempo_total': dados_resposta[4]}]
                df_respostas = pd.concat([df_respostas, pd.DataFrame(dict_resposta)])
                df_respostas_ordernadoporpreco = df_respostas.sort_values(by = 'valor')
                df_respostas_ordernadoporpreco['origem'] = ajusta_caracteres(df_respostas_ordernadoporpreco['origem'])
                df_respostas_ordernadoporpreco['data_saida'] = ajusta_caracteres(df_respostas_ordernadoporpreco['data_saida'])
                df_respostas_ordernadoporpreco.to_csv('.\\voos.csv', index=False) 
                print(df_respostas_ordernadoporpreco)
    
    #Fechando o Browser9
    driver.quit()
    
    #print(df_respostas)
    
    '''
    #resposta = google_scrapy(lista_codigos_europeus[0], 'GIG', '25/02/2024')
    resposta = 'A partir de 2904 Reais brasileiros. Voo da Tap Air Portugal com 1 parada. Sai do aeroporto Aeroporto de Berlim-Brandemburgo às 12:50 do dia domingo, fevereiro 25 e chega no aeroporto Aeroporto Internacional do Rio de Janeiro - Galeão às 06:20 do dia segunda-feira, fevereiro 26. Duração total: 21 h 30 min. Parada (1 de 1) de 8 h no aeroporto Aeroporto Humberto Delgado, emLisboa.'
    dados_resposta = pega_dados_resposta(resposta)
    print(dados_resposta)
    dict_resposta = [{'valor': dados_resposta[0], 'origem': dados_resposta[1],
                     'destino': dados_resposta[2], 'data_saida': dados_resposta[3],
                                'hora_saida': dados_resposta[4], 
                                'tempo_total': dados_resposta[5]}]
    print(dict_resposta)
    df_respostas = pd.concat([df_respostas, pd.DataFrame(dict_resposta)])
    print(df_respostas)
    '''