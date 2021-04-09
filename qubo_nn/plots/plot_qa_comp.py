import pickle
import collections

import numpy as np
import scipy.stats as st
import matplotlib as mpl
from matplotlib import pyplot as plt


mpl.font_manager._rebuild()
plt.rc('font', family='Raleway')
# n = 6
# color = plt.cm.Greens(np.linspace(.3, 1, n))[::-1]
# mpl.rcParams['axes.prop_cycle'] = plt.cycler('color', color)
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.Set2.colors)


def gen_table(kv):
    def calc_ci(key, arr):
        arr = arr[~np.isnan(arr)]
        arr = arr[arr != 0.]
        mean = np.mean(arr, axis=0)
        ci = st.t.interval(
            0.95,
            len(arr) - 1,
            loc=np.mean(arr, axis=0),
            scale=st.sem(arr, axis=0)
        )

        range_ = round(mean - ci[0], 4)
        mean = round(mean, 4)
        return mean, range_

    # First, aggregate.
    kv_new = collections.defaultdict(list)
    for k, v in kv.items():
        kv_new[k[:-1]].extend(v)

    for k, v in kv_new.items():
        # arr = arr[:, 1:201]
        v = np.array(v)
        mean, range_ = calc_ci(k, v[1].max(axis=1))  # r2
        print(k, "R2", "%.3f" % mean, "+-", "%.3f" % range_)


def plot(kv):
    tags = {
        'qa_N_16_norm': '16x16',
        'qa_N_64_norm': '64x64',
        'qa_N_100_norm': '100x100',
        'qa_N_144_norm': '144x144'
    }

    fig, axs = plt.subplots(1, 1, figsize=(5, 3.5))

    def calc_ci(ax, key, arr):
        # arr = arr[~np.isnan(arr)]
        # arr = arr[arr != 0.]
        mean = np.mean(arr, axis=0)
        ci = st.t.interval(
            0.95,
            len(arr) - 1,
            loc=np.mean(arr, axis=0),
            scale=st.sem(arr, axis=0)
        )

        x = np.arange(len(mean))

        ax.plot(x, mean, label=tags[key])
        ax.fill_between(x, ci[0], ci[1], alpha=.2)

    # First, aggregate.
    kv_new = collections.defaultdict(list)
    for k, v in kv.items():
        kv_new[k[:-1]].extend(v)

    for k, v in kv_new.items():
        v = np.array(v)
        calc_ci(axs, k, v[1][:, :200])  # r2

        axs.legend()
        axs.set_ylabel(r'$R^2$')
        axs.set_xlabel("Epoch")

        # # Shrink current axis by 20%
        # box = axs.get_position()
        # axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # # Put a legend to the right of the current axis
        # axs.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    plt.tight_layout()
    plt.show()
    fig.savefig('qa_comp.png')
    fig.savefig('qa_comp.pdf')


def run():
    with open('qa_comp.pickle', 'rb') as f:
        kv = pickle.load(f)
    gen_table(kv)
    plot(kv)


if __name__ == '__main__':
    run()