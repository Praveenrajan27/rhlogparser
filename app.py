import connexion


# Instantiate App
app = connexion.App(__name__)

#Adding swagger spec
app.add_api('spec/swagger.yaml')
app.app.config.from_object('config.DevConfig')
application = app.app

if __name__ == '__main__':
    app.run()


