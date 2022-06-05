from main import create_app
from config import TestConfig

if __name__ == '__main__':
    app = create_app(TestConfig)
    app.run(debug=True, host='0.0.0.0', port=5130, use_reloader=False)
