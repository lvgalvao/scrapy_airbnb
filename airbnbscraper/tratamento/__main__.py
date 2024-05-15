import pandas as pd
import json
import os
import re

# Defina o caminho para o arquivo JSON na pasta data
input_file = os.path.join('data', 'resultados.json')
output_file = os.path.join('data', 'resultados_processados.json')

# Carregar os dados do arquivo JSON usando a codificação utf-8
with open(input_file, encoding='utf-8') as f:
    data = json.load(f)

# Criar um DataFrame a partir dos dados
df = pd.DataFrame(data)

# Função para extrair o score e a quantidade de avaliações
def extract_score_and_reviews(score_text):
    if pd.isna(score_text):
        return None, None
    # Usar expressão regular para extrair números
    score_match = re.search(r'(\d+,\d+|\d+\.\d+|\d+)', score_text)
    qte_score_match = re.search(r'(\d{1,3}(?:\.\d{3})*) avaliações', score_text)
    
    if score_match and qte_score_match:
        score = score_match.group(1).replace(',', '.')
        qte_score = qte_score_match.group(1).replace('.', '')
        return float(score), int(qte_score)
    return None, None

# Função para limpar o preço
def clean_price(price_text):
    if pd.isna(price_text):
        return None
    # Extrair apenas os números do preço
    price_match = re.search(r'(\d+)', price_text.replace('.', ''))
    if price_match:
        return int(price_match.group(1))
    return None

def clean_href(href_text):
    if pd.isna(href_text):
        return None
    return href_text.replace('/experiences/', '')

# Função para limpar a duração
def clean_duration(duration_text):
    if pd.isna(duration_text):
        return None
    # Extrair apenas os números do duration e converter para float
    duration_match = re.search(r'(\d+,\d+|\d+)', duration_text)
    if duration_match:
        return float(duration_match.group(1).replace(',', '.'))
    return None

# Aplicar a função a cada linha do DataFrame
df['score'], df['qte_score'] = zip(*df['score'].apply(extract_score_and_reviews))
df['price'] = df['price'].apply(clean_price)
df['href'] = df['href'].apply(clean_href)
df['duration'] = df['duration'].apply(clean_duration)

df.rename(columns={'aria_label': 'nome_passeio'}, inplace=True)

# Verificar os dados processados
print(df.head())

# Salvar o DataFrame processado em um novo arquivo JSON usando a codificação utf-8
df.to_json(output_file, orient='records', lines=True, force_ascii=False)
