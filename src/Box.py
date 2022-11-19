class Box:
    def __init__(self, name, possible_ingredients, ingredients):
        self._name = name
        possible_ingredients.sort()
        self._possible_ingredients = possible_ingredients
        ingredients.sort()
        self._ingredients = self.set_ingredients(ingredients)

    def set_ingredients(self, ingredients):
        current = 0
        result = {}
        for ingredient in self._possible_ingredients:
            result.update({ingredient: []})
            while(current != len(ingredients) and ingredient == ingredients[current]):
                result[ingredient].append(ingredients[current])
                current += 1
        return result
	
    def check_for_ingredient(self, ingredient):
        return ingredient in self._ingredients[ingredient]

    def can_put_ingredient(self, ingredient):
        return ingredient in self._ingredients.keys()

    def retrieve_ingredient(self, ingredient):
        temp = self._ingredients[ingredient]
        res = temp.pop()
        self._ingredients.update({ingredient: temp})
        return res

    def add_ingredient(self, ingredient):
        temp = self._ingredients[ingredient]
        temp.append(ingredient)
        self._ingredients.update({ingredient : temp})

    def __str__(self):
        return self._name + " box"

    def is_empty(self):
        return self._ingredients == []

# shop contains boxes
# boxes contain ingredients
# boxes = what it cann carry
# what it does carry
