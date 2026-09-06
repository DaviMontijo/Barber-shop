import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('barbershop.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ==========================================
# PÁGINA INICIAL
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# PAGINA DE CADASTRO E LISTAGEM DE BARBEIROS
# ==========================================
@app.route('/barbeiro', methods=['GET', 'POST'])
def barbeiro():
    conn = get_db()
    
    if request.method == 'POST':
        nome_barbeiro = request.form.get('nome_barbeiro')
        tempo_experiencia = request.form.get('tempo_experiencia')
        descricao_barbeiro = request.form.get('descricao_barbeiro')
        servicos_selecionados = request.form.getlist('servicos')

        if not nome_barbeiro or not tempo_experiencia or not descricao_barbeiro or not servicos_selecionados:
            conn.close()
            return redirect(url_for('barbeiro', mensagem_erro="Preencha todos os campos obrigatórios."))

        cursor = conn.cursor()
        cursor.execute("INSERT INTO barbeiro (nome_barbeiro, tempo_experiencia, descricao_barbeiro) VALUES (?, ?, ?)",
                       (nome_barbeiro, tempo_experiencia, descricao_barbeiro))
        id_barbeiro = cursor.lastrowid

        for id_servico in servicos_selecionados:
            cursor.execute("INSERT INTO barbeiro_servico (id_barbeiro, id_servico) VALUES (?, ?)",
                           (id_barbeiro, id_servico))

        conn.commit()
        conn.close()
        return redirect(url_for('barbeiro', mensagem_sucesso="Barbeiro cadastrado com sucesso!"))

    if request.method == 'GET': 
        termo_busca = request.args.get('q', '').strip()
        
        if termo_busca:
            barbeiros = conn.execute('''
                SELECT b.id_barbeiro, b.nome_barbeiro, b.tempo_experiencia, b.descricao_barbeiro,
                    GROUP_CONCAT(s.nome_servico, ', ') AS servicos
                FROM barbeiro b
                LEFT JOIN barbeiro_servico bs ON b.id_barbeiro = bs.id_barbeiro
                LEFT JOIN servico s ON bs.id_servico = s.id_servico
                WHERE b.nome_barbeiro LIKE ? OR b.descricao_barbeiro LIKE ?
                GROUP BY b.id_barbeiro
                ORDER BY b.nome_barbeiro
            ''', (f'%{termo_busca}%', f'%{termo_busca}%')).fetchall()
        else:
            barbeiros = conn.execute('''
                SELECT b.id_barbeiro, b.nome_barbeiro, b.tempo_experiencia, b.descricao_barbeiro,
                    GROUP_CONCAT(s.nome_servico, ', ') AS servicos
                FROM barbeiro b
                LEFT JOIN barbeiro_servico bs ON b.id_barbeiro = bs.id_barbeiro
                LEFT JOIN servico s ON bs.id_servico = s.id_servico
                GROUP BY b.id_barbeiro
                ORDER BY b.nome_barbeiro
            ''').fetchall()

        servicos = conn.execute("SELECT id_servico, nome_servico FROM servico ORDER BY nome_servico").fetchall()
        conn.close()
        
        return render_template('barbeiro.html', barbeiros=barbeiros, servicos=servicos)

# ==========================================
# PAGINA DE EDIÇÃO DE BARBEIROS
# ==========================================
@app.route("/editar_barbeiro/<int:id_barbeiro>", methods=["GET", "POST"])
def editar_barbeiro(id_barbeiro):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        nome_barbeiro = request.form.get("nome_barbeiro", "").strip()
        tempo_experiencia = request.form.get("tempo_experiencia", "").strip()
        descricao_barbeiro = request.form.get("descricao_barbeiro", "").strip()
        servicos_selecionados = request.form.getlist("servicos")

        if not nome_barbeiro or not tempo_experiencia or not descricao_barbeiro or not servicos_selecionados:
            conn.close()
            return redirect(url_for("editar_barbeiro", id_barbeiro=id_barbeiro, mensagem_erro="Preencha todos os campos."))

        try:
            tempo_experiencia = int(tempo_experiencia)
            if tempo_experiencia < 0:
                raise ValueError
        except (TypeError, ValueError):
            conn.close()
            return redirect(url_for("editar_barbeiro", id_barbeiro=id_barbeiro, mensagem_erro="Informe um tempo de experiência válido."))

        cursor.execute("""
            UPDATE barbeiro 
            SET nome_barbeiro = ?, tempo_experiencia = ?, descricao_barbeiro = ? 
            WHERE id_barbeiro = ?
        """, (nome_barbeiro, tempo_experiencia, descricao_barbeiro, id_barbeiro))

        cursor.execute("DELETE FROM barbeiro_servico WHERE id_barbeiro = ?", (id_barbeiro,))
        for id_servico in servicos_selecionados:
            cursor.execute(
                "INSERT INTO barbeiro_servico (id_barbeiro, id_servico) VALUES (?, ?)",
                (id_barbeiro, id_servico)
            )

        conn.commit()
        conn.close()
        return redirect(url_for("barbeiro", mensagem_sucesso="Barbeiro atualizado com sucesso!"))

    if request.method == "GET":
        barbeiro_dados = cursor.execute(
            "SELECT id_barbeiro, nome_barbeiro, tempo_experiencia, descricao_barbeiro FROM barbeiro WHERE id_barbeiro = ?", 
            (id_barbeiro,)
        ).fetchone()

        if not barbeiro_dados:
            conn.close()
            return redirect(url_for("barbeiro", mensagem_erro="Barbeiro não encontrado."))

        servicos = cursor.execute("SELECT id_servico, nome_servico FROM servico").fetchall()
        
        servicos_atuais = cursor.execute(
            "SELECT id_servico FROM barbeiro_servico WHERE id_barbeiro = ?", 
            (id_barbeiro,)
        ).fetchall()
        ids_servicos_atuais = [s[0] for s in servicos_atuais]

        conn.close()
        return render_template(
            "editar_barbeiro.html", 
            barbeiro=barbeiro_dados, 
            servicos=servicos, 
            ids_servicos_atuais=ids_servicos_atuais
        )

# ==========================================
# PAGINA DE EXCLUSÃO DE BARBEIROS
# ==========================================
@app.route("/excluir_barbeiro/<int:id_barbeiro>", methods=["POST"])
def excluir_barbeiro(id_barbeiro):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM barbeiro WHERE id_barbeiro = ?", (id_barbeiro,))
    conn.commit()
    conn.close()
    return redirect(url_for("barbeiro", mensagem_sucesso="Barbeiro excluído com sucesso!"))

# ==========================================
# PÁGINA DE CADASTRO E LISTAGEM DE SERVIÇOS
# ==========================================
@app.route("/servico", methods=["GET", "POST"])
def servico():
    conn = get_db()

    if request.method == "POST":
        nome_servico = request.form.get("nome_servico", "").strip()
        preco = request.form.get("preco", "").strip()
        duracao = request.form.get("duracao", "").strip()

        if not nome_servico or not preco or not duracao:
            conn.close()
            return redirect(url_for("servico", mensagem_erro="Preencha todos os campos."))

        try:
            preco = float(preco.replace(",", "."))
            if preco < 0:
                raise ValueError
        except (TypeError, ValueError):
            conn.close()
            return redirect(url_for("servico", mensagem_erro="Informe um preço válido."))

        try:
            duracao = int(duracao)
            if duracao <= 0:
                raise ValueError
        except (TypeError, ValueError):
            conn.close()
            return redirect(url_for("servico", mensagem_erro="Informe uma duração válida."))

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO servico (nome_servico, preco, duracao) VALUES (?, ?, ?)",
            (nome_servico, preco, duracao)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("servico", mensagem_sucesso="Serviço cadastrado com sucesso!"))

    if request.method == "GET":
        termo_busca = request.args.get('q', '').strip()

        if termo_busca:
            servicos = conn.execute(
                "SELECT id_servico, nome_servico, preco, duracao FROM servico WHERE nome_servico LIKE ? ORDER BY nome_servico",
                (f'%{termo_busca}%',)
            ).fetchall()
        else:
            servicos = conn.execute(
                "SELECT id_servico, nome_servico, preco, duracao FROM servico ORDER BY nome_servico"
            ).fetchall()

        conn.close()
        return render_template('servico.html', servicos=servicos)

# ==========================================
# PÁGINA DE EDIÇÃO DE SERVIÇOS
# ==========================================
@app.route("/editar_servico/<int:id_servico>", methods=["GET", "POST"])
def editar_servico(id_servico):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        nome_servico = request.form.get("nome_servico", "").strip()
        preco = request.form.get("preco", "").strip()
        duracao = request.form.get("duracao", "").strip()

        if not nome_servico or not preco or not duracao:
            conn.close()
            return redirect(url_for("editar_servico", id_servico=id_servico, mensagem_erro="Preencha todos os campos."))

        try:
            preco = float(preco.replace(",", "."))
            if preco < 0:
                raise ValueError
        except (TypeError, ValueError):
            conn.close() 
            return redirect(url_for("editar_servico", id_servico=id_servico, mensagem_erro="Informe um preço válido."))

        try:
            duracao = int(duracao)
            if duracao <= 0:
                raise ValueError
        except (TypeError, ValueError):
            conn.close()
            return redirect(url_for("editar_servico", id_servico=id_servico, mensagem_erro="Informe uma duração válida."))

        cursor.execute("""
            UPDATE servico SET nome_servico = ?, preco = ?, duracao = ? WHERE id_servico = ?
        """, (nome_servico, preco, duracao, id_servico))
        conn.commit()
        conn.close()
        return redirect(url_for("servico", mensagem_sucesso="Serviço atualizado com sucesso!"))

    if request.method == "GET":
        servico_dados = cursor.execute(
            "SELECT id_servico, nome_servico, preco, duracao FROM servico WHERE id_servico = ?", 
            (id_servico,)
        ).fetchone()

        if not servico_dados:
            conn.close()
            return redirect(url_for("servico", mensagem_erro="Serviço não encontrado."))

        conn.close()
        return render_template("editar_servico.html", servico=servico_dados)

# ==========================================
# PÁGINA DE EXCLUSÃO DE SERVIÇOS
# ==========================================
@app.route("/excluir_servico/<int:id_servico>", methods=["POST"])
def excluir_servico(id_servico):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servico WHERE id_servico = ?", (id_servico,))
    conn.commit()
    conn.close()
    return redirect(url_for("servico", mensagem_sucesso="Serviço excluído com sucesso!"))

if __name__ == "__main__":
    app.run(debug=True)