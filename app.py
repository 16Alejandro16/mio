from flask import Flask,url_for,send_file,send_from_directory,Response,make_response,stream_with_context,request,render_template
import logging
import os,mimetypes

logging.basicConfig(level=logging.INFO)

app = Flask(__name__.split(".")[0],template_folder="Templates/",static_folder="Static/")
CONFIG = app.config
CONFIG['USE_X_SENDFILE'] = True
USER_FOLDER = CONFIG["USERS_FOLDER"] = os.path.abspath("File")
DB = CONFIG["DATA_BASE"] = os.path.abspath("database/db.json")

if not os.path.exists(USER_FOLDER):
    os.makedirs("File", exist_ok=True)

if not os.path.exists(DB):
    os.makedirs("database", exist_ok=True)

if not os.path.exists(DB):
    with open(DB, 'w') as file:
        file.write("")

@app.route("/")
def root():
    response = make_response(render_template("index.html"))
    return response

@app.route("/download/beta-test", methods=["GET", "HEAD"])
def download():
    print(request.headers)
    file = os.listdir(USER_FOLDER)[0]
    url = f"{USER_FOLDER}\\{file}"
    if not os.path.exists(url):
        return "El archivo no existe o ya ha caducado",404   
    
    metadatos = os.stat(url)
    length = metadatos.st_size
    mtime = metadatos.st_mtime
    mimetype = mimetypes.guess_type(url)
    
    headers = {
            'Content-Length' : length,
            'Last-Modified' : mtime,
            
        }
    
    if request.method == "GET":       
        def generate():
            with open(url, "rb") as file:
                while(True):
                    chunk = file.read(10000)
                    if not chunk:
                        break
                    yield chunk
        return Response(generate(),status=200,content_type='application/octet-stream',headers=headers,mimetype=mimetype)
    else:
        return Response(headers=headers,mimetype=mimetype)
    
if __name__ == "__main__":
    app.run("0.0.0.0")


# app.route('/downloads/<nombre>')
# def stream_data(nombre):
#     def generate():
#         # create and return your data in small parts here
#         for i in xrange(10000):
#             yield str(i)

#     return Response(stream_with_context(generate()))