#Importando bibliotecas
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
import pandas as pd
import re
from datetime import datetime, timedelta
import pyautogui
import threading
import os

'''
busca_voos.py
Bruno Rodrigues Pacheco
28/09/2023

Esta versao esta fazendo o seguinte:
    - usa o selenium para navegar no gooogle flights e buscar os precos de passagens
        - o selenium precisa da aplicacao chromedriver.exe colocado em alguma pasta do path
        - colocar o chromedriver dentro da pasta do venv/Scripts'
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
    wait(driver, css) # wait for the element to appear
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
    """
    This function performs a web scraping on Google Flights website to search for flights.
    It receives the departure city (dep), arrival city (arr), departure date (dep_dt) and a driver object.
    The driver object is used to interact with the website.
    The function returns information about the best flight found or 'Nao ha voos' if no flights were found.
    """
    
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

def pega_dados_resposta(string_voo):

    # Expressões regulares para extrair os valores desejados
    valor_match = re.search(r"A partir de (\d+) Reais brasileiros", string_voo)
    origem_match = re.search(r"Sai do aeroporto (.+?) às", string_voo)
    destino_match = re.search(r"chega no aeroporto (.+?) às", string_voo)
    data_saida_match = re.search(r"(\d{2}:\d{2}) do dia (.+?) (\d+)", string_voo)
    tempo_total_match = re.search(r"Duração total: (.+?)\. Parada", string_voo)

    # Extrair os valores correspondentes das correspondências
    valor = valor_match.group(1) if valor_match else None
    origem = origem_match.group(1) if origem_match else None
    destino = destino_match.group(1) if destino_match else None
    hora_saida, dia_saida, mes_saida = data_saida_match.groups() if data_saida_match else (None, None, None)
    tempo_total = tempo_total_match.group(1) if tempo_total_match else None

    # Criar uma lista com os valores extraídos
    lista_voo = [valor, origem, f"{dia_saida}, {mes_saida}", hora_saida, tempo_total, destino]
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

def processar_dados(data_th, orig, dest):
    print(f'Iniciando processamento para a data {data_th} em thread {threading.current_thread().name} - data ')
    global df_respostas
    #Abrir Chrome Browser e Google Flights

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome('chromedriver', options=options)
    
    for cod_arp_orig in orig:
        for cod_arp_dest in dest:
            try:
                resposta = google_scrapy(cod_arp_orig, cod_arp_dest, data_th, driver)
                if resposta == 'Nao ha voos':
                    print('nao ha voos de '+cod_arp_orig+' para '+cod_arp_dest+' na data '+data_th)
                
                else:
                    dados_resposta = pega_dados_resposta(resposta)
                    dict_resposta = [{'valor': dados_resposta[0], 'origem': dados_resposta[1], 
                    'destino': dados_resposta[5], 'data_saida': dados_resposta[2], 'hora_saida': dados_resposta[3], 
                    'tempo_total': dados_resposta[4]}]

                    lock.acquire()

                    df_respostas = pd.concat([df_respostas, pd.DataFrame(dict_resposta)])
                    df_respostas_ordernadoporpreco = df_respostas.sort_values(by = 'valor')
                    df_respostas_ordernadoporpreco['origem'] = ajusta_caracteres(df_respostas_ordernadoporpreco['origem'])
                    df_respostas_ordernadoporpreco['destino'] = ajusta_caracteres(df_respostas_ordernadoporpreco['destino'])
                    df_respostas_ordernadoporpreco['data_saida'] = ajusta_caracteres(df_respostas_ordernadoporpreco['data_saida'])
                    df_respostas_ordernadoporpreco.to_csv('.\\voos.csv', index=False) 
                    lock.release()

                    print(df_respostas_ordernadoporpreco)
                
            except:
                print('erro na thread '+threading.current_thread().name+' do aeroporto '+cod_arp_orig+' para o aeroporto '+cod_arp_dest+' na data '+data_th)
                pass

    #Fechando o Browser9
    driver.quit()

def obt_rsp_oto_otm_mto():
    """
    Function to obtain user input for the desired search mode.

    Returns:
        int: The selected search mode (1 for One to One, 2 for One to Many, 3 for Many to One).
    """
    padrao = r"^[1-3]$"
    while True:
        resposta = input('Deseja pesquisar qual modalidade?\n1 - One to One\n2 - One to Many\n3 - Many to One?\n')
        if re.match(padrao, resposta):
            return int(resposta)
        else:
            print("Resposta invalida. Você deve inserir um número inteiro entre 1 e 3.")

def obt_rsp_aeroportos(df_aeroportos):
    """
    Function to obtain user input for the desired airports.

    Args:
        df_aeroportos (pandas.DataFrame): DataFrame with airport information.

    Returns:
        list: The selected airport codes.
    """
    padrao = r"^[A-Z]{3}$"
    while True:
        print("Lista de Aeroportos:")
        for index, row in df_aeroportos.iterrows():
            print(f"Código: {row['codigo']} - Cidade: {row['cidade']} - País: {row['pais']}")
        resposta = input('Digite os códigos dos aeroportos separados por vírgula:\n')
        aeroportos = resposta.split(',')
        aeroportos = [a.strip().upper() for a in aeroportos]
        if all(re.match(padrao, a) for a in aeroportos):
            if all(a in df_aeroportos['codigo'].to_list() for a in aeroportos):
                return aeroportos
            else:
                print("Resposta inválida. Você deve inserir códigos de aeroportos válidos.")
        else:
            print("Resposta inválida. Você deve inserir códigos de aeroportos válidos.")

if __name__ == '__main__':
    
    df_aeroportos = pd.read_csv('.\\aeroportos.csv', delimiter=",")
    #df_aeroportos.columns = df_aeroportos.columns.str.lower()
    #df_aeroportos = df_aeroportos.apply(lambda x: x.astype(str).str.lower() if x.dtype == 'object' else x)
    #df_aeroportos['continente'] = df_aeroportos.apply(coloca_continente, axis=1)

    #valor = 'europa'
    df_aeroportos['codigo'] = df_aeroportos['codigo'].str.upper()
    #lista_codigos_europeus = df_aeroportos.query('continente == @valor')['codigo'].to_list()  
    
    df_respostas = pd.DataFrame(columns=['valor', 'origem','data_saida'
                                , 'hora_saida','tempo_total'])

    #data_inicial = datetime.strptime(input('Data inicial - formato DD/MM/AAAA: '), "%d/%m/%Y")
    #data_final = datetime.strptime(input('Data final - formato DD/MM/AAAA: '), "%d/%m/%Y")
    
    data_inicial = datetime.strptime("09/02/2024", "%d/%m/%Y")
    data_final = datetime.strptime("25/02/2024", "%d/%m/%Y")
    lista_datas = cria_lista_datas(data_inicial, data_final)
    
    opcao_oto_otm_mto = obt_rsp_oto_otm_mto()
    
    if opcao_oto_otm_mto == 1:
        print('Opcao selecionada: One to One')
        # cod_orig = input('Aeroporto de Origem: ')
        # cod_dest = input('Aeroporto de Destino: ')
        orig = ['GRU']
        dest = ['LIS']
        pass
    
    elif opcao_oto_otm_mto == 2:
        print('Opcao selecionada: One to Many')
        # cod_orig = input('Aeroporto de Origem: ')
        orig = ['GRU']
        #dest = obt_rsp_aeroportos(df_aeroportos) 
        dest = ['LIS', 'MAD', 'BCN']   
    
    elif opcao_oto_otm_mto == 3:
        print('Opcao selecionada: Many to One')
        #orig = obt_rsp_aeroportos(df_aeroportos)
        orig = ['LIS', 'MAD', 'BCN']
        # cod_dest = input('Aeroporto de Destino: ')
        dest = ['LIS']

    lock = threading.Lock()
    
    # Criar e iniciar threads
    threads = []
    print(df_respostas.head())
    for data in lista_datas:
        thread = threading.Thread(target=processar_dados, args = (data, orig, dest,))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()