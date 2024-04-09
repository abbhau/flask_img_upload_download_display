from flask import Flask
from io import BytesIO
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class Upload(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        filename = db.Column(db.String(50))
        data = db.Column(db.LargeBinary)
    
    db.create_all()


@app.route('/upload/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f"{file.filename} successfully Uploaded"
    return render_template('index.html')

@app.route('/download/<int:pk>/')
def download_file(pk):
    upload = Upload.query.filter_by(id=pk).first()
    return send_file(BytesIO(upload.data), download_name = upload.filename, as_attachment=True)

@app.route('/show/')
def retrieve_file():
    #upload = Upload.query.with_entities(Upload.data)
    upload = Upload.query.all()
    li = []
    for file in upload:
        encode_file = base64.b64encode(file.data).decode('utf-8')
        li.append({'data':encode_file, 'filename':file.filename })
    return render_template('photos.html', images=li)

if __name__ =="__main__":
    app.run(debug=True)