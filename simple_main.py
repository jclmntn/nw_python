from implementation.simple_industry import Industry
from implementation.nw82_industry import SimNW82
import matplotlib.pyplot as plt

if __name__ == "__main__":

    industry = Industry()
    industry.create()
    industry.price()

    print(f"Results from Simple Industry implementation:\nPrice={industry.p:.4f}, Quantity={industry.Qtot:.4f}")

    sim = SimNW82(N = 100, n=32, K0= 12.89, rin = 0.194, rim = 0.00097)
    sim.simulate()
