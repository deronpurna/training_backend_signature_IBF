from flask import Flask

#buat variabel utama buat procfile
pelatihan_ibf_app = Flask(__name__)


@pelatihan_ibf_app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    pelatihan_ibf_app.run()