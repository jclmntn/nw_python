class Firm:
    def __init__(self, A, K):
        self.A, self.K = A, K
        self.c = 0.16
    def output(self):
        self.qi = self.A*self.K


class Industry:
    def __init__(self, n=2, A0=0.16, K0=139.58, D = 67):
        self.n = n
        self.A0 = A0
        self.K0 = K0
        self.D = D
        self.firms = []

    def reset(self):
        self.firms = []

    def create(self):
        for i in range(self.n):
            firm = Firm(self.A0, self.K0)
            self.firms.append(firm)

    def price(self):
        self.Qtot = 0
        for firm in self.firms:
            firm.output()
            self.Qtot += firm.qi
            self.p = self.D/self.Qtot
