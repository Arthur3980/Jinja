from flask import Flask, jsonify, request, render_template, flash
import dados
import funcoes

def menu():


        app = Flask(__name__)
        # app.config('SECRET_KEY')
        biblioteca = dados.carregar_do_arquivo()

        @app.route('/')
        def hello():
            return "Hello World!"

        @app.route('/name/<nome>', methods=['GET', 'POST'])
        def name(nome):
            return f"Olá, eu não sou o {nome}!"

        @app.route('/biblioteca', methods=['GET'])
        def lista_livros():
            return jsonify(biblioteca), 200

        @app.route('/biblioteca/<isbn>')
        def detalha_livro(isbn):
            for l in biblioteca:
                if l['isbn'] == isbn:
                    return jsonify(1)
            return jsonify ("message: livro não localizado"),404

        @app.route('/biblioteca/insert', methods=['GET', 'POST'])
        def insere_livro():
            # novo_livro = request.get_json()
            if request.method == 'POST':
                novo_livro = {
                            'isbn': request.form.get('isbn'),
                            'titulo': request.form.get('titulo'),
                            'autor': request.form.get('autor'),
                            'genero': request.form.get('genero'),
                            'ano_publicacao': request.form.get('ano_publicacao'),
                            'editora': request.form.get('editora'),
                            'paginas': request.form.get('paginas'),
                            'status': request.form.get('status'),
                            'localizacao': request.form.get('localizacao')
                    }
                for l in biblioteca:
                    if l ['isbn'] == novo_livro['isbn']:
                        return jsonify("Livro já está cadastrado"),200
                biblioteca.append(novo_livro)
                dados.salvar_no_arquivo(biblioteca)
                return render_template('biblioteca.html', biblioteca=biblioteca)
            else:
                return render_template('criar_livro.html')

        @app.route('/biblioteca/delete/<isbn>', methods = ['DELETE'])
        def detalha_livro(isbn):
            for l in biblioteca:
                if l['isbn'] == isbn:
                    biblioteca.remove(l)
                    dados.salvar_no_arquivo(biblioteca)
                    return jsonify ("message: livro deletado com sucesso"),200
            return jsonify("message: livro não localizado"),404

        @app.route('/biblioteca/update/<isbn>', methods = ['PUT', 'POST'])
        def atualiza_livro(isbn):
            for l in biblioteca:
                if l['isbn'] == isbn:
                    novo_livro = request.get_json()
                    biblioteca.remove(l)
                    biblioteca.append(novo_livro)
                    dados.salvar_no_arquivo(biblioteca)
                    return jsonify ("message: livro alterado com sucesso"),200
            return jsonify("message: livro não localizado"),404

        @app.route('/biblioteca/excluir/<isbn>', methods=['POST'])
        def excluir_livro(isbn):
            biblioteca = dados.carregar_do_arquivo()
            biblioteca = [livro for livro in biblioteca if livro['isbn'] != isbn]
            dados.salvar_no_arquivo(biblioteca)
            flash(f'Livro com ISBN {isbn} foi removido com sucesso!', 'success')
            return redirect(url_for('menu'))
        

        # if __name__ == "__main__":
        #     exibir_menu()


        if __name__ == '__main__':
            app.run(debug=True)
