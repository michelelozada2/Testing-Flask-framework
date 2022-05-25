from flask import Flask, render_template, g
import sqlite3

DATABASE = "banco.bd"
SECRET_KEY = "chave"

app = Flask('Hello')
app.config.from_object(__name__)
def conecta_bd():
    return sqlite3.connect(DATABASE)  #retona conexão com o BD. 
    
@app.before_request # antes da requisição
def antes_requisicao():
    g.bd = conecta_bd() #abrir comexão com banco.  guarda nesta variável a conexão com banco.

@app.teardown_request # depois da requisição | fechar conexão com bd 
def depois_requisicao(e):  # recebe parâmetro | ref. tratamento de exceções
    g.bd.close()

#Rotas
@app.route('/') # Home - rota raiz
def exibir_entradas():
    sql = "SELECT titulo,texto,criado_em FROM entradas ORDER BY id DESC;"
    cur = g.bd.execute(sql)  #resposta da execução
    entradas = []
    for titulo, texto, criado_em in cur.fetchall():
        entradas.append({"titulo": titulo, "texto": texto, "criado_em": criado_em})
    return render_template("layout.html", entradas=entradas)


@app.route('/hello')
def hello():
    return render_template('hello.html')  # pegar o que está em hello.html

@app.route('/tchau')
def tchau():
    return 'Tchau' 