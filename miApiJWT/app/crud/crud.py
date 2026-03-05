from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "secret_key_123"

api_url = "http://localhost:5000"


@app.route('/')
def inicio():
    try:
        response = requests.get(f"{api_url}/v1/usuario/{id}")
        api = response.json()
        return render_template('crud.html', usuarios=api ['data'])
    except Exception as e:
        return f"error de conexion: {e} .revisa la conexion entre servidores "

@app.route('/eliminar/<int:id>')
def eliminar(id):
    try:
        requests.delete(f"{api_url}/v1/EliminarUsuario/{id}")
    except Exception as e:
        print(f"Error al eliminar: {e}")
    return redirect(url_for('inicio'))


@app.route('/agregar', methods=['POST'])
def agregar():
    usuario_nuevo = {
        "id": int(request.form['id']),
        "nombre": request.form['nombre'],
        "edad": int(request.form['edad'])
    }
    try:
        requests.post(f"{api_url}/v1/AgregarUsuario/{usuario_nuevo['id']}", json=usuario_nuevo)
    except Exception as e:
        print(f"Error al agregar: {e}")
    
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, port=5020)