from flask import Flask, jsonify, request, render_template

class MyFlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_routes()

    def configure_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

        @self.app.route('/api/data', methods=['GET'])
        def get_data():
            return jsonify({"date": date,
                            "inex" : inex
                            ""
                            })

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    app_instance = MyFlaskApp()
    app_instance.run()
