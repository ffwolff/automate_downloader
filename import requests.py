from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os
import time

# Caminho do ChromeDriver
caminho_chromedriver = r'C:\Users\FRANCO.WOLFF\Documents\REPO\industra_solidaria\chromedriver.exe'

# Pasta onde os arquivos serão salvos
pasta_destino = r'C:\Users\FRANCO.WOLFF\Documents\REPO\industra_solidaria\arquivos'
os.makedirs(pasta_destino, exist_ok=True)

# URL da página HTML com os grupos
url = 'SEU_LINK_AQUI'  # <- substitua conforme necessário

# Configurações do navegador
options = Options()
# options.add_argument('--headless')
service = Service(caminho_chromedriver)
driver = webdriver.Chrome(service=service, options=options)

# Abre a página
driver.get(url)
time.sleep(5)

# Pega o HTML da página
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Busca todos os grupos
grupos = soup.find_all(id='grupoPedido')
print(f'{len(grupos)} grupos encontrados.')

for grupo in grupos:
    # Usa seletor CSS para buscar mesmo IDs duplicados
    elemento_nome = grupo.select_one('[id=nomeArquivo]')
    elemento_cnpj = grupo.select_one('[id=cnpj]')
    elemento_onda = grupo.select_one('[id=onda]')

    if not (elemento_nome and elemento_cnpj and elemento_onda):
        print('❌ Elemento incompleto encontrado. Pulando...')
        continue

    # Pega a URL parcial do arquivo
    caminho_arquivo = elemento_nome.get('href') or elemento_nome.get_text(strip=True)
    url_completa = 'https:' + caminho_arquivo.strip()

    cnpj = elemento_cnpj.get_text(strip=True)
    onda = elemento_onda.get_text(strip=True)

    extensao = os.path.splitext(url_completa)[1]
    nome_arquivo = f"{cnpj}_{onda}{extensao}"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    try:
        print(f"⬇️ Baixando: {url_completa}")
        resposta = requests.get(url_completa, timeout=15)
        resposta.raise_for_status()

        with open(caminho_completo, 'wb') as f:
            f.write(resposta.content)

        print(f"✅ Salvo como: {nome_arquivo}")

    except Exception as e:
        print(f"❌ Erro ao baixar {url_completa}: {e}")

driver.quit()
