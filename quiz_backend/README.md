## GETTING STARTED
1. Clone this repository by giving this command: git clone https://github.com/JaziBro/quiz_app.git
2. In your terminal of VsCode, download all the required dependencies present in pyproject.toml by giving the command: poetry add
3. Run the command: poetry run uvicorn quiz_backend.main:app --reload
4. It will start giving logs in terminal and after some time, it will give the host: http://127.0.0.1:8000
5. Copy and paste this host url to any browser's search bar
6. This will open the main route "/" of project, printing "Welcome Home"
7. add this route "/docs" to the host url in search bar
8. This will take you to Mock Server of FastAPI i.e Swagger FastAPI
9. Here you will find every route in present in my main.py file
10. First select the user_signup route with POST http endpoint, then click Execute to try it out. 
11. It will ask you for email, password and user_name. Enter all these fields
12. If succesful, then you can select user_login route and enter your email and password to login.