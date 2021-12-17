from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_bcrypt import Bcrypt
from sqlalchemy import func


app = Flask(__name__)

db = SQLAlchemy(app)




app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1164@localhost:5432/bd'
#postgresql://postgres:1164@localhost:5432/bd#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#'postgresql://bpkuntuozplhyv:1946b29e86df8f0662ca8d2b9c2499a72e77396536664563d32b2b1251ce3c73@ec2-52-200-188-218.compute-1.amazonaws.com:5432/d43d8jemsfbnfd'#
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
    fecha_publicacion = db.Column(db.Date)
    n_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(255))
    volumen = db.Column(db.Integer)
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))

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
    fecha_nac = db.Column(db.Date)
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

@app.route('/fav')
def fav():
    usr = favoritos.query.join(Usuarios, Usuarios.id == favoritos.id_usuario).join(Libro, Libro.id_libro == favoritos.id_libro).add_columns(Usuarios.id, Usuarios.email, favoritos.id_libro, favoritos.id_listafav, Libro.titulo_libro, Usuarios.email)
    usr0= Usuarios.query.all()
    
    return render_template("favoritos.html", usr=usr, usr0=usr0)

@app.route('/afav/<id>')
def afav(id):
    libro =  Libro.query.filter_by(id_libro=int(id))
    usr = Usuarios.query.all()
    return render_template("aniadirfav.html", usr=usr, libro=libro)



@app.route('/afav2', methods=['POST'])
def afav2():
    id = request.form['id']
    usr = request.form['usr']
    
    fav =  favoritos(id_libro = id, id_usuario=usr )
    print (id, usr)
    db.session.add(fav)
    db.session.commit()
    return redirect('/libro')



@app.route('/buscarfav', methods=['POST'])
def buscarfav():
    ids =request.form['usr']
    usr0= Usuarios.query.all()
    usr = Usuarios.query.filter_by(id=int(ids)).join(favoritos, Usuarios.id == favoritos.id_usuario).add_columns(Usuarios.id, Usuarios.email, favoritos.id_libro, Libro.titulo_libro, Usuarios.email)
    return render_template("favoritosr.html", usr=usr, usr0 = usr0)

@app.route('/eliminarf/<id>')
def eliminarf(id):
    ls = favoritos.query.filter_by(id_listafav=int(id)).delete()
    db.session.commit()
    return redirect('/fav')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/libro')
def libro():
    libro2 = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(
        Libro.titulo_libro, Autor.nom_autor, Autor.nacionalidad, Libro.fecha_publicacion, Genero.nom_gen, Editorial.nombre_editorial, Libro.n_paginas, Libro.formato, Libro.volumen, Libro.id_libro)
    libro1 = Libro.query.all()
    consultar = Genero.query.all()
    consultar2 = Autor.query.all()
    consultar3 = Editorial.query.all()
    return render_template("libro.html", consulta0=libro2, libro1=libro1, consulta=consultar, consulta2=consultar2, consulta3=consultar3)

@app.route('/eliminarL/<id>')
def eliminar(id):
    libro = Libro.query.filter_by(id_libro=int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/libro')

@app.route('/editarL2', methods=['POST'])
def edit2():
    id = request.form['id']
    titulo = request.form['titulo']
    fecha = request.form['fecha']
    paginas = request.form['paginas']
    formato = request.form['formato']
    volumen = request.form['volumen']
    genero = request.form['genero']
    autor = request.form['autor']
    editorial = request.form['editorial']
    print(titulo, fecha, paginas, formato, volumen, genero, autor, editorial)
    Libro.query.filter_by(id_libro=int(id)).update({"titulo_libro":(titulo)})
    Libro.query.filter_by(id_libro=int(id)).update({"fecha_publicacion":(fecha)})
    Libro.query.filter_by(id_libro=int(id)).update({"n_paginas":(paginas)})
    Libro.query.filter_by(id_libro=int(id)).update({"formato":(formato)})
    Libro.query.filter_by(id_libro=int(id)).update({"volumen":(volumen)})
    Libro.query.filter_by(id_libro=int(id)).update({"id_genero":(genero)})
    Libro.query.filter_by(id_libro=int(id)).update({"id_autor":(autor)})
    Libro.query.filter_by(id_libro=int(id)).update({"id_editorial":(editorial)})
    db.session.commit()
    return redirect('/libro')

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

    return redirect('/libro')


@app.route('/editarL1/<id>')
def edit1(id):
    consultar1= Genero.query.all()
    consultar2 = Autor.query.all()
    consultar3 = Editorial.query.all()
    fav = Usuarios.query.all()
    libro1 = Libro.query.filter_by(id_libro=int(id)).all()
    return render_template('libroedit.html', consulta=libro1, consulta1=consultar1, consulta2=consultar2, consulta3=consultar3, fav=fav)





#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#





@app.route('/autor')
def autor():
    aut = Autor.query.all()
    return render_template("autor.html", consulta=aut)

@app.route('/agregarautor', methods=['POST'])
def agregarautor():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    nac = request.form['nac']
    autor = Autor(nom_autor=nombre, fecha_nac=fecha, nacionalidad=nac)
    db.session.add(autor)
    db.session.commit()

    return redirect('/autor')


@app.route('/eliminarA/<id>')
def eliminarA(id):
    libro = Autor.query.filter_by(id_autor=int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/autor')

@app.route('/editarA2', methods=['POST'])
def editA2():
    id = request.form['id']
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    nac = request.form['nac']
    Autor.query.filter_by(id_autor=int(id)).update({"nom_autor":(nombre)})
    Autor.query.filter_by(id_autor=int(id)).update({"fecha_nac":(fecha)})
    Autor.query.filter_by(id_autor=int(id)).update({"nacionalidad":(nac)})
    
    db.session.commit()
    return redirect('/autor')


@app.route('/editarA1/<id>')
def editA1(id):
    autor = Autor.query.filter_by(id_autor=int(id)).all()
    print(autor)
    return render_template('autoredit.html', consulta=autor)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.route('/genero')
def genero():
    gen = Genero.query.all()
    return render_template("genero.html", consulta=gen)


@app.route('/agregargenero', methods=['POST'])
def agregargenero():
    nombre = request.form['nombre']
    gen = Genero(nom_gen=nombre)
    db.session.add(gen)
    db.session.commit()
    return redirect('/genero')

@app.route('/eliminarG/<id>')
def eliminarG(id):
    gen = Genero.query.filter_by(id_genero=int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/genero')

@app.route('/editarG2', methods=['POST'])
def editG2():
    id = request.form['id']
    nombre = request.form['nombre']
    Genero.query.filter_by(id_genero=int(id)).update({"nom_gen":(nombre)})
    db.session.commit()
    return redirect('/genero')


@app.route('/editarG1/<id>')
def editG1(id):
    libro1 = Genero.query.filter_by(id_genero=int(id)).all()
    return render_template('generoedit.html', consulta=libro1)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.route('/editorial')
def editorial():
    edi = Editorial.query.all()
    return render_template("editorial.html", consulta=edi)

@app.route('/agregareditorial', methods=['POST'])
def agregareditoril():
    nombre = request.form['nombre']
    edit = Editorial(nombre_editorial=nombre)
    db.session.add(edit)
    db.session.commit()

    return redirect('/editorial')

@app.route('/eliminarE/<id>')
def eliminarE(id):
    libro = Libro.query.filter_by(id_libro=int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/editorial')

@app.route('/editarE2', methods=['POST'])
def editE2():
    id = request.form['id']
    nombre = request.form['nombre']
    Editorial.query.filter_by(id_editorial=int(id)).update({"nombre_editorial":(nombre)})
    
    db.session.commit()
    return redirect('/editorial')


@app.route('/editarE1/<id>')
def editE1(id):
    libro1 = Editorial.query.filter_by(id_editorial=int(id)).all()
    return render_template('editorialedit.html', consulta=libro1)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    consulta = Usuarios.query.filter_by(email=email).first()
    if consulta == None:
       return redirect('/')
    else:
        bcrypt.check_password_hash(consulta.password, password)
        return redirect('/paginap')

@app.route('/paginap')
def paginap():
    consultar = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(
        Libro.titulo_libro, Autor.nom_autor, Autor.nacionalidad, Libro.fecha_publicacion, Genero.nom_gen, Editorial.nombre_editorial, Libro.n_paginas, Libro.formato, Libro.volumen, Libro.id_libro)
    return render_template("otroindex.html", consulta=consultar)



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


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
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



    





if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
