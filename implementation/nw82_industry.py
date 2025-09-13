from implementation.simple_industry import Firm, Industry
import numpy as np

class NW82Firm(Firm):
    def __init__(self, A0, K0, rin, rim):
        super().__init__(A0, K0)
        self.rim = rim
        self.rin = rin
        self.Ain = 0
        self.Aim = 0

    def profit(self, p):
        self.pi = p*self.A - (self.c + self.rim + self.rin)

    def innovation(self, an, mu, sigma):
        prob_inn = an*self.rin*self.K

        if np.random.uniform(0,1) < prob_inn:
            Ain = np.exp(np.random.normal(np.log(mu), sigma))
        else:
            Ain = self.A

        self.Ain = Ain

    def imitation(self, am, bestA):
        prob_imi = am*self.rim*self.K

        if np.random.uniform(0,1) < prob_imi:
            Aim = bestA
        else:
            Aim = self.A

        self.Aim = Aim

    def update(self, Qtot, p, bank, delta):
        self.A = max(self.A, self.Aim, self.Ain)
        s = self.qi/float(Qtot)
        rho = p*self.A/float(self.c)
        if s < 1:
            I_d = 1+delta-float(2-s)/float(rho*(2-2*s))
        else:
            I_d = (p-self.c)/p

        if self.pi <= 0:
            b = 0
        else:
            b = bank

        I_p = delta + (b+1)*self.pi
        self.K = (1-delta+max(0, min(I_d, I_p)))*self.K

class NW82Industry(Industry):
    def __init__(self, n=2, K0=139.58, A0=0.16, rin=0.0287, rim=0.00143):
        super().__init__(n, A0, K0)
        self.rin = rin
        self.rim = rim
        self.an, self.am = .125, 1.25
        self.mu, self.sigma = 0.16, 0.05
        self.delta = 0.03
        self.Bank = 1
        self.time = 0
        self.b_A = 0
        self.IHH = self.n
        self.latent = 1.01

    def reset(self):
        self.firms = list()
        self.time = 0
        self.b_A = 0
        self.mu = 0.16


    def create(self):
        for i in range(int(self.n/2)):
            firm = NW82Firm(self.A0, self.K0, self.rin, self.rim)
            self.firms.append(firm)
        for i in range(int((self.n+1)/2)):
            firm = NW82Firm(self.A0, self.K0, 0, self.rim)
            self.firms.append(firm)


    def update_industry(self):
        self.mu *= self.latent
        mux = self.mu
        sigmax = self.sigma
        self.Alist = [self.firms[i].A for i in range(len(self.firms))]
        self.Klist = [self.firms[i].K for i in range(len(self.firms))]
        HH = sum([k**2 for k in
        self.Klist])/float(sum(self.Klist)**2)
        self.IHH = 1/float(HH)
        self.b_A = max(self.Alist)

        for firm in self.firms:
            firm.profit(self.p)
            firm.innovation(self.an, mux, sigmax)
            firm.imitation(self.am, self.b_A)
            firm.update(self.Qtot, self.p, self.Bank, self.delta)
        self.time += 1


class SimNW82:
    def __init__(self,T =100, N= 20, n=2, K0=139.58, A0=0.16, rin=0.0287, rim=0.00143):
        self.T, self.N = T, N
        self.n = n
        self.K0, self.A0 = K0, A0
        self.rin = rin
        self.rim = rim
        self.ntprices = np.zeros((self.T, self.N))
        self.ntIHH = np.zeros((self.T, self.N))
        self.ntb_A= np.zeros((self.T, self.N))

    def simulate(self):
        indus = NW82Industry(self.n, self.K0, self.A0, self.rin, self.rim)
        for i in range(self.N):
            indus.reset()
            indus.create()
            for t in range(self.T):
                indus.price()
                indus.update_industry()
                self.ntprices[t,i] = indus.p
                self.ntIHH[t,i] = indus.IHH
                self.ntb_A[t,i] = indus.b_A
