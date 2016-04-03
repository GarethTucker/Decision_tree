from Build_tree import Tree
from Classify import Classify

class Main(object):
    def __init__(self, test_file, training_file):
        with open (test_file) as f:
            lines = f.readlines()
            self.test_list = [line.split() for line in lines]
            self.test_list = [x for x in self.test_list if x != []]
            self.test_list[1] = ['RESULT'] + self.test_list[1]

        with open (training_file) as f:
            lines = f.readlines()
            self.training_list = [line.split() for line in lines]
            self.training_list = [x for x in self.training_list if x != []]
            self.training_list[1] = ['RESULT'] + self.training_list[1]


if __name__=="__main__":
    data = Main('data/hepatitis-test.dat', 'data/hepatitis-training.dat')
    # print('\n'.join([' '.join([format(item) for item in row])
    #                  for row in data.training_list]))
    t = Tree(data)

    tree = t.tree
    tree.report('')
    print('Classifying test data...')
    c = Classify(data, tree)
    print('Num correct: {0}, Num tested: {1}'.format(c.number_correct, c.number_tested))
    print('Test showed accuracy of {0}'.format(float(c.number_correct)/c.number_tested))