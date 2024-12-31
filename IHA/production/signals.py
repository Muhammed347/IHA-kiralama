# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Group
# from production.models import Employee

# @receiver(post_save, sender=Employee)
# def assign_group_to_user(sender, instance, created, **kwargs):
#     """
#     Automatically assigns a group to the User instance associated with the Employee,
#     based on the Employee's team field.
#     """
#     if instance.team:
#         try:
#             # Get or create the group corresponding to the Employee's team
#             group, _ = Group.objects.get_or_create(name=instance.team)
            
#             # Get the associated User instance
#             user = instance.user

#             # Assign the group to the user if not already assigned
#             if not user.groups.filter(name=group.name).exists():
#                 user.groups.add(group)
#         except Group.DoesNotExist:
#             # Log or handle the case where the group doesn't exist
#             print(f"Group '{instance.team}' does not exist for user '{instance.user.username}'.")
