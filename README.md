# SimapleBot

### This bot was created to teach my friends how to deploy a telegram on the [heroku](https://heroku.com)

#### So let's get started

- First of all be sure that [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and [git](https://git-scm.com/downloads) are installed on your computer

- Now create a new account in [heroku](https://id.heroku.com/signup/login)
- open a terminal and write heorku login
- create a new app usuing the follwing command heroku create <your-app-name>
- - Change the Stack for the App using Heroku CLI:
```
heroku stack:set container --app <your-app-name>
```
- Initialise the project files as a Git Repository, push the Repo to 'Heroku Git' and build the Docker Image:
```
