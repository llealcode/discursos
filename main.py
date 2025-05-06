import streamlit as st
from time import sleep
import pandas as pd
import sqlite3


conexao = sqlite3.connect(database='discursos.db')
cursor = conexao.cursor()
df_esbocos = pd.read_sql_query(sql="SELECT * FROM esbocos", con=conexao)

st.title('Programar discurso')
st.divider()


st.markdown(f'###### ✏️ Preencher informações do discurso')

coluna1, coluna2 = st.columns(2)

input_data = coluna1.date_input(
    label='📅 Data',
    format='DD/MM/YYYY'
)

input_numero_esboco = coluna2.number_input(
    label='🗞️ Número do esboco',
    min_value=0,
    max_value=194,
    step=1,
    key='esboco',
)

if input_numero_esboco != 0:
    df_filtrado = df_esbocos[df_esbocos['esboco'] == int(input_numero_esboco)]
    df_filtrado = df_filtrado['tema'].squeeze()

input_congregacao = st.text_input(
    label='🏠 Congregação'
)

if input_numero_esboco:
    st.markdown(f'###### 📃 {df_filtrado}')

botao_cadastrar = st.button(
    label='Cadastrar conferência',
    type='primary',
    use_container_width=True,
    icon='🎤'
)

if botao_cadastrar:

    with st.spinner(text='Aguarde...'):

        tentativa = 0

        while True:
            try:
                conexao = sqlite3.connect(database='discursos.db')
                cursor = conexao.cursor()
                sleep(1)
                cursor.execute('''
                    INSERT INTO proferidos (data, esboco, congregacao)
                    VALUES (?, ?, ?)''', (str(input_data), int(input_numero_esboco), str(input_congregacao)))
                
                conexao.commit()
                conexao.close()
                st.success('✅ Cadastrado com sucesso!')
                sleep(1)
                break
            except:
                tentativa +=1
                if tentativa == 4:
                    st.error('Falha de conexão')
                    break 

st.container(height=130, border=False)

conexao = sqlite3.connect(database='discursos.db')
df = pd.read_sql_query(sql="SELECT * FROM proferidos", con=conexao)
df['data'] = pd.to_datetime(df['data'])
df = df.drop('id', axis=1)

st.header('Discursos proferidos')

st.dataframe(
    data=df, 
    hide_index=True, 
    height=500, 
    column_config={
        'data' : st.column_config.DateColumn(label='Data', format='DD/MM/YYYY', width=50),
        'esboco' : st.column_config.NumberColumn(label='Esboço', width=20),
        'congregacao' : st.column_config.TextColumn(label='Congregação', width=170)
        },
    use_container_width=True
    )
