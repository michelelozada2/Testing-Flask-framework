from flask import Flask, render_template, g, request, session, redirect, flash, url_for, abort
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
    return render_template("exibir_entradas.html", entradas=entradas)

@app.route('/inserir,' methods=["POST"])
def inserir_entradas():
    if not session.get('logado'):
        abort(401)  #abortando a requisição e dando página de erro
    ttulo = request.form['titulo']    
    texto = request.form['texto']
    sql = "INSERT INTO entradas (titulo, texto) VALUES (?,?)" 
    g.bd.execute(sql,[titulo,texto])
    g.bd.commit()
    flash('Nova entrada gravada com sucesso!')
    return redirect(url_for('exibir_entradas'))

@app.route('/login',methods=["GET","POST"]) #habilitar para receber POST
def login():
    erro = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logado'] = True
            flash('Login efetuado com sucesso')
            return redirect(url_for('exibir_entradas'))
        erro = "Usuário ou senha inválidos"   
    return render_template('login.html',erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado', None)
    flash('Logaout efetuado com sucesso')
    return redirect(url_for('exibir_entradas'))