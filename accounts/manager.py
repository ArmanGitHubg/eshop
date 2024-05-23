# class CustomerManager(models.Manager):
#     """
#     Customizing manager of user for change auth filed to phone number for default username
#     """
#     def create_superuser(self, username=None, email=None, password=None, **extra_fileds):
#         username = extra_fileds["phone"]
#         return super().create_superuser(username, email, password, **extra_fileds)
    
#     # def get_by_natural_key(self, username):
#     #     return self.get(username=username)
    
#     # override the get_queryset method to hide logical deleted in funtions
#     def get_querset(self):
#         return super().get_queryset().exclude(deleted=True)
    
#     # override delete method to change delete filed to logical delete
#     def delete(self):
#         for obj in self:
#             obj.delete()
        
#     # create new method to set new all() function for show deleted items
#     def archive(self):
#         return super().get_queryset()
    
