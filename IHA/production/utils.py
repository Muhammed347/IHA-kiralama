
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from production.models import WingPart, BodyPart, TailPart, AvionicsPart 

# def create_groups():
#     """Create groups corresponding to teams."""
#     teams = ['kanat', 'govde', 'kuyruk', 'aviyonik', 'montaj']
#     for team in teams:
#         Group.objects.get_or_create(name=team)
#     print("Groups created successfully.")

# def assign_permissions():
#     """Assign permissions to groups based on their roles."""
#     # Define permissions mapping
#     permissions_map = {
#         'kanat': WingPart,
#         'govde': BodyPart,
#         'kuyruk': TailPart,
#         'aviyonik': AvionicsPart,
#     }
    
#     for group_name, model in permissions_map.items():
#         # Get or create group
#         group, _ = Group.objects.get_or_create(name=group_name)
        
#         # Get model's permissions
#         content_type = ContentType.objects.get_for_model(model)
#         permissions = Permission.objects.filter(content_type=content_type)
        
#         # Assign permissions to the group
#         group.permissions.set(permissions)
#         print(f"Assigned permissions for group: {group_name}")
    
#     print("Permissions assigned successfully.")