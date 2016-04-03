from Node import Node
import copy

class Tree (object):

    def __init__(self, data):
        self.results = data.test_list[0]
        data.test_list = data.test_list[1:]
        data.training_list = data.training_list[1:]

        attributes = data.training_list[0]
        instances = data.training_list[1:]

        split = self.split_by_results(instances)
        self.baseline_probablity = split[0]/split[1]

        self.tree = self.build_tree(instances, attributes)

    def build_tree(self, instances, attributes):
        # if instances is empty
        #       return a leaf node containing the name and probability of the overall most probable class(ie the baseline predictor
        if not instances:
            return Node(self.results[1], None, None, self.baseline_probablity)

        # if instances are pure
        #       return a leaf node containing the name of the class of the instances in the node and probability 1
        instances_results = []
        for row in instances:
            instances_results.append(row[0])
        if len(set(instances_results)) < 2:
            return Node(instances_results[0], None, None, 1)


        # if attributes is empty
        #       return a leaf node containing the name and probability of the majority class of the instances in the node (choosen randomly if equal)
        if not len(attributes) > 1:
            results_split = self.split_by_results(instances)
            number_in_first_result = results_split[0]
            number_in_second_result = results_split[1]
            if number_in_first_result > number_in_second_result:
                probability = number_in_second_result/number_in_first_result
                return Node(self.results[0], None, None, probability)
            else:
                probability = number_in_first_result/number_in_second_result
                return Node(self.results[1], None, None, probability)

        # else get purest attribute
        purest_attribute = ''
        purity_of_purest_attribute = 1
        best_instance_trues = []
        best_instance_falses = []

        for index, attribute in enumerate(attributes[1:]):

            split =  self.split_into_trues_and_falses(instances, index)
            trues = split[0]
            falses = split[1]

            number_of_trues = float(len(trues))
            number_of_falses = float(len(falses))

            trues_split_by_result = self.split_by_results(trues)
            number_of_trues_in_first_result = trues_split_by_result[0]
            number_of_trues_in_second_result = trues_split_by_result[1]

            falses_split_by_result = self.split_by_results(falses)
            number_of_falses_in_first_result = falses_split_by_result[0]
            number_of_falses_in_second_result = falses_split_by_result[1]

            if number_of_trues > 0:
                trues_impurity = (number_of_trues_in_first_result/number_of_trues)*(number_of_trues_in_second_result/number_of_trues)
            else:
                trues_impurity = 0
            if number_of_falses > 0:
                falses_impurity = (number_of_falses_in_first_result/number_of_falses)*(number_of_falses_in_second_result/number_of_falses)
            else:
                falses_impurity = 0


            trues_weighted_impurity = trues_impurity*(number_of_trues/len(instances))
            falses_weighted_impurity = falses_impurity*(number_of_falses/len(instances))
            attribute_impurity = trues_weighted_impurity+falses_weighted_impurity

            if attribute_impurity < purity_of_purest_attribute:
                purity_of_purest_attribute = attribute_impurity
                purest_attribute = attribute

                best_instance_trues = self.remove_attribute(trues, index+1)
                best_instance_falses = self.remove_attribute(falses, index+1)

        new_attributes = copy.deepcopy(attributes)
        new_attributes.remove(purest_attribute)

        true = self.build_tree(best_instance_trues, new_attributes)
        false = self.build_tree(best_instance_falses, new_attributes)
        return Node(purest_attribute, true, false, 0)

    def split_into_trues_and_falses(self, instances, index):
        trues = []
        falses = []
        for instance in instances:
            if instance[index+1] == 'true':
                trues.append(instance)
            elif instance[index+1] == 'false':
                falses.append(instance)
        return [trues, falses]

    def split_by_results(self, set):
        number_in_first_result = 0.0
        number_in_second_result = 0.0
        for instance in set:
            if instance[0] == self.results[0]:
                number_in_first_result += 1.0
            elif instance[0] == self.results[1]:
                number_in_second_result += 1.0
        return[float(number_in_first_result), float(number_in_second_result)]

    def remove_attribute(self, set, index):
        best_instance = copy.deepcopy(set)
        for row in best_instance:
            row.pop(index)
        return best_instance