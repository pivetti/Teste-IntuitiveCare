import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
OUTPUT_DIR = "anexos"
ZIP_NAME = "anexos.zip"

def download_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    session = requests.Session()
    
    try:
        response = session.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        anexos = []
        for link in soup.select('a[href$=".pdf"]'):
            text = link.text.strip().lower()
            if 'anexo i' in text or 'anexo ii' in text:
                url = urljoin(BASE_URL, link['href'])
                filename = os.path.join(OUTPUT_DIR, url.split('/')[-1])
                
                print(f"Baixando arquivo: {filename}")
                with session.get(url, stream=True) as pdf_response:
                    pdf_response.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in pdf_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Arquivo baixado com sucesso: {filename}")
                anexos.append(filename)
                
        return anexos
    except Exception as e:
        print(f"Erro: {e}")
        return []

def zip_files(files):
    print(f"Compactando arquivos em {ZIP_NAME}...")
    with zipfile.ZipFile(ZIP_NAME, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))
    print(f"Arquivos compactados com sucesso em {ZIP_NAME}")

if __name__ == "__main__":
    downloaded = download_pdfs()
    if downloaded:
        zip_files(downloaded)
    else:
        print("Nenhum arquivo encontrado")