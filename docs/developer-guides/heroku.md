# Heroku

## purplship Deployment

To deploy purplship to Heroku, create a new Heroku app and configure your 
[purplship-heroku](https://github.com/purplship/purplship-heroku) git repository with
Heroku app using:

```terminal
git clone https://github.com/purplship/purplship-heroku.git
cd purplship-heroku
heroku git:remote -a '<purplship-app name>'
heroku buildpacks:add heroku/python
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set ALLOWED_HOSTS='<your hosts here>'
heroku config:set USE_HTTPS=True
heroku config:set DEBUG_MODE=True
heroku config:set SECRET_KEY='<your secret key here>'
```

`ALLOWED_HOSTS are required to properly setup CORS headers. 
SECRET_KEY is used by Django to store your secret data, 
it should have a cryptographically strong amount of entropy in case of production deployments.`

You can now deploy using

```terminal
git push heroku main
```

Heroku will install and deploy purplship automatically.

## Setting up the database with initial data

```terminal
heroku run -a '<purplship-app name>' purplship createsuperuser
```

## How to log in to purplship Dashboard

Once the purplship Server app has been created on Heroku, you can log in via the URL 
<purplship-app name>.herokuapp.com using the admin account.
