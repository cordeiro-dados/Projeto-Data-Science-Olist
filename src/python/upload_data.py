import os
import pandas as pd
import sqlalchemy
import re
'''
# para se conectar a um banco AWS, precisa-se de:
user = 'cordeiro'
psw = 'cordeirodados'
host = 'olist.crnlhcdwos6g.us-east-1.rds.amazonaws.com'
port = '3306'
'''
# conexão com mysql
# str_connection = 'mysql+pymysql://{user}:{psw}@{host}:{port}'



# para identificar o caminho do pai do arquivo atual
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.abspath('__file__')))

# use join pois é a maneira mais segura de realizar, pois OS muda a modo da /
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Forma 2, realiza a mesma coisa, porém de forma mais elegante, esse método se chama Compressão de Listas
files_names = [i for i in os.listdir( DATA_DIR ) if i.endswith('.csv')]

# caminho da conexão local
str_connection = 'sqlite:///{path}'
# Criando a conexãol
str_connection = str_connection.format( path=os.path.join( DATA_DIR, 'olist.db') )
# str_connection = str_connection.format( user=user, psw=psw, host=host, port=port )
# Abrindo a conexão com o banco de dados
connection = sqlalchemy.create_engine( str_connection )

# Retirar Emojis e símbolos
def remove_emojis(x):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64f"  # emoticons
        u"\U0001F300-\U0001F5ff"  # symbols & pictographs
        u"\U0001F680-\U0001F6ff"  # transport & map symbols
        u"\U0001F1e0-\U0001F1ff"  # flags
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', x)

# realizo um data_quality
def data_quality(x):
    if type(x) == str:
        new_data = remove_emojis(x.replace('\n', '').replace('\r', '').replace(r'[^\w\s]', ''))
        return new_data
    else:
        return x


# para cada arquivo é realizado uma inserção no banco
for i in files_names:
    print(i)
    # dataframe temporario
    df_tmp = pd.read_csv( os.path.join(DATA_DIR, i),encoding='utf8' )
    for c in df_tmp.columns:
        df_tmp[c] = df_tmp[c].apply(data_quality)

    # removendo os nomes informados
    table_name = 'tb_' + i.strip('.csv').replace('olist_', '').replace('_dataset', '')
    df_tmp.to_sql( table_name, 
                   connection, 
                   index=False )