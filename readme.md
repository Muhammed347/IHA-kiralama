# Requirements to run application:
- Make sure Docker is installed on your computer. 
- Start Docker Desktop or ensure the Docker daemon is running in the background.

# step 1: Clone the Project Repository an go to project directory
```bash
git clone https://github.com/Muhammed347/IHA-kiralama.git
```
```bash
code .
```
```bash
cd .\IHA-kiralama\IHA\ 
```

# step 2: Build and Start the Docker Containers(You will get an error in this step because we must migrate the database tables in the next step.) 
```bash
docker-compose up --build
```

# step 3: open a new terminal in the same directory(\IHA-kiralama\IHA\) while other terminal is running 


# step 4:Run Database Migrations on new terminal
```bash
docker exec -it django_app python manage.py migrate
```

# Step 5: Create a Superuser
```bash
docker exec -it django_app python manage.py createsuperuser
```
- example username: admin, email: can be left blank, password: admin 
- Confirm the confirmation message by typing y then enter

# Step 7: restart the Application
```bash
docker-compose down
```
```bash
docker-compose up
```

# Step 7: Access the Application
-application should be accessible in the browser at the specified port (http://localhost:8000).
-To log in to the admin panel, navigate to http://localhost:8000/admin and use the credentials you set up in the previous step.



# Step 7: Run Tests(optional)
```bash
docker exec -it django_app python manage.py test
```


![Alt text](images/giris_ekrani.png)
![Alt text](images/admin_panel.png)
![Alt text](images/login.png)
![Alt text](images/montaj.png)
![Alt text](images/parca_ekleme.png)
![Alt text](images/parca_listele.png)