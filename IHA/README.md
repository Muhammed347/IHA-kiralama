# Requirements to run application:
- Make sure Docker is installed on your computer. 
- Start Docker Desktop or ensure the Docker daemon is running in the background.

# step 1: Clone the Project Repository
```bash
git clone https://github.com/Muhammed347/IHA-kiralama.git
cd IHA
```

# step 2: Build and Start the Docker Containers
```bash
docker-compose up --build
```

# step 3: Step 4: Run Database Migrations
```bash
docker exec -it django_app python manage.py migrate
```

# Step 4: Create a Superuser
```bash
docker exec -it django_app python manage.py createsuperuser
```
- example username: admin, email: can be left blank, password: admin 
- Confirm the confirmation message by typing y then enter



