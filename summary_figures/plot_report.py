"""All figures of pr_results_summary.tex, drawn at the text width (16.6 cm) with the 10 pt document font.

fig_si_parts_noise.pdf  Si: parts of the RPA energy vs a, and their deviation from a smooth fit
fig_si_grid.pdf         Si: RPA a0 and bulk modulus vs RI basis / RI-RS grid, grid optimised at every a and frozen
fig_materials.pdf       C, SiC, BN, MgO, LiF: a0 and bulk modulus minus reference
fig_ae_rpa_noise.pdf    all-electron Si: deviation of E^EXX and E_c from a smooth fit
fig_dlp_time.pdf        d_lP: time of the quadrature / time of the analytic evaluation, automatic choice
fig_gw_gaps.pdf         all-electron G0W0 gaps of diamond and silicon

Run with a Python that has numpy and matplotlib. Reads the fits and data in data/."""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator, MultipleLocator

HERE = os.path.dirname(os.path.abspath(__file__))
RES = f"{HERE}/data"

HA_EV = 27.211386245988  # eV per hartree

plt.rcParams.update({"font.size": 10, "mathtext.fontset": "cm", "font.family": "serif", "font.serif": ["cmr10"],
                     "axes.formatter.use_mathtext": True, "axes.unicode_minus": False,
                     "axes.grid": True, "grid.alpha": 0.3, "legend.fontsize": 9})
LEG = dict(frameon=True, fancybox=False, edgecolor="black", facecolor="white", framealpha=1)
WIDTH = 16.6 / 2.54
BLUE, ORANGE, GREEN, GREY = "#0072B2", "#D55E00", "#009E73", "#999999"
BASIS_STYLE = {"T": ("o", BLUE, "cc-pVTZ"), "Q": ("s", ORANGE, "cc-pVQZ"), "X": ("D", "black", r"$X^{-3}$ limit")}


def panel_label(ax, letter):
    ax.text(0.02, 0.96, f"({letter})", transform=ax.transAxes, va="top", ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))


def si_parts_noise():
    data = json.load(open(f"{RES}/si_eos_overview/eos_data.json"))["rpa"]
    q, fine = data["tight_QZ"], data["fine_TZ"]
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2.6))
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.18, top=0.82, wspace=0.40)
    parts = (("PBE total energy", GREY, "o", lambda s: np.array(s["E_DFT"])),
             ("Hartree-Fock energy", BLUE, "s", lambda s: np.array(s["E_DFT"]) - np.array(s["E_xc"]) + np.array(s["E_EXX"])),
             ("RPA correlation energy", ORANGE, "^", lambda s: np.array(s["E_c"])))
    a = np.array(q["a"])
    i0 = list(a).index(5.46)
    for lab, col, m, energy in parts:
        v = energy(q)
        axes[0].plot(a * 100, (v - v[i0]) * HA_EV * 1000, m + "-", color=col, ms=4, label=lab)
    v = parts[1][3](q) + parts[2][3](q)
    axes[0].plot(a * 100, (v - v[i0]) * HA_EV * 1000, "D-", color=GREEN, ms=4, label="RPA total energy")
    axes[0].set_ylabel(r"$E(a)-E(546\,\mathrm{pm})$ (meV)")
    axes[0].set_xlabel(r"lattice constant $a$ (pm)")
    axes[0].xaxis.set_major_locator(MultipleLocator(10))
    af = np.array(fine["a"])
    x = (af ** 3 / 4) ** (-2 / 3)
    for lab, col, m, energy in parts:
        e = energy(fine) * HA_EV
        axes[1].plot(af * 100, (e - np.polyval(np.polyfit(x, e, 3), x)) * 1e3, m + "-", color=col, ms=4, lw=1.0)
    axes[1].set_ylabel("deviation from smooth fit (meV)")
    axes[1].set_xlabel(r"lattice constant $a$ (pm)")
    axes[1].xaxis.set_major_locator(MultipleLocator(2))
    axes[1].yaxis.set_major_locator(MultipleLocator(1))
    panel_label(axes[0], "a")
    panel_label(axes[1], "b")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="upper center", ncol=4, **LEG)
    fig.savefig(f"{HERE}/fig_si_parts_noise.pdf")
    plt.close(fig)


def si_grid():
    # fits_matrix.txt: basis RI RS | frozen a0 B0 B0' rms | optimised-at-every-a a0 B0 rms
    frozen, optimised = {}, {}
    for line in open(f"{RES}/si_gthhf_frozen_grid/fits_matrix.txt"):
        if line.startswith("#"):
            continue
        key, fro, opt = [part.split() for part in line.split("|")]
        frozen[(key[0], int(key[1]), int(key[2]))] = (float(fro[0]), float(fro[1]))
        optimised[(key[0], int(key[1]), int(key[2]))] = (float(opt[0]), float(opt[1]))
    settings = [(3, 14), (4, 14), (5, 14), (3, 20), (4, 20), (5, 20)]
    x = np.arange(len(settings))
    fig, axs = plt.subplots(2, 2, figsize=(WIDTH, 4.0), sharex=True, sharey="row")
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.10, top=0.86, wspace=0.09, hspace=0.10)
    for col, (fits, title) in enumerate(((optimised, r"RI-RS grid optimised at every $a$"),
                                         (frozen, r"RI-RS grid optimised once and frozen"))):
        for row in range(2):
            ax = axs[row, col]
            for b, (m, c, name) in BASIS_STYLE.items():
                y = np.array([fits[(b, *st)][row] if (b, *st) in fits else np.nan for st in settings])
                ax.plot(x, (y - 5.4) * 1000 if row == 0 else y, m + "-", color=c, ms=4, label=name)
            if row == 0:
                ax.axhline(21, color="black", ls=":", lw=1, label="experiment")
                ax.axhline(14, color="black", ls="--", lw=1, label="RPA, plane waves (ONCV)")
                ax.set_title(title, fontsize=10)
                ax.yaxis.set_major_locator(MultipleLocator(5))
            else:
                ax.axhline(99.2, color="black", ls=":", lw=1)
                ax.yaxis.set_major_locator(MultipleLocator(1))
            panel_label(ax, "abcd"[2 * row + col])
        axs[1, col].set_xticks(x, [f"RI {ri}\nRS {rs}" for ri, rs in settings])
    axs[0, 0].set_ylabel(r"$a_0-5.400\,\mathrm{\AA}$ (m$\mathrm{\AA}$)")
    axs[1, 0].set_ylabel("bulk modulus (GPa)")
    fig.legend(*axs[0, 0].get_legend_handles_labels(), loc="upper center", ncol=5, columnspacing=1.2, **LEG)
    fig.savefig(f"{HERE}/fig_si_grid.pdf")
    plt.close(fig)


def materials():
    # a0 (Å) and B0 (GPa): all-electron PBE, plane-wave RPA with PAW and with ONCV (references.py of the EOS folder)
    ref = {}
    exec(open(f"{RES}/eos_c_sic_bn_mgo_lif/references.py").read(), ref)
    ref = ref["REF"]
    fits = {}
    for line in open(f"{RES}/eos_c_sic_bn_mgo_lif/fits.txt"):
        if line.startswith("#"):
            continue
        key, val = line.split("|")
        mat, basis, ri, rs, method = key.split()
        fits[(mat, basis, int(ri), int(rs), method)] = [float(v) for v in val.split()]
    names = {"c": "C", "sic": "SiC", "bn": "BN", "mgo": "MgO", "lif": "LiF"}

    def best(mat, method):
        for basis in (("X", "Q") if method == "RPA" else ("Q",)):
            for ri, rs in ((4, 18), (3, 14)):
                if (mat, basis, ri, rs, method) in fits:
                    return fits[(mat, basis, ri, rs, method)]

    fig, axs = plt.subplots(1, 2, figsize=(WIDTH, 2.7))
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.11, top=0.83, wspace=0.28)
    x = np.arange(len(names))
    pairs = (("PBE", "PBE AE", "o", GREEN, GREEN, "PBE vs all-electron PBE"),
             ("RPA", "RPA PAW", "s", ORANGE, ORANGE, "RPA vs RPA (PAW)"),
             ("RPA", "RPA ONCV", "D", ORANGE, "white", "RPA vs RPA (ONCV)"))
    for ax, column, letter in zip(axs, (0, 1), "ab"):
        for j, (method, ref_name, m, c, face, lab) in enumerate(pairs):
            y = []
            for mat, name in names.items():
                r = ref[name].get(ref_name, (None, None))[column]
                y.append((1000 if column == 0 else 1) * (best(mat, method)[column] - r) if r else np.nan)
            ax.plot(x + 0.15 * (j - 1), y, m, color=c, mfc=face, ms=6, label=lab)
        ax.axhline(0, color="black", lw=0.8)
        ax.set_xticks(x, names.values())
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=7))
        low, high = ax.get_ylim()
        ax.set_ylim(low, high + 0.22 * (high - low))
        panel_label(ax, letter)
    axs[0].set_ylabel(r"$a_0-a_0^\mathrm{ref}$ (m$\mathrm{\AA}$)")
    axs[1].set_ylabel(r"bulk modulus $-$ reference (GPa)")
    fig.legend(*axs[0].get_legend_handles_labels(), loc="upper center", ncol=3, **LEG)
    fig.savefig(f"{HERE}/fig_materials.pdf")
    plt.close(fig)


def ae_rpa_noise():
    folder = f"{RES}/si_allelectron_ccpvxz_s"
    bases = (("dzs", "cc-pVDZ-s", "o", BLUE), ("tzs", "cc-pVTZ-s", "s", ORANGE), ("qzs", "cc-pVQZ-s", "^", GREEN))
    panels = (("exx_tab", r"$E^\mathrm{EXX}$, tabulated grid", 200, 100),
              ("exx_opt", r"$E^\mathrm{EXX}$, grid optimised at every $a$", 200, 100),
              ("ec_tab", r"$E_\mathrm{c}^\mathrm{RPA}$, tabulated grid", 4, 2),
              ("ec_opt", r"$E_\mathrm{c}^\mathrm{RPA}$, grid optimised at every $a$", 60, 30))
    fig, axs = plt.subplots(2, 2, figsize=(WIDTH, 4.3), sharex=True)
    fig.subplots_adjust(left=0.10, right=0.99, bottom=0.11, top=0.87, wspace=0.22, hspace=0.25)
    for ax, (key, title, ymax, step), letter in zip(axs.flat, panels, "abcd"):
        for b, name, m, c in bases:
            d = np.loadtxt(f"{folder}/{key}_{b}_res.dat", skiprows=1)
            ax.plot(100 * d[:, 0], d[:, 1], m + "-", color=c, lw=1, ms=4, label=name)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_ylim(-1.3 * ymax, 1.3 * ymax)
        ax.yaxis.set_major_locator(MultipleLocator(step))
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.set_title(title, fontsize=10)
        panel_label(ax, letter)
    for ax in axs[:, 0]:
        ax.set_ylabel("deviation from fit (meV)")
    for ax in axs[1, :]:
        ax.set_xlabel(r"lattice constant $a$ (pm)")
    fig.legend(*axs[0, 0].get_legend_handles_labels(), loc="upper center", ncol=3, **LEG)
    fig.savefig(f"{HERE}/fig_ae_rpa_noise.pdf")
    plt.close(fig)


def dlp_time():
    # (crystal and AO basis, time analytic (s), time quadrature (s), automatic choice, which time is an estimate);
    # 4 nodes, all-electron (AE) cases 1 node
    cases = (("MgO, aug-SZV", 7.7, 195, "analytic", ""), ("GaAs, aug-SZV", 4.0, 87, "analytic", ""),
             ("AlAs, aug-SZV", 1.6, 21.6, "analytic", ""), ("TiO$_2$, aug-SZV", 28.3, 75.8, "analytic", ""),
             ("Si, aug-SZV", 1.3, 4.5, "analytic", ""), ("GaAs, aug-TZVP", 466, 2562, "analytic", ""),
             ("AlAs, aug-TZVP", 125, 25, "quadrature", ""), ("WS$_2$, aug-TZVP", 94, 75, "analytic", ""),
             ("Si, aug-TZVP", 529, 164, "quadrature", ""), ("TiO$_2$, aug-DZVP", 2000, 924, "quadrature", "analytic"),
             ("Si, pc-2 (AE)", 43.5, 1e10, "analytic", "quadrature"), ("C, pc-2 (AE)", 98.2, 7e6, "analytic", "quadrature"))
    fig, ax = plt.subplots(figsize=(WIDTH, 3.4))
    fig.subplots_adjust(left=0.20, right=0.98, bottom=0.14, top=0.85)
    for i, (name, t_analytic, t_quadrature, choice, estimate) in enumerate(cases):
        c = BLUE if choice == "analytic" else ORANGE
        ax.plot(t_quadrature / t_analytic, i, "o" if choice == "analytic" else "s", ms=7, color=c,
                mfc="white" if estimate else c, mew=1.5)
    ax.axvline(1, color="black", lw=0.8)
    ax.set_xscale("log")
    ax.set_xlim(0.05, 1e11)
    ax.set_xticks([10.0 ** n for n in range(-1, 12, 2)])
    ax.set_yticks(np.arange(len(cases)), [c[0] for c in cases], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("time of the quadrature / time of the analytic evaluation")
    handles = [plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=7, label="code chooses analytic"),
               plt.Line2D([], [], marker="s", ls="", color=ORANGE, ms=7, label="code chooses quadrature"),
               plt.Line2D([], [], marker="o", ls="", color=GREY, mfc="white", mew=1.5, ms=7, label="one time estimated")]
    fig.legend(handles=handles, loc="upper center", ncol=3, **LEG)
    fig.savefig(f"{HERE}/fig_dlp_time.pdf")
    plt.close(fig)


def gw_gaps():
    # G0W0@PBE indirect gaps (eV): (AO basis, RI functions per atom, gap)
    diamond = (("aug-SZV", 45, 5.387), ("aug-SZV", 54, 5.394), ("aug-DZVP", 60, 5.481), ("aug-DZVP", 67, 5.474),
               ("aug-TZVP", 73, 5.596), ("aug-TZVP", 84, 5.597))
    silicon = (("aug-SZV", 69, 0.997), ("aug-SZV", 105, 0.986), ("aug-DZVP", 70, 0.879), ("aug-DZVP", 115, 0.981),
               ("aug-DZVP", 237, 0.985), ("aug-TZVP", 104, 0.979), ("aug-TZVP", 115, 1.062), ("aug-TZVP", 237, 1.028))
    references = {"diamond": (("CP2K, GTH pseudopotential", 5.590, "-"), ("FHI-aims, all-electron", 5.60, "--"),
                              ("FHI-aims, all-electron", 5.69, "--"), ("VASP, PAW", 5.72, ":")),
                  "silicon": (("CP2K, GTH pseudopotential", 1.166, "-"), ("FHI-aims, all-electron", 1.13, "--"),
                              ("FHI-aims, all-electron", 1.12, "--"), ("VASP, PAW", 1.30, ":"))}
    fig, axs = plt.subplots(1, 2, figsize=(WIDTH, 3.0), gridspec_kw={"width_ratios": [6, 8]})
    fig.subplots_adjust(left=0.09, right=0.99, bottom=0.20, top=0.80, wspace=0.18)
    for ax, data, name, letter in ((axs[0], diamond, "diamond", "a"), (axs[1], silicon, "silicon", "b")):
        x = np.arange(len(data))
        ax.plot(x, [g for _, _, g in data], "s", color=BLUE, ms=6, label="CP2K, all-electron (this PR)")
        seen = set()
        for lab, value, ls in references[name]:
            ax.axhline(value, color="black", ls=ls, lw=0.9, label=None if lab in seen else lab)
            seen.add(lab)
        ax.set_xticks(x, [n for _, n, _ in data])
        for basis in dict.fromkeys(b for b, _, _ in data):
            members = [k for k, (b, _, _) in enumerate(data) if b == basis]
            ax.text(np.mean(members), -0.17, basis, transform=ax.get_xaxis_transform(), ha="center", va="top")
            ax.axvline(members[-1] + 0.5, color=GREY, lw=0.6)
        ax.set_xlim(-0.6, len(data) - 0.4)
        ax.set_title(name, fontsize=10)
        ax.grid(axis="x", visible=False)
        panel_label(ax, letter)
    axs[0].set_ylim(5.3, 5.8)
    axs[1].set_ylim(0.8, 1.4)
    for ax in axs:
        ax.yaxis.set_major_locator(MultipleLocator(0.1))
    axs[0].set_ylabel(r"$G_0W_0$ gap (eV)")
    fig.legend(*axs[0].get_legend_handles_labels(), loc="upper center", ncol=4, columnspacing=1.0, fontsize=8, **LEG)
    fig.savefig(f"{HERE}/fig_gw_gaps.pdf")
    plt.close(fig)


if __name__ == "__main__":
    si_parts_noise()
    si_grid()
    materials()
    ae_rpa_noise()
    dlp_time()
    gw_gaps()
