"""Tables of pr_results_summary.tex: PBE and RPA lattice constants and bulk moduli of Si, C, SiC, BN, MgO, LiF
with the mean absolute error (MAE) with respect to experiment. Writes tables.tex and tables.md.

CP2K values: cc-pVQZ, k mesh 8x8x8; PBE with GTH-PBE, RPA with GTH-HF, RI 4, RS 18 (Si: RS 20).
The RPA tables have a second LiF column with an AE (all-electron) Li atom (0046, series liae); the MAE of the CP2K row
uses it, and the LiF value with Li GTH-HF-q3 is put in parentheses."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)
SOLIDS = ("Si", "C", "SiC", "BN", "MgO", "LiF")
LIF_LI_AE = "LiF ae"
LIF_LI_AE_NOTE = ("ae: Li all-electron (GAPW, def2-QZVP basis without its two most diffuse primitives) instead of "
                  "Li GTH-HF-q3.")
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
RPA_GPAW = {"Si": (None, 95), "C": (None, 435), "SiC": (None, 220), "MgO": (None, 163), "LiF": (None, 71)}
RPA_STDPAW = {"Si": (5.438, None), "C": (3.571, None), "SiC": (4.367, None), "MgO": (4.217, None), "LiF": (3.993, None)}
REFERENCES = ("Tran2011", "Bosoni2024", "Pitts2025", "Harl2010", "Humer2026", "Klimes2015", "Patrick2015")  # numbering in tables.md
RPA_ONCV = {"Si": (5.414, None), "C": (3.567, None), "BN": (3.617, None), "MgO": (4.200, None), "LiF": (3.996, None)}


def cp2k_values():
    pbe, rpa = {"Si": (5.4615, 88.2)}, {}
    for line in open(f"{RES}/0045_pbe_gthpbe_c_sic_bn_mgo_lif/fits.txt"):
        if not line.startswith("#"):
            mat, val = line.split("|")
            pbe[mat.strip()] = tuple(float(v) for v in val.split()[:2])
    for line in open(f"{RES}/0041_eos_gthhf_c_sic_bn_mgo_lif/fits.txt"):
        w = line.replace("|", " ").split()
        if w[:5][1:] == ["Q", "4", "18", "RPA"]:
            rpa[w[0]] = (float(w[5]), float(w[6]))
    for line in open(f"{RES}/0041_si_gthhf_frozen_grid/fits_matrix.txt"):
        if line.startswith("Q 4 20"):
            w = line.split("|")[2].split()
            rpa["Si"] = (float(w[0]), float(w[1]))
    pbe = {s: pbe[KEY.get(s, s)] for s in SOLIDS}
    rpa = {s: rpa[KEY.get(s, s)] for s in SOLIDS}
    for line in open(f"{RES}/0046_lif_bulk_modulus/fits_tests.txt"):
        if line.startswith("liae"):
            w = line.split("|")[3].split()
            rpa[LIF_LI_AE] = (float(w[0]), float(w[1]))
    return pbe, rpa


def row(values, column, second_lif_column=False):
    """formatted entries of the six solids and the MAE with respect to experiment over the available solids;
    second_lif_column: one more cell for LiF with all-electron Li, which replaces LiF in the MAE where it exists"""
    fmt = "{:.3f}" if column == 0 else "{:.0f}"
    cells, errors = [], []
    for s in SOLIDS:
        v = values.get(s, (None, None))[column]
        replaced = s == "LiF" and LIF_LI_AE in values
        cells.append(None if v is None else ("(" + fmt.format(v) + ")" if replaced else fmt.format(v)))
        if replaced:
            v = values[LIF_LI_AE][column]
        if v is not None:
            errors.append(abs(v - EXP[s][column]))
    if second_lif_column:
        cells.append(fmt.format(values[LIF_LI_AE][column]) if LIF_LI_AE in values else None)
    return cells, (sum(errors) / len(errors) if errors else None)


def tables():
    pbe, rpa = cp2k_values()
    # (row label, values, citation keys); REFERENCES gives the reference numbers of the markdown tables
    pbe_rows = (("CP2K, GTH-PBE, cc-pVQZ", pbe, ()), ("all-electron (WIEN2k)", PBE_AE, ("Tran2011", "Bosoni2024")),
                ("plane waves, PAW", PBE_PAW, ("Tran2011",)), ("plane waves, ONCV", PBE_ONCV, ("Pitts2025",)))
    rpa_rows = (("CP2K, GTH-HF, cc-pVQZ", rpa, ()), ("plane waves, PAW", RPA_PAW, ("Harl2010", "Humer2026")),
                ("plane waves, norm-cons. PAW", RPA_NCPAW, ("Klimes2015",)),
                ("plane waves, standard PAW", RPA_STDPAW, ("Klimes2015",)), ("plane waves, ONCV", RPA_ONCV, ("Pitts2025",)),
                ("plane waves, PAW (GPAW)", RPA_GPAW, ("Patrick2015",)))
    out = []
    for method, rows in (("PBE", pbe_rows), ("RPA", rpa_rows)):
        for column, quantity in ((0, "lattice constant"), (1, "bulk modulus")):
            lines = []
            for label, values, keys in rows:
                cells, mae = row(values, column, method == "RPA")
                if mae is not None:
                    lines.append((label, cells, mae, keys))
            lines.append(("experiment", row(EXP, column, method == "RPA")[0], None, ("Tran2011", "Harl2010")))
            out.append((method, quantity, column, lines))
    return out


def write_tex(all_tables, captions):
    with open(f"{HERE}/tables.tex", "w") as f:
        for (method, quantity, column, lines), (label, caption) in zip(all_tables, captions):
            f.write("\\begin{table}[!htb]\n\\centering\\small\n\\caption{" + caption + "}\n\\label{" + label + "}\n")
            columns = SOLIDS + (("LiF ae$^*$",) if method == "RPA" else ())
            f.write("\\begin{tabular}{l" + "c" * (len(columns) + 1) + "}\n\\toprule\n & " + " & ".join(columns)
                    + " & MAE\\\\\n\\midrule\n")
            for i, (name, cells, mae, keys) in enumerate(lines):
                if name == "experiment" or i == 1:
                    f.write("\\midrule\n")
                cells = ["--" if c is None else c for c in cells]
                m = "" if mae is None else (f"{1000 * mae:.0f}" if column == 0 else f"{mae:.0f}")
                cite = "~\\cite{" + ",".join(keys) + "}" if keys else ""
                f.write(f"{name}{cite} & " + " & ".join(cells) + f" & {m}\\\\\n")
            f.write("\\bottomrule\n\\end{tabular}\n")
            if method == "RPA" and column == 1:  # the note stands once, below the bulk modulus table
                f.write("\\\\[2pt]\\parbox{\\textwidth}{\\footnotesize $^*$ " + LIF_LI_AE_NOTE + "}\n")
            f.write("\\end{table}\n\n")


def write_markdown(all_tables):
    with open(f"{HERE}/tables.md", "w") as f:
        for method, quantity, column, lines in all_tables:
            f.write(f"**{method} {quantity} ({'Å' if column == 0 else 'GPa'})**, MAE vs. experiment"
                    + (" in mÅ" if column == 0 else "") + "\n\n")
            columns = SOLIDS + ((LIF_LI_AE + "*",) if method == "RPA" else ())
            f.write("| | " + " | ".join(columns) + " | MAE |\n|---|" + "---|" * (len(columns) + 1) + "\n")
            for i, (name, cells, mae, keys) in enumerate(lines):
                bold = "**" if i == 0 else ""
                cells = ["–" if c is None else bold + c + bold for c in cells]
                m = "" if mae is None else bold + (f"{1000 * mae:.0f}" if column == 0 else f"{mae:.0f}") + bold
                cite = " [" + ", ".join(str(REFERENCES.index(k) + 1) for k in keys) + "]" if keys else ""
                f.write(f"| {bold}{name}{bold}{cite} | " + " | ".join(cells) + f" | {m} |\n")
            f.write("\n")
            if method == "RPA":
                f.write("\\* " + LIF_LI_AE_NOTE + "\n\n")


if __name__ == "__main__":
    captions = (("tab:pbe_a0", "PBE lattice constant $a_0$ (\\AA) and its mean absolute error (MAE, in m\\AA) with "
                 "respect to experiment."),
                ("tab:pbe_b0", "PBE bulk modulus $B_0$ (GPa) and its MAE with respect to experiment."),
                ("tab:rpa_a0", "RPA lattice constant $a_0$ (\\AA) and its MAE (m\\AA) with respect to experiment."),
                ("tab:rpa_b0", "RPA bulk modulus $B_0$ (GPa) and its MAE with respect to experiment."))
    all_tables = tables()
    write_tex(all_tables, captions)
    write_markdown(all_tables)
