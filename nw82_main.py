from implementation.nw82_industry import SimNW82
from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    sim = SimNW82(N = 100, n=32, K0= 12.89, rin = 0.194, rim = 0.00097)
    sim.simulate()

    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 2, figure=fig)


    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    ax1.plot(sim.ntprices)
    ax1.set_title("Prices over time")

    ax2.plot(sim.ntb_A)
    ax2.set_title("Available production technique over time")

    ax3.plot(sim.ntIHH)
    ax3.set_xlabel("Time (ticks)")
    ax3.set_title("Inverse HH over time")

    plt.tight_layout()
    plt.show()

