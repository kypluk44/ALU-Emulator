import random
from unittest import TestCase
from itertools import product

from lib.utils import Display, CircuitError
from lib.circuit import NOR, NAND, XOR, AND3, OR3, XNOR, ODD, MT1, HADD, \
    ADD, SC, NOT8, AND8, OR8, EQ8, NEQ8, GT8, LT8, GTE8, LTE8, ADD8, ALU


class BaseTest(TestCase):
    IN = 0
    OUT = 0
    CIRCUIT = None

    @staticmethod
    def F(*args):
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_tm()

    def init_tm(self):
        self.TM = {}
        for i in product((0, 1), repeat=self.IN):
            if self.IN >= 10:
                if random.random() > 0.01:
                    continue
            self.TM[i] = self.F(*i)

    def init_circuit(self, inputs):
        d = Display(self.OUT)
        kwargs = {}
        for i in range(self.IN):
            kwargs[f'in{i + 1}'] = inputs[i]
        for i in range(self.OUT):
            kwargs[f'out{i + 1}'] = getattr(d, f"c{i + 1}")
        c = self.CIRCUIT(**kwargs)
        return c, d

    def test(self):
        if not self.CIRCUIT:
            return
        if not self.CIRCUIT.ELEMENTS:
            raise CircuitError("Empty scheme")
        for inputs, outputs in self.TM.items():
            if outputs is None:
                continue
            c, d = self.init_circuit(inputs)
            c.run()
            if not d.check(outputs):
                print(f"Input: {inputs}, output: {d.res()}, correct: {outputs}")
                raise Exception


class TestNOR(BaseTest):
    IN = 2
    OUT = 1
    CIRCUIT = NOR

    @staticmethod
    def F(a, b):
        return not (a or b)


class TestNAND(BaseTest):
    IN = 2
    OUT = 1
    CIRCUIT = NAND

    @staticmethod
    def F(a, b):
        return not (a and b)


class TestXOR(BaseTest):
    IN = 2
    OUT = 1
    CIRCUIT = XOR

    @staticmethod
    def F(a, b):
        return (a + b) % 2


class TestAND3(BaseTest):
    IN = 3
    OUT = 1
    CIRCUIT = AND3

    @staticmethod
    def F(a, b, c):
        return a and b and c


class TestOR3(BaseTest):
    IN = 3
    OUT = 1
    CIRCUIT = OR3

    @staticmethod
    def F(a, b, c):
        return a or b or c


class TestXNOR(BaseTest):
    IN = 2
    OUT = 1
    CIRCUIT = XNOR

    @staticmethod
    def F(a, b):
        return (a + b + 1) % 2


class TestODD(BaseTest):
    IN = 4
    OUT = 1
    CIRCUIT = ODD

    @staticmethod
    def F(a, b, c, d):
        return (a + b + c + d) % 2


class TestMT1(BaseTest):
    IN = 4
    OUT = 1
    CIRCUIT = MT1

    @staticmethod
    def F(a, b, c, d):
        return (a + b + c + d) > 1


class TestSC(BaseTest):
    IN = 3
    OUT = 4
    CIRCUIT = SC

    @staticmethod
    def F(a, b, c):
        res = [0, 0, 0, 0]
        res[a + b + c] = 1
        return res


class TestHADD(BaseTest):
    IN = 2
    OUT = 2
    CIRCUIT = HADD

    @staticmethod
    def F(a, b):
        return [(a + b) % 2, a and b]


class TestADD(BaseTest):
    IN = 3
    OUT = 2
    CIRCUIT = ADD

    @staticmethod
    def F(a, b, c):
        return [(a + b + c) % 2, a + b + c >= 2]