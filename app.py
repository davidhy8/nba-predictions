from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()

print("Hi")

# TO DO LIST:
# 1. Familiarize with the use of Github
# 2. Learn how to create a Flask project. You will also have to learn basic HTML, CSS, and Javascript
# 3. Create a framework for the project, and then we will fill in each file with code