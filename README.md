
# FastAPI CRUD
This is a Social media CRUD Api with a feature to Vote on posts and bearer authentication created with the FastAPI framework.

- To run this program, first clone this repo, cd into the folder and create a virtual environment

> python -m venv venv

Next to install all the packages used in this program, please run:

> pip install -r requirements.txt 

- Once all the packages are installed, `cd..` into `apidemo`
> cd apidemo

- Create a '.env' file and add your environment configs listed in the `config.py` to the '.env' file.

- Run `uvicorn app.main:app --reload` to start your program in localhost.

- Open the link '(CTRL + click)' provided in your terminal and add '/docs' to open the Swagger UI to test all the endpoints in this api.
