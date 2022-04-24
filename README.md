# Flask API REST Template
Template de API Rest desarrollada en Python con el framework Flask. El template cubre la de gestión de usuarios
y tokens jwt para autenticación. Cuenta con 4 entornos develop, testing, local, producción. En el entorno local utiliza 
docker para crear un entorno formado por varios servicios como api (flask), database (postgresql), swagger (swagger-ui), proxy-inverso (nginx), 
cron para realizar backups de la base de datos de forma automática. En el entorno de producción se utiliza la 
plataforma heroku, mediante el workflow [pro.yml](./.github/workflows/pro.yml) se realiza el despliegue.

## Indice
- [Tecnología](#tecnología)
- [Requisitos](#requisitos)
- [Swagger](#swagger)
- [Entornos](#entornos)
   - [Develop](#develop)
   - [Testing](#testing)
   - [Local](#local)
   - [Producción](#producción)
- [Backups](#backups)
- [Comandos de Flask](#comandos-de-flask)
  - [Flask-cli](#flask-cli)
- [Comandos de BBDD](#comandos-de-bbdd)
  - [Flask-migrate](#flask-migrate)
- [Endpoints](#endpoints)
  - [Users](#users)
  - [Auth](#auth)
- [CI-CD](#ci-cd)
   - [CI (Continuous Integration)](#ci-continuous-integration)
   - [CD (Continuous deployment)](#cd-continuous-deployment)
- [Ejemplo de expansion de este template](#ejemplo-de-expansion-de-este-template)
- [Aviso de descargo de responsabilidad](#aviso-de-descargo-de-responsabilidad)
- [Contribución](#contribución)

## Tecnología
- **Web Framework:** Flask
- **ORM:** Flask-sqlalchemy
- **Swagger:** Swagger-UI
- **Autenticación:** JSON Web Token
- **Serialización, Deserialización y Validación:** Marshmallow con el módulo flask-marshmallow
- **Migración BBDD:** Flask-migrate
- **Authentication:** Flask-jwt-extended
- **Gestor de environments:** Pipenv
- **Contenirizacion:** Docker y docker-compose
- **Base De Datos:** PostgreSQL y SQLite
- **Python WSGI HTTP Server:** Gunicorn
- **Proxy:** Nginx
- **Cobertura de código:** Coverage
- **Tests:** Unittest
- **Plataforma de deploy:** Heroku
- **CI/CD:** Github Actions

## Requisitos
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [Docker](https://www.docker.com/get-started)
- [Docker-Compose](https://docs.docker.com/compose/install/)
- [Python 3.8](https://www.python.org/downloads/)
- [Github](https://github.com)
- [Heroku](https://www.heroku.com)

## Swagger
Visualización del Swagger en **entorno local**:
- Petición GET en la ruta **\<url\>:8080/docs/**.

## Entornos
### Develop
Entorno de desarrollo que usa como BBDD SQLite (develop.db) y utiliza el servidor que incorpora flask en modo debug.
1. Crear environment e instalar paquetes:
   ```shell
   pipenv install
   ```
2. Crear fichero **.env** e introducir las variables de entorno del environment. Ejemplo:
   ```shell
   # Configuracion APP
   APP_NAME="[Name APP]"
   APP_ENV="develop"
   
   # Configuracion Flask
   FLASK_APP= "app:app"
   FLASK_ENV="development"
   APP_SETTINGS_MODULE="config.DevelopConfig"
   APP_TEST_SETTINGS_MODULE="config.TestingConfig"
   FLASK_RUN_HOST=<api_host>  # Por ejemplo "0.0.0.0"
   
   # Configuracion de servicio BBDD
   DATABASE_URL="sqlite:///develop.db"
   DATABASE_TEST_URL="sqlite:///testing.db"
   ```
3. Ejecutar:
   ```shell
   pipenv run flask
   ```
**NOTA:** La API Rest usa el host *localhost* y el puerto *5000*.

### Testing
Entorno de testing que usa como BBDD SQLite (testing.db) y realiza tests unitarios, tests de integración y tests de API.
1. Crear environment e instalar paquetes:
   ```shell
   pipenv install
   ```

2. Crear fichero **.env** e introducir las variables de entorno del environment. Ejemplo:
   ```shell
   # Configuracion APP
   APP_NAME="[Name APP]" # Por ejemplo Flask API Rest Template
   APP_ENV="develop"
   
   # Configuracion Flask
   FLASK_APP= "app:app"
   FLASK_ENV="development"
   APP_SETTINGS_MODULE="config.DevelopConfig"
   APP_TEST_SETTINGS_MODULE="config.TestingConfig"
   FLASK_RUN_HOST=<api_host>  # Por ejemplo "0.0.0.0"
   
   # Configuracion de servicio BBDD
   DATABASE_URL="sqlite:///develop.db"
   DATABASE_TEST_URL="sqlite:///testing.db"
   ```

3. Ejecutar todos los tests:
   ```shell
   pipenv run tests
   ```

4. Ejecutar tests unitarios:
   ```shell
   pipenv run tests_unit
   ```

5. Ejecutar tests de integración:
   ```shell
   pipenv run tests_integration
   ```

6. Ejecutar tests de API:
   ```shell
   pipenv run tests_api
   ```

7. Ejecutar cobertura:
   ```shell
   pipenv run coverage
   ```

8. Ejecutar report de cobertura:
   ```shell
   pipenv run coverage_report
   ```
**NOTA:** La API Rest usa el host *localhost* y el puerto *5000*.

### Local
Servicios contenerizados de forma separada con BBDD PostgreSQL (db), API (api), SwaggerUI (docs) y Proxy inverso Nginx (nginx) con Docker y docker-compose.

1. Crear environment e instalar paquetes:
   ```shell
   pipenv install
   ```

2. Crear ficheros **.env.api.local**, **.env.db.local** y **.env.cron.local** e introducir las variables de entorno para
   cada servicio. En el entorno local hay 5 servicios (api, bd, docs, nginx, cron). Por ejemplo:
   1. **.env.api.local**:
      ```shell
      # Configuracion APP
      APP_NAME=[Name APP] # Por ejemplo Flask API Rest Template
      APP_ENV=local
      
      # Configuracion Flask
      API_ENTRYPOINT=app:app
      APP_SETTINGS_MODULE=config.LocalConfig
      APP_TEST_SETTINGS_MODULE=config.TestingConfig
      
      # Configuracion de servicio API
      API_HOST=<api_host>  # Por ejemplo 0.0.0.0
      API_PORT=<port_api> # Por ejemplo 5000
      
      # Configuracion de servicio BBDD
      BBDD_HOST=<name_container_bbdd> # Por ejemplo db (name service en docker-compose)
      BBDD_PORT=<port_container_bbdd> # Por ejemplo 5432 (port service en docker-compose)
      DATABASE=postgres
      DATABASE_TEST_URL=<url bbdd test> # Por ejemplo postgresql+psycopg2://db_user:db_password@db:5432/db_test
      DATABASE_URL=<url bbdd> # Por ejemplo postgresql+psycopg2://db_user:db_password@db:5432/db_demo
      ```
   2. **.env.db.local**:
      ```shell
      # Esta variable de entorno (opcional) se utiliza junto con POSTGRES_PASSWORD para establecer un usuario y su contraseña.
      # Esta variable creará el usuario especificado con poder de superusuario y una base de datos con el mismo nombre.
      # Si no se especifica, se utilizará el usuario por defecto de postgres.
      POSTGRES_USER=<name_user> # Por ejemplo db_user
      
      # Esta variable de entorno es IMPRESCINDIBLE para utilizar la imagen de PostgreSQL. No debe estar vacía ni indefinida.
      # Esta variable de entorno establece la contraseña de superusuario para PostgreSQL.
      # El superusuario por defecto está definido por la variable de entorno POSTGRES_USER.
      POSTGRES_PASSWORD=<password> # Por ejemplo db_password
      
      # La variable de entorno POSTGRES_DB (opcional) puede utilizarse para definir un nombre diferente para la base de datos
      # por defecto que se crea cuando la imagen se inicia por primera vez. Si no se especifica, se utilizará el valor de POSTGRES_USER.
      # POSTGRES_DB=<name_BBDD> # Por ejemplo db_demo
      
      # La variable de entorno POSTGRES_DATABASES (IMPRESCINDIBLE) define un nombre diferente para la base de datos por defecto
      # se crea cuando la imagen se inicia por primera vez.
      POSTGRES_DATABASES=<name_BBDD>[,<name_BBDD>,...] # Por ejemplo db_demo,db_test
      ```
   3. **.env.cron.local**:
      ```shell
      # Configuracion de servicio BBDD backups

      # Usuario para acceder al servidor bbdd, ejemplo root
      BBDD_USER=<name_user> # Por ejemplo root
        
      # Password para acceder a la bbdd postgresql
      PGPASSWORD=<password> # Por ejemplo password
        
      # Host name (o IP address) de PostgreSQL server, ejemplo localhost
      BBDD_HOST=<host> # Por ejemplo db (name service en docker-compose)
        
      # Port de PostgreSQL server, ejemplo 5432
      BBDD_PORT=<port> # Por ejemplo 5432 (port service en docker-compose)
        
      # Tipo de bbdd
      DATABASE=<tipo_database> # Por ejemplo postgres
        
      # List of DBNAMES for Daily/Weekly Backup e.g. "DB1 DB2 DB3"
      BACKUPS_DBNAMES=<tables> # Por ejemplo all
        
      # Backup directory location e.g /backups
      BACKUPS_BACKUPDIR=<dir_backups> # Por ejemplo /var/backups/postgres
        
      # LOG directory location
      BACKUPS_LOGDIR=<dir_logs> # Por ejemplo /var/log
        
      # List of DBNAMES to EXLUCDE if DBNAMES are set to all (must be in " quotes)
      BACKUPS_DBEXCLUDE=<tables> # Por ejemplo db_test root postgres template0 template1
        
      # Include CREATE DATABASE in backup?
      BACKUPS_CREATE_DATABASE=<yes_or_no> # Por ejemplo yes
        
      # Separate backup directory and file for each DB? (yes or no)
      BACKUPS_SEPDIR=<yes_or_no> # Por ejemplo yes
        
      # Which day do you want weekly backups? (1 to 7 where 1 is Monday)
      BACKUPS_DOWEEKLY=<day_week> # Por ejemplo 7
        
      # Which day do you want monthly backups? (1 to 28)
      BACKUPS_DOMONTHLY=<day_month> # Por ejemplo 1
        
      # Choose Compression type. (gzip or bzip2)
      BACKUPS_COMP=<compression_type> # Por ejemplo bzip2
        
      # Command to run before backups (uncomment to use)
      #BACKUPS_PREBACKUP=<command> # Por ejemplo /etc/pgsql-backup-pre
        
      # Command run after backups (uncomment to use)
      #BACKUPS_POSTBACKUP=<command> # Por ejemplo sh /home/backups/scripts/ftp_pgsql
      ```
   
**Nota:** Es RECOMENDABLE cambiar por seguridad el valor de `DATABASE_URL`, `DATABASE_TEST_URL`, `POSTGRES_USER`, 
`POSTGRES_PASSWORD`, `BBDD_USER`, `` y `PGPASSWORD`.

4. Ejecutar:
   1. Levantar servicios:
      ```shell
      docker-compose up -d
      ```
   2. Parar servicios:
      ```shell
      docker-compose stop
      ```
   3. Eliminar servicios:
      ```shell
      docker-compose down
      ```
   4. Eliminar servicios (eliminando volúmenes):
      ```shell
      docker-compose down -v
      ```
   4. Eliminar servicios (eliminando volúmenes e imagenes):
      ```shell
      docker-compose down -v --rmi all
      ```   
   5. Visualizar servicios:
      ```shell
      docker-compose ps
      ```
**NOTA:** La API Rest usa por defecto el host *localhost* y el puerto *8080*.

### Producción
Plataforma de producción Heroku. En el entorno de producción se usa BBDD SQLite (develop.db).
Se despliega automáticamente en Heroku mediante el workflow *pro* (Github Actions) cuando haces push a la rama master.

1. Crear fichero **.env.pro** e introducir las variables de entorno necesarias para producción. Por ejemplo:
   1. **.env.pro**:
      ```shell      
      # Configuracion APP
      APP_NAME=Flask API Rest Template
      APP_ENV=production
      
      # Configuracion Flask
      API_ENTRYPOINT=app:app
      APP_SETTINGS_MODULE=config.ProductionConfig
      
      # Configuracion de servicio API
      API_HOST=<api_host>  # Por ejemplo 0.0.0.0
      
      # Configuracion de servicio BBDD
      DATABASE_URL=<url_database> # Por ejemplo sqlite:///production.db
      
      # Plataforma de deploy
      PLATFORM_DEPLOY=heroku
      ```
2. Crear *Secrets* en Github:
   1. **HEROKU_APP_NAME**: Nombre de app en Heroku.
   2. **HEROKU_API_KEY**: Token de acceso a Heroku.

**NOTA:** La API Rest usa el host *https://<name_app_heroku>.herokuapp.com*.

## Backups
En el entorno local existe un servicio llamado `cron` y es el encargado de ejecutar un script que realiza un backup
de la base de datos, en este caso de postgresql. El script se ejecuta diariamente mediante cron y realiza una copia 
diaria, una semanal y una mensual. 

- Las copias de seguridad `diarias` se rotan semanalmente.
- Las copias de seguridad `semanales` se ejecutan por defecto el sábado por la mañana cuando cron.daily scripts son ejecutados.
Puede ser cambiado con la configuración `DOWEEKLY`. Las copias de seguridad semanales se rotan en un ciclo de 5 semanas.
- Las copias de seguridad `mensuales` se ejecutan el día 1 de cada mes. Puede ser cambiado con la configuración `DOMONTHLY`. 
  Las copias de seguridad mensuales NO se rotan automáticamente.

**Nota:** Puede ser una buena idea copiar las copias de seguridad mensuales fuera de línea o en otro servidor.

## Comandos de Flask
### Flask-cli
   - Crear todas las tablas en la base de datos:
      ```sh
      flask create_db
      ```
   
   - Borra todas las tablas en la base de datos:
      ```sh
      flask drop_db
      ```
   
   - Crea usuario admin para la API Rest:
      ```sh
      flask create-user-admin
      ```
     
   - Reset de la base de datos:
      ```sh
      flask reset-db
      ```
     
   - Correr tests sin coverage:
      ```sh
      flask reset-db
      ```
     
   - Correr tests con coverage sin reporte en html:
      ```sh
      flask cov
      ```
     
   - Correr tests con coverage con reporte en html:
      ```sh
      flask cov-html
      ```
     
## Comandos de BBDD
### Flask-migrate
   - Crear un repositorio de migración:
      ```sh
      flask db init
      ```

   - Generar una version de migración:
      ```sh
      flask db migrate -m "Init"
      ```
     
   - Aplicar migración a la Base de Datos:
      ```sh
      flask db upgrade
      ```

## Endpoints
Distintos roles: user, admin

### Users
| Endpoint | HTTP Method | Result | Role |
|:---|:---:|---|---|
| `/users`  | `POST`  | Crear nuevo usuario  | user, admin |
| `/users`  | `GET`  | Obtener todos los usuarios  | admin |
| `/users/{user_id}`  | `GET`  | Obtener un usuario | user, admin |
| `/users/{user_id}`  | `PUT`  | Actualizar un usuario | user, admin |
| `/users/{user_id}`  | `DELETE`  | Eliminar un usuario | user, admin |
> La implementacion de los endpoints de user esta en  [app/api/v1/users/resources.py](./app/api/v1/users/resources.py).

### Auth
| Endpoint | HTTP Method | Result | Role |
|:---|:---:|---|---|
| `/auth/login`  | `POST`  | Login de un usuario  | user, admin |
| `/auth/logout`  | `DELETE`  | logout de un usuario | user, admin |
| `/auth/refresh`  | `GET`  | Refresh de access token  | user, admin |
> La implementacion de los endpoints de auth esta en  [app/api/v1/auth/resources.py](./app/api/v1/auth/resources.py).


## CI-CD
### CI (Continuous Integration)
El workflow de CI (ci.yml) utiliza Github Actions, como el Github Action [action-pipenv](https://github.com/igp7/action-pipenv) para utilizar comandos de pipenv.
El workflow ejecuta los tests unitarios, tests de integración y tests de API cuando se realiza un pull-request a master y develop o un push a develop.

### CD (Continuous Deployment)
El workflow de CD (pro.yml) utiliza Github Actions, como el Github Action [action-pipenv](https://github.com/igp7/action-pipenv) para utilizar comandos de pipenv.
El workflow ejecuta los tests unitarios, tests de integración, tests de API y desplegar en Heroku cuando se realiza un push a master.
- **NOTA:** Los **Actions Secrets** son necesarios para ejecutar corractamente el pipeline de CD. 
   - **HEROKU_API_KEY:** Token de acceso a Heroku.
   - **HEROKU_APP_NAME:** Nombre de app en Heroku.

## Ejemplo de expansion de este template
Necesitas añadir *items* que permita a los usuarios hacer CRUD en sus artículos:
1. Crear un modelo de base de datos `item` en [app/api/models.py](./app/api/models.py).
2. Crear un schema de `item` para load, dump y validacion en [app/api/v1/schemas.py](./app/api/v1/schemas.py)
3. Crea un directorio `items` en el directorio [app/api/v1](./app/api/v1/).
    1. Crear `items.py` en el directorio [app/api/v1/items](./app/api/v1/items/).
	2. Ver [users](./app/api/v1/users/resources.py) como ejemplo de cómo hacerlo.
    3. Crear bluepoint para `items`. 
	3. Crea una clase ItemsAPI y extender esta clase a partir de MethodView.
	4. Añadir los métodos CRUD necesarios para `items`.
4. Añadir blueprint de `items` [aqui](./app/__init__.py) 
5. Crea nuevos tests para el nuevo modulo:
   1. Crear archivo de tests funcionales `tests_items_api.py` (convención para este proyecto) en [tests/functional](./tests/functional) y escribe tus tests.
   2. Crear archivo de tests de integracion `tests_items_integration.py` (convención para este proyecto) en [tests/integration](./tests/integration) y escribe tus tests.
   3. Crear archivo de tests unitarias `tests_items_unit.py` (convención para este proyecto) en [tests/unit](./tests/unit) y escribe tus tests.
   4. Crear peticiones en postman (Opcional).
6. Añadir los endpoints en [swagger](services/docs/swagger.yml).
7. Añadir los endpoints en [README](#endpoints)

## Aviso de descargo de responsabilidad
En ningún caso me hago responsable por daños y perjuicios, incluidos, entre otros, daños y perjuicios indirectos o de carácter secundario, o daños y perjuicios por pérdidas o beneficios derivados de, o relacionados con, la utilización de este software.

Tú, como usuario, actúas por tu cuenta y riesgo si decides utilizar este software.

## Contribución
Siéntete libre de realizar cualquier sugerencia o mejora al proyecto.
