import pytest

from food_detection import FoodDetection

'''
Here we will import the code classes and functions to perform tests. 

example: 

The function:

class FoodDetection:
    def __init__(self, needle_img, haystack_img):
        self.needle_img = needle_img
        self.haystack_img = haystack_img

    def dist_from(self, x, y):
        centrex = 475
        centrey = 462
        return (((x - centrex)*(x-centrex)) + ((y-centrey)*(y-centrey)))

'''

'''
A test:

def dist_from_not_negative():
    instance_of_class = FoodDetection(needle_img, haystack_img)
    distance_from = instance_of_class.dist_from( x, y )

    assert distance_from[0]>=0, "Only positive numbers accepted."
    print('You entered: ', num)


'''

## passable tests for usage of pytest
def test_some_sensible_test():
    assert 3 * 3 == 9

def test_some_sensible_test_2():
    assert 3 * 3 != 4