from lib.core import C, Input, Output
from lib.utils import CircuitError


class Circuit:
    ELEMENTS = {}

    def __init__(self, **kwargs):
        self._init = kwargs
        self._elements = []
        for elem, names in self.ELEMENTS.items():
            for n in names:
                e = elem()
                self._elements.append(e)
                setattr(self, n, e)
        self._input_names = []
        for name, contact in self.inout().items():
            if not (name.startswith('in') or name.startswith('out')):
                raise CircuitError("Bad contacts name")
            if contact:
                setattr(self, name, contact)
            elif name.startswith("in"):
                setattr(self, name, Input())
                self._input_names.append(name)
            else:
                setattr(self, name, Output())
        self._conductors = []
        for c in self.connect():
            self._conductors.append(C(*c))

    def inout(self):
        return {}

    def connect(self):
        return ()

    def update(self):
        for n, value in self._init.items():
            c = getattr(self, n)
            if n.startswith('in'):
                c.value = value
            else:
                value.value = c.value
        for g in self._elements:
            g.update()
        for c in self._conductors:
            c.update()
        for n in self._input_names:
            getattr(self, n).update()

    def run(self, n=100):
        for _ in range(n):
            self.update()


class Bridge(Circuit):
    def inout(self):
        return {
            "in1": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = self.in1.value


class NOT(Circuit):
    def inout(self):
        return {
            "in1": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(not self.in1.value)


class AND(Circuit):
    def inout(self):
        return {
            "in1": None,
            "in2": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(self.in1.value and self.in2.value)


class OR(Circuit):
    def inout(self):
        return {
            "in1": None,
            "in2": None,
            "out1": None
        }

    def update(self):
        super().update()
        self.out1.value = int(self.in1.value or self.in2.value)


class NOR(Circuit):
    ELEMENTS = {
        OR: ("o1",),
        NOT: ("n1",)
    }

    def inout(self):
        return {
            "in1": self.o1.in1,
            "in2": self.o1.in2,
            "out1": self.n1.out1
        }

    def connect(self):
        return (
            (self.o1.out1, self.n1.in1),
        )


class NAND(Circuit):
    ELEMENTS = {
        NOT: ("n1",),
        AND: ("a1",)
    }

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "out1": self.n1.out1,
        }

    def connect(self):
        return (
            (self.a1.out1, self.n1.in1),
        )


class XOR(Circuit):
    ELEMENTS = {
        OR: ("o1",),
        AND: ("a1", "a2"),
        NOT: ("n1", "n2"),
        Bridge: ("b1", "b2"),
    }

    def inout(self):
        return {
            "in1": self.b1.in1,
            "in2": self.b2.in1,
            "out1": self.o1.out1
        }

    def connect(self):
        return (
            (self.b1.out1, self.n1.in1),
            (self.b2.out1, self.n2.in1),
            (self.b2.out1, self.a1.in1),
            (self.n1.out1, self.a1.in2),
            (self.b1.out1, self.a2.in1),
            (self.n2.out1, self.a2.in2),
            (self.a1.out1, self.o1.in1),
            (self.a2.out1, self.o1.in2)
        )


class AND3(Circuit):
    ELEMENTS = {
        AND: ("a1", "a2")
    }

    def inout(self):
        return {
            "in1": self.a1.in1,
            "in2": self.a1.in2,
            "in3": self.a2.in1,
            "out1": self.a2.out1
        }

    def connect(self):
        return (
            (self.a1.out1, self.a2.in2),
        )


class OR3(Circuit):
    ELEMENTS = {
        OR: ("o1", "o2",),
    }

    def inout(self):
        return {
            "in1": self.o1.in1,
            "in2": self.o1.in2,
            "in3": self.o2.in1,
            "out1": self.o2.out1
        }

    def connect(self):
        return (
            (self.o1.out1, self.o2.in2),
        )


class XNOR(Circuit):
    ELEMENTS = {
        XOR: ("xo1",),
        NOT: ("n1",)
    }

    def inout(self):
        return {
            "in1": self.xo1.in1,
            "in2": self.xo1.in2,
            "out1": self.n1.out1
        }

    def connect(self):
        return (
            (self.xo1.out1, self.n1.in1),
        )


class ODD(Circuit):
    ELEMENTS = {
        XOR: ("xo1", "xo2", "xo3", "xo4"),
    }

    def inout(self):
        return {
            "in1": self.xo3.in1,
            "in2": self.xo2.in1,
            "in3": self.xo1.in1,
            "in4": self.xo1.in2,
            "out1": self.xo3.out1
        }

    def connect(self):
        return (
            (self.xo1.out1, self.xo2.in2),
            (self.xo2.out1, self.xo3.in2)
        )


class MT1(Circuit):  # (x1∨x2∨x3∨x4) ∧ (x1∨x2∨x3∨¬x4) ∧ (x1∨x2∨¬x3∨x4) ∧ (x1∨¬x2∨x3∨x4) ∧ (¬x1∨x2∨x3∨x4)
    ELEMENTS = {
        AND: ("a1", "a2", "a3", "a4", "a5", "a6"),
        OR3: ("or1", "or2"),
        OR: ("o1",),
        Bridge: ("b1", "b2", "b3", "b4")
    }

    def inout(self):
        return {
            "in1": self.b1.in1,
            "in2": self.b2.in1,
            "in3": self.b3.in1,
            "in4": self.b4.in1,
            "out1": self.o1.out1
        }

    def connect(self):
        return (
            (self.b1.out1, self.a1.in1),
            (self.b2.out1, self.a1.in2),
            (self.b1.out1, self.a2.in1),
            (self.b3.out1, self.a2.in2),
            (self.b1.out1, self.a3.in1),
            (self.b4.out1, self.a3.in2),
            (self.b2.out1, self.a4.in1),
            (self.b3.out1, self.a4.in2),
            (self.b2.out1, self.a5.in1),
            (self.b4.out1, self.a5.in2),
            (self.b3.out1, self.a6.in1),
            (self.b4.out1, self.a6.in2),

            (self.a1.out1, self.or1.in1),
            (self.a2.out1, self.or1.in2),
            (self.a3.out1, self.or1.in3),
            (self.a4.out1, self.or2.in1),
            (self.a5.out1, self.or2.in2),
            (self.a6.out1, self.or2.in3),

            (self.or1.out1, self.o1.in1),
            (self.or2.out1, self.o1.in2)
        )


class SC(Circuit):
    ELEMENTS = {
        AND3: ("ad1", "ad2", "ad3", "ad4", "ad5", "ad6", "ad7", "ad8"),
        OR: ("o1", "o2", "o3", "o4",),
        NOT: ("n1", "n2", "n3"),
        Bridge: ("b1", "b2", "b3")

    }

    def inout(self):
        return {
            "in1": self.b1.in1,
            "in2": self.b2.in1,
            "in3": self.b3.in1,
            "out1": self.ad1.out1,
            "out2": self.o2.out1,
            "out3": self.o4.out1,
            "out4": self.ad8.out1
        }

    def connect(self):
        return (
            (self.b1.out1, self.n1.in1),
            (self.b2.out1, self.n2.in1),
            (self.b3.out1, self.n3.in1),


            (self.n1.out1, self.ad1.in1),
            (self.n2.out1, self.ad1.in2),
            (self.n3.out1, self.ad1.in3),


            (self.n1.out1, self.ad2.in1),
            (self.n2.out1, self.ad2.in2),
            (self.b3.out1, self.ad2.in3),

            (self.n1.out1, self.ad3.in1),
            (self.b2.out1, self.ad3.in2),
            (self.n3.out1, self.ad3.in3),

            (self.b1.out1, self.ad4.in1),
            (self.n2.out1, self.ad4.in2),
            (self.n3.out1, self.ad4.in3),

            (self.ad2.out1, self.o1.in1),
            (self.ad3.out1, self.o1.in2),
            (self.o1.out1, self.o2.in1),
            (self.ad4.out1, self.o2.in2),


            (self.n1.out1, self.ad5.in1),
            (self.b2.out1, self.ad5.in2),
            (self.b3.out1, self.ad5.in3),

            (self.b1.out1, self.ad6.in1),
            (self.n2.out1, self.ad6.in2),
            (self.b3.out1, self.ad6.in3),

            (self.b1.out1, self.ad7.in1),
            (self.b2.out1, self.ad7.in2),
            (self.n3.out1, self.ad7.in3),

            (self.ad5.out1, self.o3.in1),
            (self.ad6.out1, self.o3.in2),
            (self.o3.out1, self.o4.in1),
            (self.ad7.out1, self.o4.in2),


            (self.b1.out1, self.ad8.in1),
            (self.b2.out1, self.ad8.in2),
            (self.b3.out1, self.ad8.in3),

        )


class HADD(Circuit):
    ELEMENTS = {
        AND: ("a1", "a2"),
        OR: ("o1",),
        NOT: ("n1",),
        Bridge: ("b1", "b2", "b3")
    }

    def inout(self):
        return {
            "in1": self.b1.in1,
            "in2": self.b2.in1,
            "out1": self.a2.out1,
            "out2": self.b3.out1
        }

    def connect(self):
        return (
            (self.b1.out1, self.o1.in1),
            (self.b2.out1, self.o1.in2),
            (self.b1.out1, self.a1.in1),
            (self.b2.out1, self.a1.in2),
            (self.a1.out1, self.b3.in1),
            (self.b3.out1, self.n1.in1),
            (self.o1.out1, self.a2.in1),
            (self.n1.out1, self.a2.in2),

        )


class ADD(Circuit):
    ELEMENTS = {
        HADD: ("h1", "h2"),
        OR: ("o1",)
    }

    def inout(self):
        return {
            "in1": self.h2.in1,
            "in2": self.h1.in1,
            "in3": self.h1.in2,
            "out1": self.h2.out1,
            "out2": self.o1.out1
        }

    def connect(self):
        return (
            (self.h1.out1, self.h2.in2),
            (self.h1.out2, self.o1.in1),
            (self.h2.out2, self.o1.in2)

        )