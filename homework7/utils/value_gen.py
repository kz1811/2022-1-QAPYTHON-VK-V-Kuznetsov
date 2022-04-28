import random
import string


class Generator:

    def rand_gen(self, num=20):
        name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(num))
        return name

    def name(self):
        return self.rand_gen(6)

    def surname(self):
        return self.rand_gen(8)
