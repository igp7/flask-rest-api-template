# Configuracion APP
APP_NAME=Flask API Rest Template
APP_ENV=production

# Configuracion Flask
API_ENTRYPOINT=app:app
APP_SETTINGS_MODULE=config.ProductionConfig

# Configuracion de servicio API
API_HOST=0.0.0.0

# Configuracion de servicio BBDD
DATABASE_URL=sqlite:///production.db

# Plataforma de deploy
PLATFORM_DEPLOY=heroku