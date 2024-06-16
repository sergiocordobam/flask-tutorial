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

- Finally, check the changes by accessing to your EC2 instance public IP
