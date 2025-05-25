from faker import Faker 
import pandas as pd 
import random 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def gerar_dados_falsos(num_linhas):
    fake = Faker(['pt_BR']) 
    Faker.seed(4321) 
    random.seed(4321)
    dados_falsos = []
    for _ in range(num_linhas):
        plano = random.choice(['amil', 'hapvida', 'bradesco', 'unimed']) 
        data = fake.date_between(start_date= datetime.strptime('2024-01-01', '%Y-%m-%d').date(), end_date=date.today())
        pagamento = fake.random_number(digits=4) 
        data_pagamento = data
        saida = fake.random_number(digits=4) 
        saldo = pagamento - saida
        carteira = fake.random_number(digits=5)
      

        # adicionar as variáveis a lista abaixo
        dados_falsos.append([plano, data, pagamento, data_pagamento, saida, saldo, carteira])
    
    return dados_falsos


num_linhas = 500

dados = gerar_dados_falsos(num_linhas)

# adicionar as variáveis a lista abaixo
colunas = ['plano','data','pagamento','data_pagamento','saida','saldo','carteira']

dados_falsos = pd.DataFrame(dados, columns=colunas)

dados_falsos.to_parquet('../data/mock_data.parquet', engine='pyarrow')
