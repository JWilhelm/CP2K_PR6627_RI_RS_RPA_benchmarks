"""Tables of pr_results_summary.tex: PBE and RPA lattice constants and bulk moduli of Si, C, SiC, BN, MgO, LiF
with the mean absolute error (MAE) with respect to experiment. Writes tables.tex and tables.md.

CP2K values: cc-pVQZ, k mesh 8x8x8; PBE with GTH-PBE, RPA with GTH-HF, RI 4, RS 18 (Si: RS 20)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = f"{HERE}/data"
SOLIDS = ("Si", "C", "SiC", "BN", "MgO", "LiF")
KEY = {"C": "c", "SiC": "sic", "BN": "bn", "MgO": "mgo", "LiF": "lif"}

# reference values, (a0 in A, B0 in GPa)
EXP = {"Si": (5.421, 101), "C": (3.553, 455), "SiC": (4.346, 229), "BN": (3.592, 410), "MgO": (4.189, 165),
       "LiF": (3.972, 76.3)}
PBE_AE = {"Si": (5.476, 89.0), "C": (3.575, 435), "SiC": (4.384, 213), "BN": (3.628, 374), "MgO": (4.254, 149.0),
          "LiF": (4.069, 67.2)}
PBE_PAW = {"Si": (5.469, 87.8), "C": (3.574, 431), "SiC": (4.380, 210), "BN": (3.626, 370), "LiF": (4.068, 67.3)}
PBE_ONCV = {"Si": (5.479, None), "C": (3.567, None), "BN": (3.621, None), "MgO": (4.255, None), "LiF": (4.062, None)}
RPA_PAW = {"Si": (5.432, 99), "C": (3.572, 441), "SiC": (4.365, 223), "BN": (3.621, 378), "MgO": (4.225, 168),
           "LiF": (3.998, 76)}
RPA_NCPAW = {"Si": (5.428, None), "C": (3.562, None), "SiC": (4.353, None), "MgO": (4.200, None), "LiF": (3.994, None)}
RPA_STDPAW = {"Si": (5.438, None), "C": (3.571, None), "SiC": (4.367, None), "MgO": (4.217, None), "LiF": (3.993, None)}
RPA_ONCV = {"Si": (5.414, None), "C": (3.567, None), "BN": (3.617, None), "MgO": (4.200, None), "LiF": (3.996, None)}


def cp2k_values():
    pbe, rpa = {"Si": (5.4615, 88.2)}, {}
    for line in open(f"{RES}/pbe_gthpbe_c_sic_bn_mgo_lif/fits.txt"):
        if not line.startswith("#"):
            mat, val = line.split("|")
            pbe[mat.strip()] = tuple(float(v) for v in val.split()[:2])
    for line in open(f"{RES}/eos_c_sic_bn_mgo_lif/fits.txt"):
        w = line.replace("|", " ").split()
        if w[:5][1:] == ["Q", "4", "18", "RPA"]:
            rpa[w[0]] = (float(w[5]), float(w[6]))
    for line in open(f"{RES}/si_gthhf_frozen_grid/fits_matrix.txt"):
        if line.startswith("Q 4 20"):
            w = line.split("|")[2].split()
            rpa["Si"] = (float(w[0]), float(w[1]))
    pbe = {s: pbe[KEY.get(s, s)] for s in SOLIDS}
    rpa = {s: rpa[KEY.get(s, s)] for s in SOLIDS}
    return pbe, rpa


def row(values, column, mark=None):
    """formatted entries of the six solids and the MAE with respect to experiment (number of solids if not six)"""
    fmt = "{:.3f}" if column == 0 else "{:.0f}"
    cells, errors = [], []
    for s in SOLIDS:
        v = values.get(s, (None, None))[column]
        if v is None:
            cells.append(None)
        else:
            cells.append(fmt.format(v) + (mark if mark and s == "LiF" else ""))
            errors.append(abs(v - EXP[s][column]))
    mae = sum(errors) / len(errors) if errors else None
    return cells, mae, len(errors)


def tables():
    pbe, rpa = cp2k_values()
    star = "*"
    pbe_rows = (("CP2K, GTH-PBE, cc-pVQZ", pbe, None), ("all-electron (WIEN2k)", PBE_AE, None),
                ("plane waves, PAW", PBE_PAW, None), ("plane waves, ONCV", PBE_ONCV, None))
    rpa_rows = (("CP2K, GTH-HF, cc-pVQZ", rpa, star), ("plane waves, PAW", RPA_PAW, None),
                ("plane waves, norm-conserving PAW", RPA_NCPAW, None), ("plane waves, standard PAW", RPA_STDPAW, None),
                ("plane waves, ONCV", RPA_ONCV, None))
    out = []
    for method, rows in (("PBE", pbe_rows), ("RPA", rpa_rows)):
        for column, quantity in ((0, "lattice constant"), (1, "bulk modulus")):
            lines = []
            for label, values, mark in rows:
                cells, mae, n = row(values, column, mark)
                if n:
                    lines.append((label, cells, mae, n))
            lines.append(("experiment", row(EXP, column)[0], None, 6))
            out.append((method, quantity, column, lines))
    return out


def write_tex(all_tables, captions):
    with open(f"{HERE}/tables.tex", "w") as f:
        for (method, quantity, column, lines), (label, caption) in zip(all_tables, captions):
            f.write("\\begin{table}[tb]\n\\centering\\small\n\\caption{" + caption + "}\n\\label{" + label + "}\n")
            f.write("\\begin{tabular}{lccccccc}\n\\toprule\n & " + " & ".join(SOLIDS) + " & MAE\\\\\n\\midrule\n")
            for i, (name, cells, mae, n) in enumerate(lines):
                if name == "experiment" or i == 1:
                    f.write("\\midrule\n")
                cells = ["--" if c is None else c.replace("*", "$^*$") for c in cells]
                if mae is None:
                    m = ""
                else:
                    m = (f"{1000 * mae:.0f}~m\\AA" if column == 0 else f"{mae:.0f}") + (f"\\ ({n})" if n < 6 else "")
                f.write(f"{name} & " + " & ".join(cells) + f" & {m}\\\\\n")
            f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n\n")


def write_markdown(all_tables):
    with open(f"{HERE}/tables.md", "w") as f:
        for method, quantity, column, lines in all_tables:
            unit = "Å" if column == 0 else "GPa"
            f.write(f"{method} {quantity} ({unit}); MAE = mean absolute error with respect to experiment"
                    + (" (mÅ)" if column == 0 else "") + ":\n\n")
            f.write("| | " + " | ".join(SOLIDS) + " | MAE |\n|---|" + "---|" * 7 + "\n")
            for i, (name, cells, mae, n) in enumerate(lines):
                bold = "**" if i == 0 else ""
                cells = ["–" if c is None else bold + c.replace("*", "") + bold + ("\\*" if "*" in c else "") for c in cells]
                m = "" if mae is None else bold + (f"{1000 * mae:.0f}" if column == 0 else f"{mae:.0f}") + bold + (f" ({n})" if n < 6 else "")
                f.write(f"| {bold}{name}{bold} | " + " | ".join(cells) + f" | {m} |\n")
            f.write("\n")


if __name__ == "__main__":
    captions = (("tab:pbe_a0", "PBE lattice constant $a_0$ (\\AA). MAE: mean absolute error with respect to experiment; "
                 "a number in parentheses is the number of solids if not all six are available."),
                ("tab:pbe_b0", "PBE bulk modulus $B_0$ (GPa)."),
                ("tab:rpa_a0", "RPA lattice constant $a_0$ (\\AA). $^*$Fit to seven lattice constants "
                 "(3.94--4.18~\\AA); the calculations at 3.86 and 3.90~\\AA\\ were not finished."),
                ("tab:rpa_b0", "RPA bulk modulus $B_0$ (GPa)."))
    all_tables = tables()
    write_tex(all_tables, captions)
    write_markdown(all_tables)
