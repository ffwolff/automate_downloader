# 📥 Download Automático de Arquivos com Selenium e BeautifulSoup

Este projeto automatiza o download de arquivos de uma página web utilizando **Python**, **Selenium** e **BeautifulSoup**. Ele percorre os elementos da página, monta a URL de cada arquivo e salva localmente com um nome estruturado.

## 🔧 O que o script faz

1. Acessa uma URL definida no código.
2. Busca todos os elementos com `id="grupoPedido"`.
3. Para cada grupo:
   - Coleta os valores dos elementos com `id="nomeArquivo"`, `id="cnpj"` e `id="onda"`.
   - Concatena `"https"` com o valor de `nomeArquivo` para formar a URL do arquivo.
   - Extrai a extensão do arquivo.
   - Gera um nome de arquivo no formato: `{CNPJ}_{Onda}.{extensão}`
   - Faz o download do arquivo e salva na pasta `arquivos`.

> ⚠️ O script lida com elementos que possuem IDs repetidos, algo incomum, mas possível em páginas não padronizadas.

## 🧾 Exemplo de nome final

Para:
- `cnpj = 23924235000175`
- `onda = Onda1`
- URL termina em `.jpg`

O nome salvo será:

```
23924235000175_Onda1.jpg
```

## 📂 Estrutura esperada do projeto

```
industra_solidaria/
│
├── chromedriver.exe             # ChromeDriver compatível com seu navegador
├── download_arquivos.py        # Script principal
├── arquivos/                   # Pasta onde os arquivos serão salvos
├── README.md                   # Este arquivo
```

## 🚀 Como usar

### 1. Instale o Python

Baixe e instale a versão mais recente em:  
https://www.python.org/downloads/

Na instalação, marque a opção **“Add Python to PATH”**.

### 2. Instale as dependências

Abra o terminal e execute:

```bash
pip install selenium beautifulsoup4 requests
```

### 3. Baixe o ChromeDriver

1. Verifique a versão do seu navegador Chrome.
2. Acesse: https://googlechromelabs.github.io/chrome-for-testing/
3. Baixe a versão correspondente ao seu Chrome.
4. Extraia o executável `chromedriver.exe` para a raiz do projeto.

### 4. Atualize a URL no script

Abra o arquivo `download_arquivos.py` e edite a variável `url`:

```python
url = 'https://www.seusite.com/sua_pagina'
```

### 5. Crie a pasta `arquivos`

Essa pasta é onde os arquivos serão baixados. Crie manualmente ou use o terminal:

```bash
mkdir arquivos
```

### 6. Execute o script

No terminal:

```bash
python download_arquivos.py
```

## 💻 Exemplo de script (`download_arquivos.py`)

```python
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# URL da página a ser acessada
url = 'https://www.seusite.com/sua_pagina'

# Configurações do ChromeDriver
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    time.sleep(3)  # Aguarda carregamento da página

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    grupos = soup.find_all(id='grupoPedido')

    if not os.path.exists('arquivos'):
        os.makedirs('arquivos')

    for grupo in grupos:
        nome_arquivo_element = grupo.find(id='nomeArquivo')
        cnpj_element = grupo.find(id='cnpj')
        onda_element = grupo.find(id='onda')

        if nome_arquivo_element and cnpj_element and onda_element:
            nome_arquivo = nome_arquivo_element.text.strip()
            cnpj = cnpj_element.text.strip()
            onda = onda_element.text.strip()

            url_download = f"https{nome_arquivo}"
            extensao = os.path.splitext(url_download)[1]
            nome_final = f"{cnpj}_{onda}{extensao}"
            caminho_completo = os.path.join('arquivos', nome_final)

            try:
                resposta = requests.get(url_download)
                if resposta.status_code == 200:
                    with open(caminho_completo, 'wb') as f:
                        f.write(resposta.content)
                    print(f"✅ Arquivo salvo: {nome_final}")
                else:
                    print(f"❌ Erro ao baixar: {url_download}")
            except Exception as e:
                print(f"⚠️ Erro ao salvar {nome_final}: {e}")
        else:
            print("⚠️ Elemento com dados ausentes. Pulando item...")

except Exception as e:
    print(f"Erro geral: {e}")
finally:
    driver.quit()
```

---

## 🧠 Observações

- O script funciona mesmo que elementos com `id` se repitam (não recomendado em HTML, mas tratado no código).
- Use com responsabilidade e sempre com permissão para download.
- Pode ser adaptado facilmente para páginas com estrutura similar.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.
