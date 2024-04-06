from enum import Enum 

# DEFAULT_SUGAR = 1
# DEFAULT_BUTTER = 1
# DEFAULT_EGGS = 1
# DEFAULT_FLOUR = 1
# DEFAULT_BAKING_SODA = 1
# DEFAULT_MILK = 1

class RecipeNames(Enum):
    none = 0
    cookies = 1
    cupcakes = 2
    cake = 3

    def static_enum(recipeNameValue):
        if recipeNameValue in ('none', 'None'):
            return RecipeNames.none
        elif recipeNameValue in ('cookies', 'Cookies'):
            return RecipeNames.cookies
        elif recipeNameValue in ('cupcakes', 'Cupcakes'):
            return RecipeNames.cupcakes
        elif recipeNameValue in ('cake', 'Cake'):
            return RecipeNames.cake

class Recipe:

    def __init__(self, name : RecipeNames, batch_yield : int, mix_time : int, bake_time : int, decorate_time : int):
        self.name = name
        self.batch_yield = batch_yield
        self.times = {
            'mixer' : mix_time,
            'oven' : bake_time,
            'decorating_station' : decorate_time
        }



