# Deploy a Flask app on AWS step by step, using Docker and Docker Compose
- Create a new EC2 instance using Ubuntu
- Allow HTTP and HTTPS traffic

## 1. Install and update the required packages
- Connect by SSH to your EC2 instance and run the following command:
- Update your package list:

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

- Install Docker dependencies:

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```

- Install Docker Compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- Close your EC2 SSH instance shell and connect again
- Verify Docker and Docker Compose installations:

 ```bash
docker --version
docker-compose --version
``` 

## 2. Clone your GitHub project

- In my case I'm using a project called **"Flask-tutorial"**
- Then, navigate to the main folder of the project:

```bash
git clone https://github.com/sergiocordobam/flask-tutorial.git
cd flask-tutorial
```
- Start Docker service

```bash
sudo systemctl start docker
```

## 3. Build and run the Docker container using Docker Compose

- Build and start the app using Docker Compose:
 
```bash
sudo docker-compose up --build -d
```

## 4. Set up Nginx

- Install Nginx:

```bash
sudo apt-get install nginx -y
```

- Start and enable the Nginx service:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

- Edit the Nginx default configuration file:

```bash
sudo nano /etc/nginx/sites-available/default
```

- Delete all the existing content in the file and replace it with the following chunk of code:

```bash
upstream flaskhelloworld {
    server 127.0.0.1:8000;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name <your_EC2_public_IP_address>;

    location / {
        proxy_pass http://flaskhelloworld;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Adjust error handling as needed
        try_files $uri $uri/ @proxy_to_flask;
    }

    location @proxy_to_flask {
        proxy_pass http://flaskhelloworld;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- Restart Nginx to apply the changes:

```bash
sudo systemctl restart nginx
```

## 5. Access to your EC2 instance:

- You should be able to see your Flask app when accessing to the public IP address.

# Update your app

- Push changes to your GitHub repository
- Connect to your EC2 instance (SSH)
- Navigate to your project folder:

```bash
cd flask-tutorial
```

- Pull changes from GitHub:

```bash
git pull origin main
```

- Rebuild and restart your Docker container using Docker Compose:

```bash
sudo docker-compose up --build -d
```

- Finally, check the changes by accessing to your EC2 instance public IP.

# Database

- Install SQLAlchemy packages:

```bash
pip install sqlalchemy flask-sqlalchemy pymysql
```

- Update your packages requirements:

```bash
pip freeze > requirements.txt 
``` 
  
- Add the following content to your `requirements.txt` file:

```bash
cryptography==3.4.8
```

- Update your `docker-compose.yml` file:

```bash
version: '3'
services:
  mysql:
    image: mysql:latest
    environment:
      MYSQL_DATABASE: <db_name>
      MYSQL_USER: <user> 
      MYSQL_PASSWORD: <password>
      MYSQL_ROOT_PASSWORD: <rootpassword>
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"

  flask-app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      FLASK_APP: app.py
      FLASK_ENV: development
    depends_on:
      - mysql

volumes:
  mysql-data:
```

- Add the following lines of code to your `app.py` file:

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskpassword@mysql/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

- Create the model and then add this chunk of code below the model:

```bash
with app.app_context():
    db.create_all()
```

- In your EC2 instance run this command:

```bash
cd <your_project_folder>
git pull origin main
```

- Build the Docker image:

```bash
sudo docker-compose up --build -d
```

# MySQL

- If you want to connect to the database, install the mysql-client:

```bash
sudo apt update
sudo apt install mysql-client
```

- Verify installation:

```bash
mysql --version
```

- Connect to the database:

```bash
mysql -u flaskuser -p -h 127.0.0.1
```

- Enter your password
- Check your EC2 instance

# Bootstrap

- Add Bootstrap to your Flask app:

```bash
<!doctype html>
<html>
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>{% block title %}{% endblock title%}</title>
</head>
<body>
    {% block content %}
    {% endblock content%}
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
```

## Template Inheritance

- If your app has similar elements, you can use template blocks to avoid repeating code:

```bash
{% extends "<file_name>.html" %}
{% block title %} <title> {% endblock title %}
{% block content %}
{% endblock content %}
```
