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


# Step 8: You can use the following command to automatically generate 5 users for each team.(optional)
```bash
docker exec -it django_app  python manage.py add_users
```
-automatically generated user account information:
kanat_user password123 \
govde_user password123  \
kuyruk_user password123 \ 
aviyonik_user password123 \
montaj_user password123 \

\
# How application works
-Registered users can do their jobs after being assigned to teams from the admin page. \
-Teams that produce parts (wing, body, tail, avionics) can produce their own parts from the parts production page and list their own produced parts and delete their own parts. \
-The assembly team can combine parts and produce aircraft and display the produced aircraft in a table. \


# App screenshots
![mainPage](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/giris_ekrani.PNG?raw=true) \ \
![admin](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/admin_panel.PNG?raw=true) \ \
![login](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/login.PNG?raw=true) \ \
![montaj](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/montaj.PNG?raw=true) \ \
![add](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/parca_ekleme.PNG?raw=true) \ \
![list](https://github.com/Muhammed347/IHA-kiralama/blob/main/images/parca_listele.PNG?raw=true) \ \