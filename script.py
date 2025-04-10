from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os

# Caminho do ChromeDriver
caminho_chromedriver = r'E:\Users\Franco\Documents\repo\PYTHON\automate_downloader\chromedriver.exe'

# Pasta onde os arquivos serão salvos
pasta_destino = r'E:\Users\Franco\Documents\repo\PYTHON\automate_downloader\arquivos_teste'
os.makedirs(pasta_destino, exist_ok=True)

# URL da página HTML com os grupos
url = 'https://cadastrosolidarioindustria.com.br/exportar_arquivos'

# Configurações do navegador
options = Options()
options.add_argument('--headless')  # modo invisível
service = Service(caminho_chromedriver)
driver = webdriver.Chrome(service=service, options=options)

# Abre a página
driver.get(url)

# Espera os elementos estarem preenchidos com conteúdo
def wait_for_element_with_text(driver, element_id, timeout=20):
    WebDriverWait(driver, timeout).until(
        lambda d: any(el.text.strip() for el in d.find_elements(By.ID, element_id))
    )

try:
    wait_for_element_with_text(driver, 'onda', timeout=20)
except:
    print("⚠️ Timeout esperando o campo 'onda' ser preenchido.")

# Captura HTML após os dados estarem carregados
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Busca todos os grupos
grupos = soup.find_all(id='grupoPedido')
print(f'{len(grupos)} grupos encontrados.')

for i, grupo in enumerate(grupos, start=1):
    elemento_nome = grupo.select_one('[id=nomeArquivo]')
    elemento_cnpj = grupo.select_one('[id=cnpj]')
    elemento_onda = grupo.select_one('[id=onda]')
    elemento_contador = grupo.select_one('[id=contador]')

    if not all([elemento_nome, elemento_cnpj, elemento_onda, elemento_contador]):
        print(f'❌ Grupo {i}: Elemento incompleto encontrado. Pulando...')
        continue

    caminho_arquivo = elemento_nome.get('href') or elemento_nome.get_text(strip=True)
    if not caminho_arquivo.startswith('//'):
        print(f'❌ Grupo {i}: Caminho inválido: "{caminho_arquivo}". Pulando...')
        continue

    url_completa = 'https:' + caminho_arquivo.strip()
    cnpj = elemento_cnpj.get_text(strip=True)
    onda = elemento_onda.get_text(strip=True).replace(' ', '')
    contador = elemento_contador.get_text(strip=True).zfill(3)

    extensao = os.path.splitext(url_completa)[1]
    nome_arquivo = f"{cnpj}_{onda}_{contador}{extensao}"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)

    try:
        print(f"⬇️ Grupo {i}: Baixando {url_completa}")
        resposta = requests.get(url_completa, timeout=15)
        resposta.raise_for_status()

        with open(caminho_completo, 'wb') as f:
            f.write(resposta.content)

        print(f"✅ Grupo {i}: Salvo como {nome_arquivo}")

    except Exception as e:
        print(f"❌ Grupo {i}: Erro ao baixar {url_completa}: {e}")

driver.quit()
