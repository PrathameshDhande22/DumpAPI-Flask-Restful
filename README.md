# DumpAPI

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)

DumpAPI is a Flask-Restful API that contains data of departments and their employees. The API utilizes token generation with JWT (JSON Web Tokens) for secure access. All the data is stored in a cloud database provided by Yugabyte, which offers a free PostgreSQL database service. The passwords are hashed and stored in the database for enhanced security.

## Usage

To use the DumpAPI in your system, follow the steps below:

1. Create a virtual environment for the project.
2. Install all the required dependencies using  `pip install -r requirements.txt`.
3. Add your `.env` file in the `DumpAPI` folder, containing the following data:
```
DATABASE_YUGA="your database sqlalchemy uri"
ENCRYPT_KEY="your key" (for encrypting the passwords)
JWT_KEY="your key" (for encrypting the JWT token)
```

4. Run the `run.py` file to start the API.

## Docs :

API Link : [https://dumpapi-flask-api.onrender.com/](https://dumpapi-flask-api.onrender.com/)

**Note :** Before Using Directly Call the link for booting the server as the api is hosted on [Render.com](https://render.com) after inactivity it shutdown after calling it restarts the server.

## Docs :
Docs Link  

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Attribution

![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)

## Author : Prathamesh Dhande


