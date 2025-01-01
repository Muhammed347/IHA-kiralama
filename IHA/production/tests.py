from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import WingPart, Employee, AircraftName, Team, BodyPart, AirCraft, TailPart, AvionicsPart
from .forms import WingPartForm
from django.contrib.messages import get_messages

# class AddWingPartViewTest(TestCase):

#     def setUp(self):
#         # Create a user with the 'kanat' team
#         self.user = User.objects.create_user(username='wing_user', password='password123')
#         self.employee = Employee.objects.create(user=self.user, team=Team.kanat.value)
        
#         self.client.login(username='wing_user', password='password123')
        
#         self.valid_data = {
#             'aircraftname': AircraftName.TB2.value,
#             'status': 'unused',
#         }
#         self.invalid_data = {
#             'aircraftname': '',  # Missing required field
#             'status': 'unused',
#         }

#     def test_authorized_user_adds_part(self):
#         response = self.client.post(reverse('add_wing_part'), data=self.valid_data)
#         self.assertRedirects(response, reverse('listParts'))
#         self.assertTrue(WingPart.objects.filter(aircraftname=AircraftName.TB2.value).exists())
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Kanat Parcasi basari ile eklendi.")

#     def test_unauthorized_user_access(self):
#         # Create a user with a different team
#         other_user = User.objects.create_user(username='body_user', password='password123')
#         Employee.objects.create(user=other_user, team=Team.govde.value)  # Team not authorized
        
#         self.client.login(username='body_user', password='password123')
        
#         response = self.client.post(reverse('add_wing_part'), data=self.valid_data)
#         self.assertRedirects(response, reverse('index'))
#         self.assertFalse(WingPart.objects.filter(aircraftname=AircraftName.TB2.value).exists())
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Bu sayfaya erismek icin yetkili degilsiniz.")

#     def test_invalid_form_submission(self):
#         response = self.client.post(reverse('add_wing_part'), data=self.invalid_data)
#         self.assertRedirects(response, reverse('produceParts'))
#         self.assertFalse(WingPart.objects.exists())
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Kanat Parcasi eklenirken bir soun olustu.")

#     def test_get_request(self):
#         response = self.client.get(reverse('add_wing_part'))
#         self.assertRedirects(response, reverse('index'))
        
# class DeletePartViewTest(TestCase):

#     def setUp(self):
#         # Create users and assign them to teams
#         self.kanat_user = User.objects.create_user(username='kanat_user', password='password123')
#         Employee.objects.create(user=self.kanat_user, team=Team.kanat.value)

#         self.govde_user = User.objects.create_user(username='govde_user', password='password123')
#         Employee.objects.create(user=self.govde_user, team=Team.govde.value)

#         self.no_team_user = User.objects.create_user(username='no_team_user', password='password123')

#         # Create parts
#         self.wing_part = WingPart.objects.create(aircraftname='TB2', status='unused')
#         self.body_part = BodyPart.objects.create(aircraftname='AKINCI', status='used')

#     def test_authorized_user_deletes_part(self):
#         self.client.login(username='kanat_user', password='password123')
#         response = self.client.post(reverse('delete_part', args=[self.wing_part.id]))
#         self.assertRedirects(response, reverse('listParts'))
#         self.assertFalse(WingPart.objects.filter(id=self.wing_part.id).exists())

#     def test_unauthorized_user_attempts_to_delete_part(self):
#         self.client.login(username='govde_user', password='password123')
#         response = self.client.post(reverse('delete_part', args=[self.wing_part.id]))
#         #self.assertEqual(response.status_code, 403)
#         self.assertTrue(WingPart.objects.filter(id=self.wing_part.id).exists())

#     def test_user_without_team_attempts_to_delete_part(self):
#         self.client.login(username='no_team_user', password='password123')
#         response = self.client.post(reverse('delete_part', args=[self.wing_part.id]))
#         self.assertRedirects(response, reverse('index'))
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Hicbir takima ait değilsiniz.")
#         self.assertTrue(WingPart.objects.filter(id=self.wing_part.id).exists())

#     def test_non_existent_part_deletion(self):
#         self.client.login(username='kanat_user', password='password123')
#         response = self.client.post(reverse('delete_part', args=[999]))  # Non-existent ID
#         self.assertEqual(response.status_code, 404)

#     def test_anonymous_user_attempts_to_delete_part(self):
#         response = self.client.post(reverse('delete_part', args=[self.wing_part.id]))
#         #self.assertRedirects(response, f"{reverse('login')}?next={reverse('delete_part', args=[self.wing_part.id])}")
#         self.assertTrue(WingPart.objects.filter(id=self.wing_part.id).exists())





class AssembleAndViewDronesTest(TestCase):
    def setUp(self):
        # Create users
        self.montaj_user = User.objects.create_user(username="montaj_user", password="password123")
        Employee.objects.create(user=self.montaj_user, team=Team.montaj.value)

        self.other_user = User.objects.create_user(username="other_user", password="password123")
        Employee.objects.create(user=self.other_user, team=Team.kanat.value)

        # Create parts for aircraft
        self.wing = WingPart.objects.create(aircraftname=AircraftName.TB2.value)
        self.body = BodyPart.objects.create(aircraftname=AircraftName.TB2.value)
        self.tail = TailPart.objects.create(aircraftname=AircraftName.TB2.value)
        self.avionics = AvionicsPart.objects.create(aircraftname=AircraftName.TB2.value)

        # Create an aircraft
        self.aircraft = AirCraft.objects.create(
            aircraftname=AircraftName.TB2.value,
            wing=self.wing,
            body=self.body,
            tail=self.tail,
            avionics=self.avionics,
        )

        # these will be used to submit form
        self.tb3wing = WingPart.objects.create(aircraftname=AircraftName.TB3.value)
        self.tb3body = BodyPart.objects.create(aircraftname=AircraftName.TB3.value)
        self.tb3tail = TailPart.objects.create(aircraftname=AircraftName.TB3.value)
        self.tb3avionics = AvionicsPart.objects.create(aircraftname=AircraftName.TB3.value)

        #other model part. will be used to test model compatibility
        self.akinciwing = WingPart.objects.create(aircraftname=AircraftName.AKINCI.value) 

        

    def test_authorized_user_accesses_view(self):
        self.client.login(username="montaj_user", password="password123")
        response = self.client.get(reverse("assemble_and_view_drones"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertContains(response, AircraftName.TB2.value)

    def test_authorized_user_submits_valid_form(self):
        self.client.login(username="montaj_user", password="password123")
        valid_data = {
            "aircraftname": AircraftName.TB3.value,
            "wing": self.tb3wing.pk,
            "body": self.tb3body.pk,
            "tail": self.tb3tail.pk,
            "avionics": self.tb3avionics.pk,
        }
        response = self.client.post(reverse("assemble_and_view_drones"), data=valid_data)
        self.assertRedirects(response, reverse("assemble_and_view_drones"))
        self.assertTrue(AirCraft.objects.filter(aircraftname=AircraftName.TB3.value).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"'{AircraftName.TB3.value}' adli ucak basari ile olusturuldu.")

    def test_authorized_user_submits_invalid_form(self):
        self.client.login(username="montaj_user", password="password123")
        invalid_data = {
            "aircraftname": "",  # Missing required field
            "wing": self.tb3wing.pk,
            "body": self.tb3body.pk,
            "tail": self.tb3tail.pk,
            "avionics": self.tb3avionics.pk,
        }
        response = self.client.post(reverse("assemble_and_view_drones"), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AirCraft.objects.filter(aircraftname="").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "ucak uretirken hata meydana geldi.")

    def test_cannot_use_part_from_different_aircraft_model(self):
        self.client.login(username="montaj_user", password="password123")
        invalid_data = {
            "aircraftname": AircraftName.TB3.value,
            "wing": self.akinciwing.pk,  # Part from akinci, diffirent model part defined in setup
            "body": self.tb3body.pk,
            "tail": self.tb3tail.pk,
            "avionics": self.tb3avionics.pk,
        }
        response = self.client.post(reverse("assemble_and_view_drones"), data=invalid_data)

        self.assertFalse(AirCraft.objects.filter(aircraftname=AircraftName.TB3.value).exists())

        #This is different from the others because it is checked when creating the form
        self.assertRaisesMessage(ValueError, "Kullanilan butun parcalar ucak modeliyle ayni modele sahip olmali.")
    
    def test_cannot_use_part_already_used(self):
        self.client.login(username="montaj_user", password="password123")
        invalid_data = {
            "aircraftname": AircraftName.TB3.value,
            "wing": self.wing.pk,  # Part from TB2, already used in setup
            "body": self.tb3body.pk,
            "tail": self.tb3tail.pk,
            "avionics": self.tb3avionics.pk,
        }
        response = self.client.post(reverse("assemble_and_view_drones"), data=invalid_data)

        
        self.assertFalse(AirCraft.objects.filter(aircraftname=AircraftName.TB3.value).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("ucak uretirken hata meydana geldi.", str(messages[0]))


    def test_unauthorized_user_accesses_view(self):
        self.client.login(username="other_user", password="password123")
        response = self.client.get(reverse("assemble_and_view_drones"))
        self.assertRedirects(response, reverse("index"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Bu sayfaya erismek icin yetkili degilsiniz.")

    def test_anonymous_user_accesses_view(self):
        response = self.client.get(reverse("assemble_and_view_drones"))
        self.assertRedirects(response, reverse("login"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Bu sayfaya erismek icin giris yapmaniz gerekiyor.")
