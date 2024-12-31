from django.db import models
from django.contrib.auth.models import User

from enum import Enum

# Create your models here.
class Team(Enum):
    kanat = "kanat"
    govde = "govde"
    kuyruk = "kuyruk"
    aviyonik = "aviyonik"
    montaj = "montaj"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]
    

class AircraftName(Enum):
    TB2 = "TB2"
    TB3 = "TB3"
    AKINCI = "AKINCI"
    KIZILELMA = "KIZILELMA"
 
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]
    

#Status enum will be used to track if wing, tail, body etc. are available or not
class Status(Enum):
    used = "used"
    unused = "unused"

 
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

#each employee keeps user and the information of the team to which he is assigned 
#When an employee is created using the user, automatically assigned to a group using the signal function   
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    team = models.CharField(max_length=50, choices=Team.choices(), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.team})"
    
    class Meta:
        verbose_name_plural = "Team"


# wing, body, tail models will derived from this BasePart class
class BasePart(models.Model):
    aircraftname = models.CharField(max_length=50, choices=AircraftName.choices(), blank=False, null=False)
    status = models.CharField(max_length=50, choices=Status.choices(), default=Status.unused.value)

    class Meta:
        abstract = True
    

class WingPart(BasePart):
    team = Team.kanat.value

    def __str__(self):
        return f"{self.aircraftname}_({self.pk}) ({self.team})"
class BodyPart(BasePart):
    team = Team.govde.value

    def __str__(self):
        return f"{self.aircraftname}_({self.pk}) ({self.team})"

class TailPart(BasePart):
    team = Team.kuyruk.value

    def __str__(self):
        return f"{self.aircraftname}_({self.pk}) ({self.team})"
    

class AvionicsPart(BasePart):
    team = Team.aviyonik.value

    def __str__(self):
        return f"{self.aircraftname}_({self.pk}) ({self.team})"
    

class AirCraft(models.Model):
    aircraftname = models.CharField(max_length=50, choices=AircraftName.choices(), blank=False, null=False)
    wing = models.OneToOneField(WingPart, on_delete=models.CASCADE, blank=False, null=False, related_name="assigned_aircraft")
    body = models.OneToOneField(BodyPart, on_delete=models.CASCADE, blank=False, null=False, related_name="assigned_aircraft")
    tail = models.OneToOneField(TailPart, on_delete=models.CASCADE, blank=False, null=False, related_name="assigned_aircraft")
    avionics = models.OneToOneField(AvionicsPart, on_delete=models.CASCADE, blank=False, null=False, related_name="assigned_aircraft")

    def save(self, *args, **kwargs):
        if self.wing.status != Status.unused.value or \
        self.body.status != Status.unused.value or \
        self.tail.status != Status.unused.value or \
        self.avionics.status != Status.unused.value:
            raise ValueError("Tum ucak Parcalari kullanilmamis olmali '.")
        

        # Validate that all parts have the same aircraftname as the aircraft
        if (
            self.wing.aircraftname != self.aircraftname or
            self.body.aircraftname != self.aircraftname or
            self.tail.aircraftname != self.aircraftname or
            self.avionics.aircraftname != self.aircraftname
        ):
            raise ValueError("Kullanilan butun parcalar ucak modeliyle ayni modele sahip olmali.")

        super().save(*args, **kwargs)

        # Update the status of the used parts to "used"
        self.wing.status = Status.used.value
        self.wing.save(update_fields=["status"])
        
        self.body.status = Status.used.value
        self.body.save(update_fields=["status"])
        
        self.tail.status = Status.used.value
        self.tail.save(update_fields=["status"])
        
        self.avionics.status = Status.used.value
        self.avionics.save(update_fields=["status"])


    def __str__(self):
        return f"{self.aircraftname}_({self.pk})"



