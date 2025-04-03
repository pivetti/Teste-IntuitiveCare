import pdfplumber
import pandas as pd
import zipfile
import os

def extrair_tabela(pdf_path, csv_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                data.extend(table)
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print("CSV gerado com sucesso!")
    return csv_path

def substituir_abreviacoes(csv_path, csv_corrigido_path):
    df = pd.read_csv(csv_path)
    legenda = {"OD": "Odontológico", "AMB": "Ambulatorial"}
    df.replace(legenda, inplace=True)
    df.to_csv(csv_corrigido_path, index=False)
    print("Abreviações substituídas!")
    return csv_corrigido_path

def compactar_csv(csv_corrigido_path, zip_path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(csv_corrigido_path, os.path.basename(csv_corrigido_path))
    print("Arquivo compactado com sucesso!")

def main():
    pdf_path = "anexos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    csv_path = "transformacao_dados/rol_procedimentos.csv"
    csv_corrigido_path = "transformacao_dados/rol_procedimentos_corrigido.csv"
    zip_path = "Teste_Henrique_Pivetti.zip"
    
    extrair_tabela(pdf_path, csv_path)
    substituir_abreviacoes(csv_path, csv_corrigido_path)
    compactar_csv(csv_corrigido_path, zip_path)
    
if __name__ == "__main__":
    main()
