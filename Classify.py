from Node import Node

class Classify (object):

    def __init__(self, data, tree):
        self.test_data = data.test_list

        self.attributes = self.test_data[0]

        self.number_correct = 0
        self.number_tested = 0

        for instance in self.test_data[1:]:
            self.traverse_tree(tree, instance)

    def traverse_tree(self, node, instance):
        if not node.true and not node.false:
            self.number_tested += 1
            if node.attribute == instance[0]:
                self.number_correct += 1
            return
        for index, attribute in enumerate(self.attributes):
            if node.attribute == attribute:
                if instance[index] == 'true':
                    self.traverse_tree(node.true, instance)
                elif instance[index] == 'false':
                    self.traverse_tree(node.false, instance)