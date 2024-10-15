import pandas as pd  #importando a biblioteca utilizada para extrarir e tratar os dados
import matplotlib.pyplot as plt #biblioteca para mostrar os gráficos
import numpy as np #biblioteca para tratar numeros dos dados


base = pd.read_csv("acidentes_pi.csv", sep=';', encoding='latin1') #atribuindo a base de dados à variável base
base = base.drop(['id', 'pesid', 'uf', 'causa_principal', 'id_veiculo', 'latitude', 'longitude', 'regional', 'delegacia', 'uop'], axis=1) #retirando colunas que são desnecessárias para a análise
print(base) #mostrando a base de dados
print('')

#separando a quantidade de acidentes por trimestre em cada ano
base['data_inversa'] = pd.to_datetime(base['data_inversa'], format='%d/%m/%Y') #coloca o formato de data para o formato dia, mês ano
base['trimestre'] = base['data_inversa'].dt.to_period('Q') #cria uma nova coluna data inversa separada em períodos de três em três meses
acidentes_por_trimestre = base['trimestre'].value_counts().sort_index().sort_values(ascending=False) #contabiliza o número de acidentes em cada trimestre e os organiza de forma decrescente
print(acidentes_por_trimestre) # mostra a coluna acidentes por trimestre
print('') #mostra uma linha em branco para uma melhor vizualização

#verificando a qual dia da semana tem mais acidentes
acidentes_por_dia_semana = base['dia_semana'].value_counts().sort_values(ascending=False) 
print(acidentes_por_dia_semana)
print('')

#verificando horarios com mais acidentes
base['horario'] = pd.to_datetime(base['horario'], format='%H:%M:%S').dt.time #coloca o o horário para o formato hora, minuto segundo
def classificar_intervalo_horario(horario): #função para separar o horário em intervalos de 3 em 3 horas
    hora = horario.hour
    return f'{hora // 3 * 3:02d}:00 - {(hora // 3 * 3 + 3) % 24:02d}:00'
base['intervalo_horario'] = base['horario'].apply(classificar_intervalo_horario) #cria uma nova coluna com nome intervalo_horario e chama a função classificar_intervalo_horario
acidentes_por_intervalo = base['intervalo_horario'].value_counts().sort_index().sort_values(ascending=False)
print(acidentes_por_intervalo)
print('')

#verificando fase do dia com mais acidentes
acidentes_por_fase_dia = base['fase_dia'].value_counts().sort_values(ascending=False)
print(acidentes_por_fase_dia)
print('')

#acidentes por condição metereologica
acidentes_por_condicao_meteorologica = base['condicao_metereologica'].value_counts().sort_values(ascending=False)
print(acidentes_por_condicao_meteorologica)
print('')

#os 10 tipos de traçado da via que mais tiveram acidentes
acidentes_por_tracado_via = base['tracado_via'].value_counts().sort_values(ascending=False).head(10)
print(acidentes_por_tracado_via)
print('')

#acidentes por tipo de veiculo
acidentes_por_tipo_veiculo = base['tipo_veiculo'].value_counts().sort_values(ascending=False).head(12)
print(acidentes_por_tipo_veiculo)
print('')

#acidentes por causa
acidentes_por_causa = base['causa_acidente'].value_counts().sort_values(ascending=False).head(12)
print(acidentes_por_causa)
print('')

#acidentes por tipo de acidente
acidentes_por_tipo_acidente = base['tipo_acidente'].value_counts().sort_values(ascending=False).head(12)
print(acidentes_por_tipo_acidente)
print('')

#acidentes por municipio
acidentes_por_municipio = base['municipio'].value_counts().sort_values(ascending=False).head(10)
print(acidentes_por_municipio)
print('')

#numero de feridos, ilesos e mortos

base['feridos'] = base['feridos_leves'] + base['feridos_graves'] #cria uma nova coluna feridos que contem os valores de feridos_leves mais feridos_graves
base['resultado_acidente'] = 'ilesos'  #por padrão a coluna resultado acidentente recebe o valor ileso
base.loc[base['feridos'] > 0, 'resultado_acidente'] = 'feridos'  #caso a quantidade de feridos em um campo seja  maior que zero a coluna resultado acidente recebe o campo ferido 
base.loc[base['mortos'] > 0, 'resultado_acidente'] = 'mortos' #caso a quantidade de mortos em um campo seja  maior que zero a coluna resultado acidente recebe o campo mortos
acidentes_por_resultado = base['resultado_acidente'].value_counts()
porcentagem_acidentes = (acidentes_por_resultado / acidentes_por_resultado.sum()) * 100 #mostra a porcentagem de ilesos, feridos e mortos
print(porcentagem_acidentes)
print('')

#numero de feridos, ilesos e mortos para os 5 tipos de veiculos com mais acidentes

veiculos_selecionados = ['Motocicleta', 'Automóvel', 'Caminhonete', 'Semireboque', 'Caminhão'] #seleciona os 5 automóveis com mais acidentes
base_filtrada = base[base['tipo_veiculo'].isin(veiculos_selecionados)] #filtra na base para contabilizar apenas os veículos selecionados
acidentes_por_veiculo_resultado = base_filtrada.groupby(['tipo_veiculo', 'resultado_acidente']).size().unstack(fill_value=0) #agrupa os acidentes por tipo de veiculo e quantidade de feridos, ilesos e mortos
percentuais_por_veiculo = (acidentes_por_veiculo_resultado.T / acidentes_por_veiculo_resultado.sum(axis=1)).T * 100 #faz a porcentagem de feridos, ilesos e mortos nos veículos selecionados
print(percentuais_por_veiculo)
print('')

#numero de acidentes por rodovias
rodovias_acidentes = base['br'].value_counts().sort_values(ascending=False)
print(rodovias_acidentes)
print('')

#km das rodovias com maior numero de acidentes
acidentes_por_rodovia = base['br'].value_counts().reset_index(name='quantidade') #conta quantos acidentes tiveram em cada rodovia
acidentes_por_rodovia.columns = ['br', 'quantidade']
rodovias_com_mais_acidente = acidentes_por_rodovia.nlargest(5, 'quantidade') #seleciona as rodovias com mais acidentes
rodovias_filtradas = base[base['br'].isin(rodovias_com_mais_acidente['br'])] #pegar apenas as rodovias que estão entre as cinco com mais acidentes
km_acidentes = rodovias_filtradas.groupby(['br', 'km']).size().reset_index(name='quantidade') #conta quantos acidentes tiveram em cada km
quantidade_km_por_rodovia = km_acidentes.groupby('br').apply(lambda x: x.nlargest(3, 'quantidade')).reset_index(drop=True) #agrupa os 3 km com mais acidentes de cada rodovia
print(quantidade_km_por_rodovia)
print('')


#gerando os gráficos da nossa consulta

#gráfico de acidentes por trimestre

ax = acidentes_por_trimestre.plot(kind='bar', color='#FF8810', figsize=(10,6)) #cria um gráfico de barras para acidentes_por_trimestre com a cor #FF8810, com largura de 10 e altura de 6 polegadas
plt.title('Acidentes por Trimestre', fontsize=16) #cria um título para o gráfico com uma fonte 16
plt.xlabel('Trimestre', fontsize=12) #define um rótulo no eixo x com uma fonte 12
plt.ylabel('Número de Acidentes', fontsize=12)#define um rótulo no eixo y com uma fonte 12
ax.set_xticklabels(acidentes_por_trimestre.index, rotation=45, ha='right') #adiciona cada trimestre no eixo x  com uma rotação de 45 graus e alinha o texto a direita
ax.set_ylim(0, 5200) #define os limites do eixo y

for p in ax.patches: #loop para percorrer cada barra do gráfico
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points') #adiciona rótulos com os valores de cada barra, alinhada horizontalmente ao centro e verticalmente acima de cada barra

plt.tight_layout() #ajustar o gráfico automaticamente para evitar que os rótulos fiquem cortados ou sobrepostos
plt.show() #mostrar o gráfico

#gráficos de acidentes por dia da semana

ax = acidentes_por_dia_semana.plot(kind='bar', color='#AA22AA', figsize=(10,6))
plt.title('Acidentes por Dia da Semana', fontsize=16)
plt.xlabel('Dia da Semana', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_dia_semana.index, rotation=45, ha='right')
ax.set_ylim(0, 12000)

for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

#acidentes por intervalo de horário

ax = acidentes_por_intervalo.plot(kind='bar', color='#22CC10', figsize=(10,6))
plt.title('Acidentes por Intervalo de Horário (3 em 3 horas)', fontsize=16)
plt.xlabel('Intervalo de Horário', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_intervalo.index, rotation=45, ha='right')
ax.set_ylim(0, 12000)

for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

#acidentes por fase do dia

ax = acidentes_por_fase_dia.plot(kind='bar', color='skyblue', figsize=(10,6))
plt.title('Acidentes por Fase do Dia', fontsize=16)
plt.xlabel('Fase do Dia', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_fase_dia.index, rotation=45, ha='right')
ax.set_ylim(0, 28000)

for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()



#acidentes por condição metereologica

ax = acidentes_por_condicao_meteorologica.plot(kind='bar', color='#55D110', figsize=(10,6))
plt.title('Acidentes por Condição Meteorológica', fontsize=16)
plt.xlabel('Condição Meteorológica', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_condicao_meteorologica.index, rotation=45, ha='right')
ax.set_ylim(0, 42000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_condicao_meteorologica.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()


#acidentes por traçado da via

ax = acidentes_por_tracado_via.plot(kind='bar', color='lightcoral', figsize=(10,6))
plt.title('Acidentes por Traçado da Via', fontsize=16)
plt.xlabel('Traçado da Via', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_tracado_via.index, rotation=45, ha='right')
ax.set_ylim(0, 37000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_tracado_via.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')
plt.tight_layout()
plt.show()


#acidentes por tipo de veiculo

ax = acidentes_por_tipo_veiculo.plot(kind='bar', color='seagreen', figsize=(10,6))
plt.title('Acidentes por Tipo de Veículo', fontsize=16)
plt.xlabel('Tipo de Veículo', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_tipo_veiculo.index, rotation=45, ha='right')
ax.set_ylim(0, 16000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_tipo_veiculo.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

#acidentes por causa

ax = acidentes_por_causa.plot(kind='bar', color='gold', figsize=(10,6))
plt.title('Principais Causas dos Acidentes', fontsize=16)
plt.xlabel('Causa do Acidente', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_causa.index, rotation=40, ha='right')
ax.set_ylim(0,6000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_causa.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()


#acidentes por tipo

ax = acidentes_por_tipo_acidente.plot(kind='bar', color='slateblue', figsize=(10,6))
plt.title('Principais Formas de Acidentes', fontsize=16)
plt.xlabel('Tipo de Acidente', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_tipo_acidente.index, rotation=40, ha='right')
ax.set_ylim(0, 12000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_tipo_acidente.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

#acidentes por município

ax = acidentes_por_municipio.plot(kind='bar', color='skyblue', figsize=(10,6))
plt.title('Acidentes por Município', fontsize=16)
plt.xlabel('Município', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
ax.set_xticklabels(acidentes_por_municipio.index, rotation=45, ha='right')
ax.set_ylim(0, 14000)

for i, p in enumerate(ax.patches):
    ax.annotate(f'{acidentes_por_municipio.iloc[i]}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', fontsize=11, color='black', 
                xytext=(0, 10), textcoords='offset points')

plt.tight_layout()
plt.show()

#numero de ilesos, feridos e mortos

plt.figure(figsize=(8,8))
plt.pie(porcentagem_acidentes, labels=porcentagem_acidentes.index, autopct='%1.1f%%', colors=['lightgreen', 'skyblue', 'lightcoral'], startangle=90) #gráfico em forma de pizza para os dados das porcentagens
plt.title('Distribuição dos Acidentes por Resultado (Feridos, Ilesos, Mortos)', fontsize=16)
plt.axis('equal') #garantir que o gráfico seja um círculo perfeito
plt.show()

#percentual de feridos, ilesos e mortos nos 5 tipos de veículos com mais acidentes

ax = percentuais_por_veiculo.plot(kind='barh', stacked=True, color=['lightgreen', 'lightcoral', 'skyblue'], figsize=(10,6)) #cria um gráfico de barras horizontal
plt.title('Percentual de Ilesos, Feridos e Mortos por Tipo de Veículo', fontsize=16)
plt.xlabel('Percentual (%)', fontsize=12)
plt.ylabel('Tipo de Veículo', fontsize=12)
for i in range(len(percentuais_por_veiculo)): #loop para percorrer todas as linhas da base e colocar os valores percentual sobre as barras 
    acumulado = 0
    for j, resultado in enumerate(percentuais_por_veiculo.columns): #outro loop para percorrer cada coluna da base nas categorias ilesos, feridos e mortos
        valor = percentuais_por_veiculo.iloc[i, j] #extrai os valores percentuais de cada célula
        if valor > 0.2: #mostra apenas os valores que são maiores que 0.2%
            ax.text(acumulado + valor / 2,
                    i, 
                    f'{valor:.1f}%',
                    ha='center', va='center',color='black', fontsize=10) #adiciona o percentual de cada valor centralizado sobre cada parte da barra
        acumulado += valor #atualiza o valor acumulado para a próxima iteração

plt.legend(title='Resultado do Acidente', bbox_to_anchor=(1.05, 1), loc='upper left') #faz uma legenda no gráfico explicando cada cor
plt.tight_layout()
plt.show()

#acidentes por rodovia

barras = rodovias_acidentes.head(10).plot(kind='bar', color='skyblue', figsize=(12, 6))
plt.title('Rodovias com Mais Acidentes', fontsize=16)
plt.xlabel('Rodovia (BR)', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)
plt.xticks(rotation=45)

for bar in barras.patches:
    plt.annotate(f'{int(bar.get_height())}', 
                 (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                 ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()

#quilometragem com mais acidentes da principais rodovias

plt.figure(figsize=(12, 8))
cores = ['skyblue', 'orange', 'green', 'red', 'purple']
for i, br in enumerate(quantidade_km_por_rodovia['br'].unique()): # Inicia um loop que itera sobre as rodovias únicas presentes na coluna br de quantidade_km_por_rodovia.
    km_por_br = quantidade_km_por_rodovia[quantidade_km_por_rodovia['br'] == br] #filtra a coluna para obter apenas os valores da rodovia atual
    positions = range(i * len(km_por_br), (i + 1) * len(km_por_br)) #define as posições das barras no eixo X para a rodovia atual.
    plt.bar(positions, km_por_br['quantidade'], width=0.75, color=cores[i], label=f'BR-{br}') #plota as barras da rodovia atual 
plt.xticks(range(len(quantidade_km_por_rodovia)), quantidade_km_por_rodovia['km'].astype(str), rotation=45) #rótulos do eixo x para quilômetros com uma rotação de 45 graus
plt.title('trecho com Mais Casos nas 5 Rodovias com Mais Acidente', fontsize=16)
plt.xlabel('Quilômetro (km)', fontsize=12)
plt.ylabel('Número de Acidentes', fontsize=12)

for index, row in quantidade_km_por_rodovia.iterrows(): #loop que itera sobre cada linha da tabela quantidade_km_por_rodovia.
    plt.text(index, row['quantidade'] + 5,
             str(row['quantidade']),
             va='bottom', ha='center', fontsize=10, color='black') #coloca o número de acidentes em cima de cada barra

plt.legend(title='Rodovia (BR)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

