import os
import sqlalchemy
import argparse
import pandas as pd

# para identificar o caminho do pai do arquivo atual
BASE_DIR =  os.path.dirname(os.path.abspath('__file__'))

# use join pois é a maneira mais segura de realizar, pois OS muda a modo da /
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

parser = argparse.ArgumentParser()
parser.add_argument('--date_init', '-i', help='Data de inicio da extração', default='2017-06-01')
parser.add_argument('--date_end', '-e', help='Data fim da extração', default='2018-06-01')
args = parser.parse_args()

# importa a query
with open( os.path.join(SQL_DIR, 'segmentos.sql')) as query_file:
    query = query_file.read()

query = query.format( date_init = args.date_init,
                      date_end = args.date_end )

# abrindo a conexão com banco
str_connection = 'sqlite:///{path}'
str_connection = str_connection.format( path=os.path.join( DATA_DIR, 'olist.db') )
connection = sqlalchemy.create_engine( str_connection )

create_query = f'''
CREATE TABLE tb_seller_sgmt AS
 {query}
 ;'''

insert_query = f'''
DELETE FROM tb_seller_sgmt WHERE DT_SGMT = '{args.date_end}';
INSERT INTO tb_seller_sgmt SELECT
{query}
;'''

try:
    connection.execute( create_query )
except:
    connection.execute( insert_query )