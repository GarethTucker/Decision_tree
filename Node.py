class Node (object):

    def __init__(self, attribute, true, false, probability):
        self.attribute = attribute
        self.true = true
        self.false = false
        self.probability = probability

    def report(self, indent):
        if not self.true and not self.false:
            print('{0} Class: {1}, prob = {2}'.format(indent, self.attribute, self.probability))
        else:
            print('{0}{1} = TRUE:'.format(indent, self.attribute))
            self.true.report('{0}    '.format(indent))
            print('{0}{1} = FALSE:'.format(indent, self.attribute))
            self.false.report('{0}    '.format(indent))
