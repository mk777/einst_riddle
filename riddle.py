#Einstein riddle solver
#
# There is a row of five different color houses. Each is occupied 
# by a man of different nationality. Each man has a different pet,
# prefers a different drink, and smokes a different brand of 
# cigarettes.
# 1. The Brit lives in a Red House.
# 2. The Swede keeps dogs as pets.
# 3. The Dane drinks tea.
# 4. The Green house is next to the White one, on the left.
# 5. The owner of the Green house drinks coffee.
# 6. The person who smokes Pall Mall rears birds.
# 7. The owner of the Yellow house smokes Dunhill.
# 8. The man living in the centre house drinks milk.
# 9. The Norwegian lives in the first house.
# 10. The man who smokes Blends lives next to the one who keeps cats.
# 11. The man who keeps horses lives next to the man who smokes Dunhill.
# 12. The man who smokes Blue Master drinks beer.
# 13. The German smokes Prince.
# 14. The Norwegian lives next to the Blue house.
# 15. The man who smokes Blends has a neighbour who drinks water.
#
# Who has fish at home?


class house_class:
    def __init__(self, color, nation, drink, smoke, pets):
        self.color = color
        self.nation = nation
        self.drink = drink
        self.smoke = smoke
        self.pets = pets

    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s" % \
        (self.color, self.nation, self.drink, self.smoke, self.pets)
    
def pred_index(data, predicate):
    """finds the index of the first element in the collection that satisfies 
    the predicate or -1 if none does"""
    
    for i,datum in enumerate(data):
        if predicate(datum):
            return i

    return -1

def pred(field,value):
    """returns a predicate which evaluates to true if the attribute named filed
    equals the value"""

    return lambda x: x.__dict__[field] == value
def all_true(bool_list):

    return bool_list.count(False) > 0

def pred_list(pairs):
    """ returns a predicate which evaluates to true if the field pair[0]
    of the argument has value pair[1] for each pair in pairs"""

    return lambda x: all_true([pred(*pair)(x) for pair in pairs])

def pred_neighb(pred1, pred2):
    """returns a lambda that returns true if the elements satisfying 
    pred1 and pred2 are next to each other in the agrument collection"""

    return lambda data: abs(pred_index(data,pred1)-pred_index(data,pred2)) == 1

def permutations(data):
    """this is written in Python 2.5 :(
    I know this is inefficient, but I only need it for 5-element lists.
    shamelessly stolen from the Recipe 252178 by Michael Davies"""

    if not data:
        yield ()
    else:
        if len(data) == 1:
            yield (data[0],)
        else:
            x = data[0]
            for perm in permutations(data[1:]):
                for i in range(0,len(data)):
                    yield perm[:i] + (x,) + perm[i:]

def cross(iterators):
    """ generator for a cross-product of iterators 
    (this is still Python 2.5)"""

    if not iterators :
        yield ()
    else:
        if len(iterators) == 1:
            for elem in iterators[0]:
                yield (elem,)
        else:
            for elem in iterators[0]:
                for tuple in cross(iterators[1:]):
                    yield (elem,) + tuple

colors = ["Red", "Yellow", "White", "Green","Blue"]

nationalities = ["Brit", "Swede", "Dane", "German", "Norwegian"]

drinks = ["tea", "coffee", "beer", "water", "milk"]

smokes = ["Pall Mall", "Dunhill", "Blends", "Blue Masters", "Prince"]

pets = ["dogs", "birds", "cats", "horses", "fish"]

single_predicates = map(pred_list,
    [(("color","Red"),("nation","Brit")),
	(("nation","Swede"),("pets","dogs")),
	(("nation","Dane"),("drink","tea")),
	(("color","Green"),("drink","coffee")),
    (("smoke","Pall Mall"),("pets","birds")),
	(("color","Yellow"),("smoke","Dunhill")),
	(("smoke","Blue Master"),("drink","beer")),
	(("nation","German"),("smoke","Prince"))])

list_predicates = [
    lambda houses: pred_index(houses,pred("color","Green")) + 1 ==  
    pred_index(houses,pred("color","White")),
    lambda houses: houses[2].drink == "milk",
    lambda houses: houses[0].nation == "Norwegian"] +\
    map(lambda pair: pred_neighb(*pair),
    [(pred("smoke","Blends"),pred("pets","cats")),
	(pred("smoke","Dunhill"),pred("pets","horses")),
	(pred("nation","Norwegian"),pred("color","Blue")),
	(pred("smoke","Blends"),pred("drink","water"))])


