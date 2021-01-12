# Flo
Flo is an auto-mixing software/algorithm built for the ELECENG 4OI6 Capstone course

# Installation
Currently Flo runs on localhost:8080, see this line in app.py to change:
`app.run(host='localhost', debug=True, port=8080)`
## Install packages
`python -m pip install requirements.txt`
## Start Server
`flask run`
## Pycharm debugging configs
![Imgur](https://i.imgur.com/LfBTmwx.png)
## Postman configs
![Imgur](https://i.imgur.com/dtBWXhH.png)
## Git workflow
Anything in {} requires you give it a name or a variable
1. Clone the repository 
    * `git clone https://github.com/4OI6Capstone/Flo.git`
2. Create a branch
    * `git checkout -b {name of branch}`
3. Check status of the git branch (ensure you are on it) **Very important command, you will use this a lot**
    * `git status`
4. Add modified files
    * `git status`
        * The files should appear in red if not added: ![Imgur](https://i.imgur.com/9WUpUOw.png)
    * `git add {name of file, you can also use **/{name of file} if you don't want to type in the whole path}`
5. Commit changes to your branch
    * `git commit -m {message}`
6. Push branch to origin (to create pull request)
    * `git push origin {name of branch}`
7. Go to Flo Repo and it should prompt you to start a pull request
## Managing new libraries and packages
It's good practice to work in a virtual environment to ensure that you aren't install packages to your whole computer and only install packages relevant to the project
1. [Follow this guide to set one up](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
2. Use `{your python command (should be python3)} -m pip install {package name}` to install packages
3. To add to requirements.txt you use `pip3 freeze > requirements.txt` then add it to your branch to push to master
