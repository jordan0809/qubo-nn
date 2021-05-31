import os
import pickle
import collections

import numpy as np
import scipy.stats as st
import matplotlib as mpl
from matplotlib import pyplot as plt


NAME = os.path.splitext(__file__)[0][5:]

mpl.font_manager._rebuild()
plt.rc('font', family='Raleway')
# n = 6
# color = plt.cm.Greens(np.linspace(.3, 1, n))[::-1]
# mpl.rcParams['axes.prop_cycle'] = plt.cycler('color', color)
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", plt.cm.Set2.colors)

PLOT_TAGS = [
    {
        'np19_LONG_r2': '64x64',
        'np19_LONG_generalized_gen2_small_arch': '64x64, 48x48',
        'np19_LONG_generalized_gen3_small_arch': '64x64, 48x48, 32x32',
        'np19_LONG_generalized_gen4_small_arch': '64x64, 48x48, 32x32, 24x24',
    },
    {
        'tsp2_r2': '64x64',
        'tsp2_generalized_gen2_small_arch': '64x64, 49x49',
        'tsp2_generalized_gen3_small_arch': '64x64, 49x49, 36x36',
        'tsp2_generalized_gen4_small_arch': '64x64, 49x49, 36x36, 25x25',
    },
    {
        'qa_N_144_norm3': '144x144',
        'qa_N_144_norm3_generalized_50k_gen2_small_arch': '144x144, 100x100',
        'qa_N_144_norm3_generalized_50k_gen3_small_arch': '144x144, 100x100, 64x64',
        'qa_N_144_norm3_generalized_50k_gen4_small_arch': '144x144, 100x100, 64x64, 36x36',
    },
    {
        'a19_2_r2': '64x64',
        'a19_2_generalized_gen2_small_arch': '64x64, 48x48',
        'a19_2_generalized_gen3_small_arch': '64x64, 48x48, 32x32',
        'a19_2_generalized_gen4_small_arch': '64x64, 48x48, 32x32, 24x24',
    },
    {
        'mvc3_r2': '64x64',
        'mvc3_generalized_gen2_small_arch': '64x64, 48x48',
        'mvc3_generalized_gen3_small_arch': '64x64, 48x48, 32x32',
        'mvc3_generalized_gen4_small_arch': '64x64, 48x48, 32x32, 24x24',
    },
    {
        'gc1_r2': '96x96',
        'gc1_generalized_gen2_small_arch': '96x96, 80x80',
        'gc1_generalized_gen3_small_arch': '96x96, 80x80, 64x64',
        'gc1_generalized_gen4_small_arch': '96x96, 80x80, 64x64, 48x48',
    }
]
PLOT_NAMES = [
    'np', 'tsp', 'qa', 'mc', 'mvc', 'gc'
]


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

    for k, v in kv.items():
        # arr = arr[:, 1:201]
        v = np.array(v)
        mean, range_ = calc_ci(k, v[0].max(axis=1))  # r2
        print(k, "R2", "%.3f" % mean, "+-", "%.3f" % range_)


def plot(kv, tags, name):
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

    for k, v in kv.items():
        if k not in tags:
            continue
        v = np.array(v)
        calc_ci(axs, k, v[0][:, :1000])  # r2

        axs.legend()
        axs.set_ylabel(r'$R^2$')
        axs.set_xlabel("Epoch")

    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
    plt.legend(frameon=False)
    plt.ylim((0.5, 1.05))
    plt.tight_layout()
    plt.show()
    fig.savefig(NAME + '_' + name + '.png')
    fig.savefig(NAME + '_' + name + '.pdf')


def run():
    with open(NAME + '.pickle', 'rb') as f:
        kv = pickle.load(f)
    gen_table(kv)
    for plot_tags in PLOT_TAGS:
        plot(kv, plot_tags)


if __name__ == '__main__':
    run()