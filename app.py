
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_bcrypt import Bcrypt
from sqlalchemy import func


app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bpkuntuozplhyv:1946b29e86df8f0662ca8d2b9c2499a72e77396536664563d32b2b1251ce3c73@ec2-52-200-188-218.compute-1.amazonaws.com:5432/d43d8jemsfbnfd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)


class Editorial (db.Model):
    __tablename__ = 'editorial'
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial


class Libro(db.Model):
    __tablename__ = 'libro'
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(150))
    fecha_publicacion = db.Column(db.DateTime)
    n_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(255))
    volumen = db.Column(db.Integer)
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_editorial = db.Column(
        db.Integer, db.ForeignKey("editorial.id_editorial"))

    def __init__(self, titulo_libro, fecha_publicacion, n_paginas, formato, volumen, id_genero, id_autor, id_editorial):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.n_paginas = n_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_genero = id_genero
        self.id_autor = id_autor
        self.id_editorial = id_editorial


class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nom_autor = db.Column(db.String(150))
    fecha_nac = db.Column(db.DateTime)
    nacionalidad = db.Column(db.String(150))

    def __init__(self, nom_autor, fecha_nac, nacionalidad):
        self.nom_autor = nom_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad


class Genero(db.Model):
    __tablename__ = 'genero'
    id_genero = db.Column(db.Integer, primary_key=True)
    nom_gen = db.Column(db.String(150))

    def __init__(self, nom_gen):
        self.nom_gen = nom_gen


class favoritos(db.Model):
    __tablename__ = 'favoritos'
    id_listafav = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    def __init__(self, id_libro, id_usuario):
        self.id_libro = id_libro
        self.id_usuario = id_usuario


class Usuarios (db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __int__(self, email, password):
        self.email = email
        self.password-password


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/libro')
def libro():
    libro2 = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(
        Libro.titulo_libro, Autor.nom_autor, Autor.nacionalidad, Libro.fecha_publicacion, Genero.nom_gen, Editorial.nombre_editorial, Libro.n_paginas, Libro.formato, Libro.volumen, Libro.id_libro)
    libro1 = Libro.query.all()
    consultar = Genero.query.all()
    consultar2 = Autor.query.all()
    consultar3 = Editorial.query.all()
    return render_template("libro.html", consulta0=libro2, consulta1=libro1, consulta=consultar, consulta2=consultar2, consulta3=consultar3)


@app.route('/autor')
def autor():
    aut = Autor.query.all()
    return render_template("autor.html", consulta=aut)


@app.route('/genero')
def genero():
    gen = Genero.query.all()
    return render_template("genero.html", consulta=gen)


@app.route('/editorial')
def editorial():
    edi = Editorial.query.all()
    return render_template("editorial.html", consulta=edi)


@app.route('/agregarautor', methods=['POST'])
def agregarautor():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    nac = request.form['nac']
    autor = Autor(nom_autor=nombre, fecha_nac=fecha, nacionalidad=nac)
    db.session.add(autor)
    db.session.commit()

    return redirect('/paginap')


@app.route('/agregareditorial', methods=['POST'])
def agregareditoril():
    nombre = request.form['nombre']
    edit = Editorial(nombre_editorial=nombre)
    db.session.add(edit)
    db.session.commit()

    return redirect('/paginap')


@app.route('/agregargenero', methods=['POST'])
def agregargenero():
    nombre = request.form['nombre']
    gen = Genero(nom_gen=nombre)
    db.session.add(gen)
    db.session.commit()
    return redirect('/paginap')


@app.route('/paginap')
def paginap():
    consultar = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(
        Libro.titulo_libro, Autor.nom_autor, Autor.nacionalidad, Libro.fecha_publicacion, Genero.nom_gen, Editorial.nombre_editorial, Libro.n_paginas, Libro.formato, Libro.volumen, Libro.id_libro)
    return render_template("otroindex.html", consulta=consultar)


@app.route('/agregarlibro', methods=['POST'])
def agregarlibro():
    titulo = request.form['titulo']
    fecha = request.form['fecha']
    paginas = request.form['paginas']
    formato = request.form['formato']
    volumen = request.form['volumen']
    genero = request.form['genero']
    autor = request.form['autor']
    editorial = request.form['editorial']
    libro = Libro(titulo_libro=titulo, fecha_publicacion=fecha, n_paginas=paginas, formato=formato,
                  volumen=volumen, id_genero=genero, id_autor=autor, id_editorial=editorial)
    db.session.add(libro)
    db.session.commit()

    return redirect('/paginap')


@app.route("/registrar")
def registrar():
    return render_template("registro.html")


@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    email = request.form['email']
    password = request.form['password']
    password_cif = bcrypt.generate_password_hash(password).decode('utf8')
    user = Usuarios(email=email, password=password_cif)
    db.session.add(user)
    db.session.commit()
    return render_template("index.html")


@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    consulta = Usuarios.query.filter_by(email=email).first()
    bcrypt.check_password_hash(consulta.password, password)
    return redirect('/paginap')


@app.route('/eliminarL/<id>')
def eliminar(id):
    libro = Libro.query.filter_by(id_libro=int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/libro')

@app.route('/editarL2/<id>', methods=['POST'])
def edit2(id):
    titulo = request.form['titulo']
    fecha = request.form['fecha']
    paginas = request.form['paginas']
    formato = request.form['formato']
    volumen = request.form['volumen']
    genero = request.form['genero']
    autor = request.form['autor']
    editorial = request.form['editorial']
    libro = Libro.query.update(titulo, fecha, paginas, formato, volumen, genero, autor, editorial).filter_by(id_libro=int(id))
    libro = Libro.query.filter_by(id_libro=int(id))
    print(libro)
    db.session.commit()
    return redirect('/libro')


@app.route('/editarL1/<id>')
def edit1(id):
    libro1 = Libro.query.filter_by(id_libro=int(id)).all()
    return render_template('libroedit.html', consulta=libro1)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


# class Notas(db.Model):
#     '''Clase Notas'''
#     __tablename__ = "notas"
#     idNota = db.Column(db.Integer, primary_key=True)
#     tituloNota = db.Column(db.String(80))
#     cuerpoNota = db.Column(db.String(200))

#     def __init__(self, tituloNota, cuerpoNota):

#         self.tituloNota = tituloNota
#         self.cuerpoNota = cuerpoNota


# @app.route('/')
# def index():

#     for nota in consultar:
#         print(nota.tituloNota)
#         print(nota.cuerpoNota)
#     return render_template('index.html', consulta=consultar)


# @app.route('/about')
# def about():
#     return render_template('about.html')


# @app.route('/createnote', methods=['POST'])
# def createnote():
#     ctitulo = request.form['titulo']
#     ccontenido = request.form['contenido']
#     notaNueva = Notas(tituloNota=ctitulo, cuerpoNota=ccontenido)
#     db.session.add(notaNueva)
#     db.session.commit()
#     return redirect('/')
#     # return 'nota creada ' + titulo +' ' + contenido


# @app.route('/leernotas')
# def leernotas():
#     consultar = Notas.query.all()
#     print(consultar)
#     for nota in consultar:
#         print(nota.tituloNota)
#         print(nota.cuerpoNota)
#     # return "Notas consultadas"
#     return render_template("index.html", consulta=consultar)


# @app.route('/eliminarN/<id>')
# def eliminar(id):
#     nota = Notas.query.filter_by(idNota=int(id)).delete()
#     print(nota)
#     db.session.commit()
#     return redirect('/')


# @app.route('/editarN/<id>')
# def editar(id):
#     nota = Notas.query.filter_by(idNota=int(id)).first()
#     print(nota)
#     return render_template("edittemplate.html", nota=nota)


# @app.route('/editnote', methods=['POST'])
# def editnore():
#     ctitulo = request.form['titulo']
#     ccontenido = request.form['contenido']
#     cid = request.form['id']
#     notaM = Notas.query.filter_by(idNota=int(cid)).first()
#     notaM.tituloNota = ctitulo
#     notaM.cuerpoNota = ccontenido
#     db.session.commit()
#     return redirect('/')
#     # return 'nota creada ' + titulo +' ' + contenido
