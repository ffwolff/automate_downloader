# auto-downloader-python

Este projeto automatiza o download de arquivos de uma página web utilizando Python, Selenium e BeautifulSoup. Ele percorre os elementos da página, monta a URL de cada arquivo e salva localmente com um nome estruturado.

## O que o script faz

1. Acessa uma URL definida no código.
2. Busca todos os elementos com `id="grupoPedido"`.
3. Para cada grupo:
   - Coleta os valores dos elementos com `id="nomeArquivo"`, `id="cnpj"`, `id="onda"` e `id="contador"`.
   - Concatena `"https"` com o valor de `nomeArquivo` (caso comece com //) para formar a URL completa do arquivo.
   - Extrai a extensão do arquivo.
   - Gera um nome de arquivo no formato: `{CNPJ}_{Onda}_{Contador}.{extensão}`
   - Faz o download do arquivo e salva na pasta definida pelo usuário (por padrão, `Downloads`).

> ⚠️ O script lida com elementos que possuem IDs duplicados, algo incomum, mas possível em páginas não padronizadas. Também garante que os arquivos só sejam baixados quando todos os dados esperados estiverem presentes.

## Exemplo de nome final

Para:
- `cnpj = 23924235000175`
- `onda = Onda1`
- `contador = 6`
- URL termina em `.pdf`

O nome salvo será:

```
23924235000175_Onda1_006.pdf
```

## Estrutura esperada do projeto

```
auto-downloader-python/
│
├── chromedriver.exe             # ChromeDriver compatível com seu navegador (ignorado pelo Git)
├── script.py                    # Script principal
├── .gitignore                   # Arquivos ignorados pelo Git
├── requirements.txt             # Dependências do projeto
├── README.md                    # Este arquivo
```

## Como usar

### 1. Instale o Python

Baixe e instale a versão mais recente em:  
https://www.python.org/downloads/

Na instalação, marque a opção **“Add Python to PATH”**.

### 2. Instale as dependências

Abra o terminal e execute:

```bash
pip install -r requirements.txt
```

Se ainda não tiver um `requirements.txt`, você pode criá-lo com:

```bash
pip freeze > requirements.txt
```

### 3. Baixe o ChromeDriver

1. Verifique a versão do seu navegador Chrome.
2. Acesse: https://googlechromelabs.github.io/chrome-for-testing/
3. Baixe a versão correspondente ao seu Chrome.
4. Extraia o executável `chromedriver.exe` para a raiz do projeto.

### 4. Atualize a URL e os caminhos no script

Abra o arquivo `script.py` e eatualize estas variáveis::

```python
caminho_chromedriver = r"SEU_CAMINHO_AQUI"
pasta_destino = r"SEU_DESTINO_AQUI"
url = "SUA_URL_AQUI"
```

### 5. Execute o script

No terminal:

```bash
python script.py
```

## Observações

- O script é robusto contra elementos ausentes ou malformados.
- O Chrome é executado em modo invisível (headless).
- Os arquivos são nomeados de forma única com base no conteúdo da página.
- Use com responsabilidade e somente com permissão para download.

---

## Licença

Este projeto está licenciado sob a licença MIT.