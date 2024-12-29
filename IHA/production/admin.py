from django.contrib import admin
from .models import Employee, WingPart, BodyPart, TailPart, AvionicsPart, AirCraft


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "team")  # Display these fields in the admin list view
    search_fields = ("user__username", "team")  # Add search functionality
    list_filter = ("team",)  # Add filtering by team


@admin.register(WingPart)
class WingPartAdmin(admin.ModelAdmin):
    list_display = ("aircraftname", "status")  # Display aircraft and status
    list_filter = ("aircraftname", "status")  # Add filters for aircraft and status


@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    list_display = ("aircraftname", "status")
    list_filter = ("aircraftname", "status")


@admin.register(TailPart)
class TailPartAdmin(admin.ModelAdmin):
    list_display = ("aircraftname", "status")
    list_filter = ("aircraftname", "status")


@admin.register(AvionicsPart)
class AvionicsPartAdmin(admin.ModelAdmin):
    list_display = ("aircraftname", "status")
    list_filter = ("aircraftname", "status")


@admin.register(AirCraft)
class AirCraftAdmin(admin.ModelAdmin):
    list_display = ("aircraftname", "wing", "body", "tail", "avionics")  # Display the parts and aircraft name
    search_fields = ("aircraftname",)  # Add search functionality
    list_filter = ("aircraftname",)  # Add filtering by aircraft name
