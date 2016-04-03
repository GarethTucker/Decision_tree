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

def report(indent, node):
        if not node.true and not node.false:
            output_file.write('{0} Class: {1}, prob = {2}\n'.format(indent, node.attribute, node.probability))
        else:
            output_file.write('{0}{1} = TRUE:\n'.format(indent, node.attribute))
            report(('{0}    '.format(indent)), node.true)
            output_file.write('{0}{1} = FALSE:\n'.format(indent, node.attribute))
            report(('{0}    '.format(indent)), node.false)

if __name__=="__main__":
    data = Main('data/hepatitis-test.dat', 'data/hepatitis-training.dat')
    # print('\n'.join([' '.join([format(item) for item in row])
    #                  for row in data.training_list]))
    t = Tree(data)

    output_file = open('../decision_tree_classification.txt', 'w')

    tree = t.tree
    report('', tree)
    output_file.write('Classifying test data...\n')
    c = Classify(data, tree)
    output_file.write('Num correct: {0}, Num tested: {1}\n'.format(c.number_correct, c.number_tested))
    output_file.write('Test showed accuracy of {0}\n'.format(float(c.number_correct)/c.number_tested))

    output_file.write('\nClassifying data split into 10...\n')
    total_accuracy_of_ten_runs = 0
    for i in range(1, 11):
        test_file_name = 'data/hepatitis-test-run'
        training_file_name = 'data/hepatitis-training-run'
        i = str(0)+str(i) if i < 10 else str(i)
        test_file_name = test_file_name+i+'.dat'
        training_file_name = training_file_name+i+'.dat'
        data = Main(test_file_name, training_file_name)
        t=Tree(data)
        tree = t.tree
        c = Classify(data, tree)
        run_accuracy = float(c.number_correct)/c.number_tested
        output_file.write('run {0} accuracy: {1}\n'.format(i, run_accuracy))
        total_accuracy_of_ten_runs += run_accuracy
    average_accuracy_of_ten_runs = total_accuracy_of_ten_runs/10
    output_file.write('average accuracy of ten runs: {0}\n'.format(average_accuracy_of_ten_runs))