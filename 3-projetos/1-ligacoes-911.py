# Ligações para o 911


# Projeto de análise de alguns dados de chamadas para o 911
# Dataset disponível no Kaggle
# https://www.kaggle.com/mchirico/montcoalert


# Colunas do dataset:
# * lat: Variável String, Latitude
# * lng: Variável String, Longitude
# * desc: Variável String, Descrição da Chamada de Emergência
# * zip: Variável String, CEP
# * título: Variável String, Título
# * timeStamp: Variável String, AAAA-MM-DD HH: MM: SS
# * twp: Variável String, Township
# * addr: Variável String, Endereço
# * e: Variável String, variável Dummy (sempre 1)


# Importações necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


print ('\n\n# Lendo o arquivo csv e visualizando suas informações')
df = pd.read_csv('projetos/df/911.csv')
print(df.info())
print(df.head())


print('\n\n# Top 5 CEPs nas chamadas 911 (Que mais se repetem)')
print(df['zip'].value_counts().head(5))


print('\n\n# Os 5 principais municípios nas chamadas 911')
print(df['twp'].value_counts().head(5))


print('\n\n# Coluna "title". Quantidade de códigos de título exclusivos')
print(df['title'].value_counts().count())
# OU
# print(df['title'].nunique())
# print(len(df['title'].unique()))


print('\n\n# Criação da coluna reason a partir da coluna title')
# Por exemplo:
# Coluna title EMS: BACK PAINS / BLESSOR
# Razão: EMS
df['reason'] = df.apply(lambda column : column['title'].split(':')[0], axis=1)
# OU
# df['reason'] = df['title'].apply(lambda title: title.split(':')[0])
print(df.head())
print(df['reason'].value_counts())


print('\n\n# Motivo mais comum para uma chamada do 911 com base na reason')
print(df['reason'].value_counts())
print(df['reason'].value_counts().head(1))


print('\n\n# Seaborn - Countplot de chamadas 911 baseadas na coluna reason')
sns.countplot(x='reason', color='blue', data=df)
plt.show()


print('\n\n# Tipo de dados dos objetos na coluna timeStamp')
print(df['timeStamp'].dtypes)


print('\n\n# Converter a coluna timeStamp em objetos DateTime')
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
print(df['timeStamp'].dtypes)


print('\n\n# Pegando a hora da coluna timeStamp')
time = df['timeStamp'].iloc[0]
print(time.hour)


print('\n\n# Criação das novas colunas hour, month e dayWeek')
df['hour'] = df['timeStamp'].dt.hour
df['month'] = df['timeStamp'].dt.month
df['dayWeek'] = df['timeStamp'].dt.dayofweek


print('\n\n# Conversão do dia da semana número para texto')
days = {
    0: 'Segunda', 
    1: 'Terça', 
    2: 'Quarta', 
    3: 'Quinta', 
    4: 'Sexta', 
    5: 'Sábado', 
    6: 'Domingo',
}
df['dayWeekText'] = df['dayWeek'].apply(lambda column : days[column])
# OU
# df['Day of Week'] = df['Day of Week'].map(dmap)


print('\n\n# Seaborn - Countplot da coluna dayWeek com a tonalidade baseada na coluna reason')
sns.countplot(x='dayWeek', data=df, hue='reason', palette='viridis')
plt.legend(loc=1)
plt.show()


print('\n\n# Seaborn - Countplot da coluna month com a tonalidade baseada na coluna reason')
sns.countplot(x='month', data=df, hue='reason', palette='viridis')
plt.legend(loc=1)
plt.show()


print('\n\n# Preenchendo os meses que faltam')

print('\n\n## Count das colunas por mês')
byMonth = df.groupby('month').count()
print(byMonth.head(12))

print('\n\n## Plot simples de linha indicando a contagem de chamadas por mês')
byMonth['twp'].plot()
plt.show()

print('\n\n## Resetado o index do df - Index month passa a ser uma coluna')
byMonth = byMonth.reset_index()

print('\n\n## Seaborn - Criação de um modelo linear')
sns.lmplot(x='month', y='twp', data=byMonth)
plt.show()


print('\n\n# Nova coluna data')
df['data'] = df['timeStamp'].apply(lambda data : data.date())

print('\n\n## Agrupando a coluna data com o groupby. Usando o count () e criando um gráfico de contagens de chamadas 911')
df.groupby('data').count()['twp'].plot()
plt.show()

print('\n\n## Agrupando a coluna data com o groupby. Usando o count () e criando um gráfico de contagens de chamadas 911')
print('## Baseado na razão EMS')
df[df['reason'] == 'EMS'].groupby('data').count()['twp'].plot()
plt.show()

print('\n\n## Agrupando a coluna data com o groupby. Usando o count () e criando um gráfico de contagens de chamadas 911')
print('## Baseado na razão Traffic')
df[df['reason'] == 'Traffic'].groupby('data').count()['twp'].plot()
plt.show()

print('\n\n## Agrupando a coluna data com o groupby. Usando o count () e criando um gráfico de contagens de chamadas 911')
print('## Baseado na razão Fire')
df[df['reason'] == 'Fire'].groupby('data').count()['twp'].plot()
plt.show()


print('\n\n# Reestruturação do DF e novos plots')

print('\n\n## Reestruturando o quadro de dados para que as colunas se tornem horas e o índice se torne o Dia da Semana')
dfDayHour = df.groupby(by=['dayWeekText', 'hour']).count()['twp']
print(dfDayHour.head(100))
dfDayHour = df.groupby(by=['dayWeekText', 'hour']).count()['twp'].unstack()
print(dfDayHour.head(100))

print('\n\n## Seaborn - Criação de um mapa de calor')
sns.heatmap(data=dfDayHour)
plt.show()

print('\n\n## Seaborn - Criação de um clustermap')
sns.clustermap(data=dfDayHour)
plt.show()


print('\n\n# Reestruturação do DF e novos plots')

print('\n\n## Reestruturando o quadro de dados para que as colunas se tornem os meses e o índice se torne o Dia da Semana')
dfDayMonth = df.groupby(by=['dayWeekText', 'month'])['twp'].count().unstack()
print(dfDayMonth.head(100))

print('\n\n## Seaborn - Criação de um mapa de calor')
sns.heatmap(data=dfDayMonth)
plt.show()

print('\n\n## Seaborn - Criação de um clustermap')
sns.clustermap(data=dfDayMonth)
plt.show()
