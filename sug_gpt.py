import threading
from selenium import webdriver
import pandas as pd

# Função para realizar o scraping e processamento
def processar_dados(data, lista_codigos_europeus):
    # Configurar o WebDriver para cada thread
    global df_respostas
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome('chromedriver', options=options)

    for cod_aerop in lista_codigos_europeus:
        resposta = google_scrapy(cod_aerop, cod_dest, data, driver)
        if resposta == 'Nao ha voos':
            print('nao ha voos de ' + cod_aerop + ' na data ' + data)
        else:
            dados_resposta = pega_dados_resposta(resposta)
            dict_resposta = [{'valor': dados_resposta[0], 'origem': dados_resposta[1], 
                              'data_saida': dados_resposta[2], 'hora_saida': dados_resposta[3], 
                              'tempo_total': dados_resposta[4]}]
            df_respostas = pd.concat([df_respostas, pd.DataFrame(dict_resposta)])
            df_respostas_ordernadoporpreco = df_respostas.sort_values(by='valor')
            df_respostas_ordernadoporpreco['origem'] = ajusta_caracteres(df_respostas_ordernadoporpreco['origem'])
            df_respostas_ordernadoporpreco['data_saida'] = ajusta_caracteres(df_respostas_ordernadoporpreco['data_saida'])
            df_respostas_ordernadoporpreco.to_csv('.\\voos.csv', index=False) 
            print(df_respostas_ordernadoporpreco)

    # Fechando o WebDriver
    driver.quit()

# Lista de datas e códigos
lista_datas = [...]  # Preencha com suas datas
lista_codigos_europeus = [...]  # Preencha com seus códigos

# Inicializar DataFrame e outras variáveis necessárias
df_respostas = pd.DataFrame()

# Criar e iniciar threads
threads = []
for data in lista_datas:
    thread = threading.Thread(target=processar_dados, args=(data, lista_codigos_europeus))
    threads.append(thread)
    thread.start()

# Aguardar todas as threads terminarem
for thread in threads:
    thread.join()

# Agora você pode prosseguir com o restante do código após as threads terminarem
