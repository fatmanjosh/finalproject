class Robot:
    def __init__(self, goal_ingredients, replacements):
        self._goal_ingredients = goal_ingredients
        self._inventory = []
        self._out_of_stock = ["milk", "almond milk"]
        self._replacements = self.update_food_dictionary(replacements)
        # milk : ([oat milk, almond milk])


        # oat milk : almond milk

    def update_food_dictionary(self, replacements):
        result = {}
        for i in range(len(replacements)):
            if i != len(replacements) - 1:
                result.update({replacements[i]: replacements[i + 1]})

        return result


    def check_ingredients(self):

        ## check if the inghredient is out
        # for each ingred in oos
        # is that in the goal state
        # if so - try replaceing that by the next replacement for that ingredient until the replacement is eiter
        # out stock or there are no more replacements

        for ingredient in self._out_of_stock:
            if not self.update_goal(ingredient):
                return False

        return True

    def update_goal(self, ingredient):
        if ingredient in self._goal_ingredients:
            if (not ingredient in self._replacements.keys()):
                return False
            current_ingredient = self._replacements[ingredient]
            # current = replacement
            while (current_ingredient in self._out_of_stock):
                if not current_ingredient in self._replacements.keys():
                    return False
                current_ingredient = self._replacements[current_ingredient]
            for i in range(len(self._goal_ingredients)):
                if current_ingredient == self._goal_ingredients[i]:
                    self._goal_ingredients[i] = current_ingredient
                    break

        return True

    def check_replacement(self, replacement):
        if(replacement[0] + 1 == len(replacement[1])):
            return True
        else:
            return False

    def pick_up_ingredient(self, ingredient, box):
        if not box.can_put_ingredient(ingredient):
            print("Ingredient cannot be found in this box. \n")
            return False
        if not box.check_for_ingredient(ingredient):
            self._out_of_stock.append(ingredient)
            if(not self.update_goal_with_replacement(ingredient)):
                return False
        else:
            self._inventory.append(box.retrieve_ingredient(ingredient))

    def report_impossible_task(self):
        print("Cannot be done")

    def give_ingredients(self, customer):
        customer.receive_ingredients(self._inventory)
        self._inventory = []

