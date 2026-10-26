import json
import math
import random

# gets info about what is around and decides to jump or not
INPUTS = 4
HIDDEN = 6


def rand_w():
    return random.uniform(-1, 1)


class Brain:
    def __init__(self):
        # every new bird gets a random brain, everything inside has random importance
        self.w1 = [[rand_w() for _ in range(INPUTS)] for _ in range(HIDDEN)]
        self.b1 = [rand_w() for _ in range(HIDDEN)]
        self.w2 = [rand_w() for _ in range(HIDDEN)]
        self.b2 = rand_w()

    def think(self, inputs):
        # every bird sees the same 4 numbers, but its own brain decides
        # how important each one is, and then if it should jump
        hidden = []
        for i in range(HIDDEN):
            s = self.b1[i]
            for j in range(INPUTS):
                s += self.w1[i][j] * inputs[j]
            hidden.append(math.tanh(s))

        out = self.b2
        for i in range(HIDDEN):
            out += self.w2[i] * hidden[i]
        return out > 0  # True = jump

    def copy(self):
        # copy of the brain, so the most successful birds go to the next generation as they are
        b = Brain()
        b.w1 = [row[:] for row in self.w1]
        b.b1 = self.b1[:]
        b.w2 = self.w2[:]
        b.b2 = self.b2
        return b

    def mutate(self, rate):
        # the child changes a little: a few random weights get a small random change
        for row in self.w1:
            for j in range(len(row)):
                if random.random() < rate:
                    row[j] += random.gauss(0, 0.5)
        for i in range(HIDDEN):
            if random.random() < rate:
                self.b1[i] += random.gauss(0, 0.5)
            if random.random() < rate:
                self.w2[i] += random.gauss(0, 0.5)
        if random.random() < rate:
            self.b2 += random.gauss(0, 0.5)

    def save(self, path):
        # save the brain to a file
        with open(path, "w") as f:
            json.dump({"w1": self.w1, "b1": self.b1, "w2": self.w2, "b2": self.b2}, f)

    @staticmethod
    def load(path):
        # load the brain from a file
        with open(path) as f:
            d = json.load(f)
        b = Brain()
        b.w1, b.b1, b.w2, b.b2 = d["w1"], d["b1"], d["w2"], d["b2"]
        return b


def crossover(a, b):
    # the child takes parts from both parents, which parts is random
    child = a.copy()
    for i in range(HIDDEN):
        if random.random() < 0.5:
            child.w1[i] = b.w1[i][:]
            child.b1[i] = b.b1[i]
            child.w2[i] = b.w2[i]
    return child
