from flask import Flask, render_template, url_for, request, redirect
import os
from banco import conexao
import base64

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    conn = conexao()
    especie = conn.execute("SELECT * FROM especie WHERE ativo=1").fetchall()
    animal = conn.execute("SELECT * FROM animal").fetchall()
    conn.close()
    return render_template("site/index.html", animal=animal, especie=especie)

@app.route("/animais")
def animais():
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE ativo=1").fetchall()
    conn.close()
    return render_template("site/animais.html", animal=animal)

@app.route("/animais_adotados")
def animais_adotados():
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE ativo=0").fetchall()
    conn.close()
    return render_template("site/animais_adotados.html", animal=animal)

@app.route("/categ_animais/<int:id>")
def categAnimais(id):
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE id_especie=? and ativo=1", (id,)).fetchall()
    conn.close()
    return render_template("site/categ_animais.html", animal=animal)

@app.route("/ficha_animais/<int:id>")
def fichaAnimais(id):
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE id=? and ativo=1", (id,)).fetchone()
    conn.close()
    return render_template("site/ficha_animais.html", animal=animal)

@app.route("/adotar/<int:id>", methods=("GET", "POST"))
def adotar(id):
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        endereco = request.form.get("endereco")
        id_animal = id

        conn.execute('''INSERT INTO adocao (nome, telefone, email, endereco, id_animal)
                        VALUES (?, ?, ?, ?, ?)''', (nome, telefone, email, endereco, id_animal))
        conn.commit()
        conn.close()
    return render_template("site/adotar.html", animal=animal)

@app.route("/admin")
def admin():
    return render_template("admin/index.html")

@app.route("/admin/listar_especies")
def listarEspecies():
    conn = conexao()
    especie = conn.execute("SELECT * FROM especie").fetchall()
    conn.close()
    return render_template("admin/listar_especies.html", especie=especie)

@app.route("/admin/listar_animais")
def listarAnimais():
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal").fetchall()
    especie = conn.execute("SELECT * FROM especie").fetchall()
    conn.close()
    return render_template("admin/listar_animais.html", animal=animal, especie=especie)

@app.route("/admin/cadastrar_especies", methods=("GET", "POST"))
def cadastrarEspecies():
    conn = conexao()
    especie = conn.execute("SELECT * FROM especie").fetchall()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")
        imagem = request.files.get("img")

        if imagem:
            imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")

            if nome:
                conn.execute('''INSERT INTO especie (nome, descricao, img, ativo)
                                VALUES (?, ?, ?, ?)''', (nome, descricao, imagem_base64, ativo))
                conn.commit()
                conn.close()
                return redirect(url_for("listarEspecies"))
    return render_template("admin/cadastrar_especies.html", especie=especie)

@app.route("/admin/cadastrar_animais", methods=("GET", "POST"))
def cadastrarAnimais():
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal").fetchall()
    especie = conn.execute("SELECT * FROM especie").fetchall()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo") 
        imagem = request.files.get("img")
        imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8") if imagem else None
        porte = request.form.get("porte")
        sexo = request.form.get("sexo")
        castrado = request.form.get("castrado")
        raca = request.form.get("raca")
        faixa_etaria = request.form.get("faixa_etaria")
        comportamento = request.form.get("comportamento")
        id_especie = request.form.get("id_especie")

        if nome:
            conn.execute('''INSERT INTO animal (nome, descricao, img, ativo, porte, sexo, castrado, raca, faixa_etaria, comportamento, id_especie)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (nome, descricao, imagem_base64, ativo, porte, sexo, castrado, raca, faixa_etaria, comportamento, id_especie))
            conn.commit()
            conn.close()
            return redirect(url_for("listarAnimais"))
    return render_template("admin/cadastrar_animais.html", animal=animal, especie=especie)

@app.route("/admin/editar_especies/<int:id>", methods=("GET", "POST"))
def editarEspecies(id):
    conn = conexao()
    especie = conn.execute("SELECT * FROM especie WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo")
        imagem = request.files.get("img")
        
        if imagem:
            imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
            conn.execute('UPDATE especie SET nome=?, descricao=?, ativo=?, img=? WHERE id=?', (nome, descricao, ativo, imagem_base64, id))
        else:
            conn.execute('UPDATE especie SET nome=?, descricao=?, ativo=? WHERE id=?', (nome, descricao, ativo, id))

        conn.commit()
        conn.close()
        return redirect(url_for("listarEspecies"))
    
    return render_template("admin/editar_especies.html", especie=especie)

@app.route("/admin/editar_animais/<int:id>", methods=("GET", "POST"))
def editarAnimais(id):
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE id=?", (id,)).fetchone()
    especie = conn.execute("SELECT * FROM especie").fetchall()

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ativo = request.form.get("ativo") 
        imagem = request.files.get("img")
        porte = request.form.get("porte")
        sexo = request.form.get("sexo")
        castrado = request.form.get("castrado")
        raca = request.form.get("raca")
        faixa_etaria = request.form.get("faixa_etaria")
        comportamento = request.form.get("comportamento")
        id_especie = request.form.get("id_especie")

        if imagem:
            imagem_base64 = base64.b64encode(imagem.read()).decode("utf-8")
            conn.execute('UPDATE animal SET nome=?, descricao=?, img=?, ativo=?, porte=?, sexo=?, castrado=?, raca=?, faixa_etaria=?, comportamento=?, id_especie=? WHERE id=?', (nome, descricao, imagem_base64, ativo, porte, sexo, castrado, raca, faixa_etaria, comportamento, id_especie, id))
        else:
            conn.execute('UPDATE animal SET nome=?, descricao=?, ativo=?, porte=?, sexo=?, castrado=?, raca=?, faixa_etaria=?, comportamento=?, id_especie=? WHERE id=?', (nome, descricao, ativo, porte, sexo, castrado, raca, faixa_etaria, comportamento, id_especie, id))

        conn.commit()
        conn.close()
        return redirect(url_for("listarAnimais"))
    return render_template("admin/editar_animais.html", animal=animal, especie=especie)

@app.route("/admin/excluir_especies/<int:id>", methods=("GET", "POST"))
def excluirEspecies(id):
    conn = conexao()
    especie = conn.execute("SELECT * FROM especie WHERE id=?", (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM especie WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarEspecies"))

    conn.close()
    return render_template("admin/excluir_especies.html", especie=especie)

@app.route("/admin/excluir_animais/<int:id>", methods=("GET", "POST"))
def excluirAnimais(id):
    conn = conexao()
    animal = conn.execute("SELECT * FROM animal WHERE id=?", (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM animal WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("listarAnimais"))

    conn.close()
    return render_template("admin/excluir_animais.html", animal=animal)

@app.route("/admin/adocao")
def pedidoAdocao():
    conn = conexao()
    adocao = conn.execute("SELECT * FROM adocao").fetchall()
    animal = conn.execute("SELECT * FROM animal").fetchall()
    conn.close()
    return render_template("admin/adocao.html", adocao=adocao, animal=animal)

app.run(debug=True)
