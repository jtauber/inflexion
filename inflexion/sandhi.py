class SandhiRule:
    def __init__(self, rule):
        """
        rule is string of form A|B>C<D|E
        """
        self.a, bcd, self.e = rule.split("|")
        self.b, cd = bcd.split(">")
        self.c, self.d = cd.split("<")
        self.theme = self.a
        self.stem = self.a + self.b
        self.suffix = self.d + self.e
        self.distinguisher = self.c + self.e
        self.surface = self.a + self.c + self.e
