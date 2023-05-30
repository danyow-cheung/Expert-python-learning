
class User(object):
    def __init__(self,roles ) -> None:
        self.roles = roles 
    
class Unauthorized(Exception):
    pass 

def protect(role):
    def proetect(function):
        def _protect(args,*kw):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("I won't tell you")
            return function(args,*kw)
        return _protect 
    return proetect 


                                   
'''Example Usage'''
tarek = User(("admin","user"))
bill = User(("user"))

class MySecrets(object):
    @protect('admin')
    def waffle_recipe(self):
        print('Use tons of butter')

these_are = MySecrets()
user = tarek 
these_are.waffle_recipe()
user = bill 
these_are.waffle_recipe()
