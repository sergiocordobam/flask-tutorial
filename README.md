# Deploy a Flask app on AWS step by step
- Create a new EC2 instance using Ubuntu
- Allow HTTP and HTTPS traffic

## 1. Install and update the required packages
- Connect by SSH to your EC2 instance and run the following command:

```bash
sudo apt-get update && sudo apt-get upgrade
```

- Install the Python Virtual Environment package:

```bash
sudo apt-get install python3-venv
```

## 2. Clone your GitHub project and set up the virtual environment

- In my case I'm using a project called **"Flask-tutorial"**
- Then, navigate to the main folder of the project:

```bash
git clone https://github.com/sergiocordobam/flask-tutorial.git
cd flask-tutorial
```
- Create a virtual environment:

```bash
python3 -m venv venv
```

- Activate the virtual environment:

```bash
source venv/bin/activate
```

## 3. Install flask

```bash
pip install Flask
```

- Verify that the Flask app is running:

```bash
python app.py
```

## 4. Run Gunicorn WSGI Server

- Install Gunicorn:

```bash
pip install gunicorn
```

- Serve the Flask app using Gunicorn:

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

- Exit from Gunicorn using `Ctrl + C`

## 5. Manage systemd

- Create a systemd file:

```bash
sudo nano /etc/systemd/system/<service_name>.service
```

- In my case, the command is:

```bash
sudo nano /etc/systemd/system/helloworld.service
```

- Paste the following content into the systemd file:

```bash
[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/flask-tutorial
ExecStart=/home/ubuntu/flask-tutorial/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

- Now you can enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start helloworld
sudo systemctl enable helloworld
```

- Check if your app is running:

```bash
curl localhost:8000
```

## 6. Set up Nginx

- Install Nginx:

```bash
sudo apt-get install nginx
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

## 7. Access to your EC2 instance:

- You should be able to see your Flask app when accessing to the public IP address.
