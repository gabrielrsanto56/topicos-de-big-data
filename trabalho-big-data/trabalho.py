import pandas as pd  #importando a biblioteca utilizada para extrarir e tratar os dados
import matplotlib.pyplot as plt #biblioteca para mostrar os gráficos

base = pd.read_csv("acidentes_pi.csv", sep=';', encoding='latin1') #atribuindo a base de dados à variável base
base = base.drop(['id', 'pesid', 'uf', 'causa_principal', 'id_veiculo', 'latitude', 'longitude', 'regional', 'delegacia', 'uop'], axis=1) #retirando colunas que são desnecessárias para a análise

#separando a quantidade de acidentes por mês
base['data_inversa'] = pd.to_datetime(base['data_inversa'], format='%d/%m/%Y')
"""base['ano'] = base['data_inversa'].dt.year
base['mes'] = base['data_inversa'].dt.month
acidentes_por_mes = base.groupby(['ano', 'mes']).size()"""


#separando a quantidade de acidentes por trimestre em cada ano
base['trimestre'] = base['data_inversa'].dt.to_period('Q')
acidentes_por_trimestre = base['trimestre'].value_counts().sort_index()
ordem_acidente_trimestre = acidentes_por_trimestre.sort_values(ascending=False)
print(ordem_acidente_trimestre)




print(base)




