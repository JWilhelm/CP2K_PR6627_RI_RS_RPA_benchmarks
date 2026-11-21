# Benchmark calculations for CP2K PR #6627 (periodic RI-RS with k-points)

This repository holds the CP2K inputs and outputs behind the test results of the pull request
[cp2k/cp2k#6627](https://github.com/cp2k/cp2k/pull/6627)
("Periodic RI-RS: RPA and exact exchange with k-points, analytic d_lP, all-electron GW"):

1. RPA correlation energy and exact-exchange energy of crystals with full k-point sampling
   (new section `DFT%XC%WF_CORRELATION%RI_RS_RPA`),
2. the analytic three-centre projection d_lP as an alternative to the quadrature on a real-space mesh,
   chosen automatically,
3. all-electron G0W0 band structures with periodic RI-RS and tabulated RI-RS grids.

The results are summarised, with all definitions and references, in
[`pr_results_summary.pdf`](pr_results_summary.pdf) (8 pages). The figures of this PDF are drawn by
[`summary_figures/plot_report.py`](summary_figures/plot_report.py) from the fit and data files in
`summary_figures/data/` (Python with numpy and matplotlib; run it in `summary_figures/`).

## Code version

The calculations were run on the Noctua 2 cluster (Paderborn) with several successive development builds
of the code of this pull request, not with one fixed commit:

- All RPA, exact-exchange and d_lP runs: development builds on top of CP2K master `017ac7245`
  (this revision is printed in every output as "source code revision number"), with the uncommitted
  changes of the pull request at the time of the run.
- All-electron G0W0 runs: a development source tree without revision information (the outputs print
  "unknown").

The pull request branch is `ri-rs-rpa-dlp-ae` of [JWilhelm/cp2k](https://github.com/JWilhelm/cp2k/tree/ri-rs-rpa-dlp-ae).
Small differences between a rerun with the final code and the numbers stored here are therefore possible.
Folders named `..._rerun1`, `..._rerun2`, ... contain the same input run again with a later development build.

## Caveat: numerical noise of RPA energies

RPA total energies from this code are not smooth functions of the geometry. When the lattice constant a is
changed, E(a) scatters around a smooth curve, almost entirely through the exact-exchange energy E^EXX, because
the RI-RS grid is optimised separately at every geometry and the optimisation ends in a different local minimum
each time. With GTH pseudopotentials the scatter is 0.3–0.9 meV per cell, which is harmless for the lattice
constant but shifts the bulk modulus of Si by up to ±5 GPa; with all-electron basis sets it is 26–91 meV,
which makes all-electron RPA equations of state unusable. See Secs. 3.2, 3.5 and 6 of the PDF.

## Where the data of each figure and table are

| PDF | Content | Folder |
|---|---|---|
| Tables 1–3, Si column | Si PBE and RPA with GTH-HF, cc-pVQZ, RI 4 / RS 20, grid optimised at every a | `si_equation_of_state_gth/rpa_gth-hf_grid_optimised_at_every_a/Si_GTH-HF_cc-pVQZ-GTH-HF-q4_k8x8x8_RI4_RS20` |
| Tables 1–3, other columns | C, SiC, BN, MgO, LiF with GTH-HF, cc-pVQZ, RI 4 / RS 18 | `c_sic_bn_mgo_lif_equation_of_state_gth-hf/*_cc-pVQZ-*_RI4_RS18` |
| Sec. 3.1, text | Si PBE all-electron (pc-4) and GTH-PBE; Si RPA with GTH-PBE | `si_equation_of_state_gth/pbe_only/`, `si_equation_of_state_gth/rpa_gth-pbe/` |
| Fig. 1 | Si GTH-HF, PBE and RPA total energy vs a (cc-pVTZ, cc-pVQZ, RI 4 / RS 14) | `si_equation_of_state_gth/rpa_gth-hf_grid_optimised_at_every_a/Si_GTH-HF_cc-pV{T,Q}Z-GTH-HF-q4_k8x8x8_RI4_RS14` |
| Fig. 2(a, c) | Si GTH-HF, grid optimised at every a | `si_equation_of_state_gth/rpa_gth-hf_grid_optimised_at_every_a/` |
| Fig. 2(b, d) | Si GTH-HF, grid optimised once at a = 5.41 Å and frozen | `si_equation_of_state_gth/rpa_gth-hf_frozen_grid/` |
| Sec. 3.3 | frozen grids of different size or from a different a | `si_equation_of_state_gth/rpa_gth-hf_frozen_grid_size_test/`, `si_equation_of_state_gth/rpa_gth-hf_frozen_grid_optimisation_runs/` |
| Sec. 6 | Si: k mesh, RI basis, cutoff, screening, time/frequency points, regularisation | `si_equation_of_state_gth/rpa_gth-pbe_cc-pVQZ_parameter_scan/`, `si_equation_of_state_gth/rpa_gth-pbe/` |
| Sec. 3.1 | pseudopotential dependence | `si_equation_of_state_gth/rpa_other_pseudopotentials/`, `si_equation_of_state_gth/pbe_only/` |
| Fig. 3, Sec. 3.4 | C, SiC, BN, MgO, LiF with GTH-HF (PBE and RPA from the same runs) | `c_sic_bn_mgo_lif_equation_of_state_gth-hf/` |
| Fig. 4, Sec. 3.5 | all-electron Si, cc-pVXZ-s | `si_allelectron_rpa_cc-pvxz-s/` (a, c: `*_tabulated_grid`; b, d: `*_grid_optimised_at_every_a`) |
| Fig. 5, Sec. 4 | d_lP timing, analytic vs quadrature, automatic choice | `dlp_analytic_vs_quadrature/` |
| Sec. 4, accuracy | Si DZVP-MOLOPT-SR, k 4x4x4; all-electron Si and C with pc-2 | `dlp_analytic_vs_quadrature/Si_DZVP-MOLOPT-SR-GTH_k4x4x4/`, `dlp_analytic_vs_quadrature/{Si,C}_all-electron_pc-2_k4x4x4/` |
| Fig. 6, Sec. 5 | all-electron G0W0 gaps of diamond and silicon | `allelectron_gw_diamond_silicon/` |
| all figures | plotting script and the fit/data files it reads | `summary_figures/` |

The plane-wave, FHI-aims, VASP, WIEN2k and experimental reference values are taken from the literature
cited in the PDF; they are not computed here.

## Folder and file naming

Equation-of-state series (`si_*`, `c_sic_bn_mgo_lif_*`) are stored as one folder per series:

```
<crystal>_<pseudopotential family or all-electron>_<AO basis>_k<NxNxN>_RI<RI_AO_RATIO>_RS<RS_AO_RATIO>[_<variant>]/
    a<lattice constant in Å>.inp       CP2K input
    a<lattice constant in Å>.out.gz    CP2K output (gzip, unchanged otherwise)
```

- `<AO basis>`: the `BASIS_SET` name of the input; for two elements the two names are joined by `+`.
  The Si GTH-PBE series use the cc-pVXZ-GTH-HF basis sets together with the GTH-PBE pseudopotential.
- `RI<x>`: `RI_AO_RATIO` of `&AUTO_RI` (RI functions per AO function); missing when the RI basis is
  tabulated (all-electron cc-pVXZ-s with cc-pVXZ-s-FIT).
- `RS<y>`: `RS_AO_RATIO` of `&GRID_OPTIMIZATION` (RI-RS grid points per AO function); missing when a
  tabulated grid is used.
- `<variant>`: the setting that differs from the other series, e.g. `CUTOFF800`, `EPS_PGF_ORB1e-24`,
  `NUM_TIME_FREQ_POINTS26`, `REGULARIZATION_RI1e-2`, `TIKHONOV1e-8`, `grid_frozen_from_a5.41`,
  `canonical_orthogonalisation`.
- Every primitive fcc cell has two atoms; all energies in the outputs are per cell.

d_lP tests (`dlp_analytic_vs_quadrature/`) use one folder per crystal, basis and k mesh, and inside one folder
per run: `analytic`, `quadrature`, `automatic` (the code chooses), `automatic_choice_only` (the run stops after
the choice is printed), `..._no_space_group` (space-group symmetry switched off), `..._<N>nodes`.
The method was forced for these tests with a development switch that is not part of the pull request.
The runs with k 4x4x4 (Si DZVP-MOLOPT-SR, all-electron Si and C) are complete RPA calculations. All other runs
were stopped as soon as d_lP was complete, so these outputs end there; the d_lP time is the line
`d_lP completed ... Exec. time` of the output. The forced analytic run of TiO2 anatase with aug-DZVP ran out of
memory (Sec. 4 of the PDF); its output ends with the last progress line.

G0W0 runs (`allelectron_gw_diamond_silicon/`) use one folder per run:
`<crystal>_<AO basis>_k12x12x12_RI<number of RI functions per atom>[_<variant>]` with `input.inp`,
`output.out.gz` and the band-structure files written by CP2K (`bandstructure_DFT.gz`,
`bandstructure_SCF_and_G0W0.gz`). `_quadrature_dlp` marks the runs with the quadrature; all others use the
analytic d_lP. The numbers of RI functions per atom are the labels on the axis of Fig. 6.

## Files that are not shipped with CP2K

Basis-set and pseudopotential files that are not in `cp2k/data` are included next to the inputs that read them:
`BASIS_ccGTH_Si`, `BASIS_ccGTH` (cc-pVXZ for GTH pseudopotentials), `POTENTIAL_Si_GTH_PBE_HF`, `POTENTIAL_GTH_HF`
(GTH-HF pseudopotentials), `BASIS_ccpVXZs` (cc-pVXZ-s with cc-pVXZ-s-FIT), and `BASIS_RI_Si_big`,
`BASIS_RI_steep`, `BASIS_AO_core` in the G0W0 run folders. Inputs of the frozen-grid series read the basis and
pseudopotential files from `../../`, which is `si_equation_of_state_gth/`.

Some series read the RI-RS grid from files: inputs with `GRID_SELECT 3` and `MAX_ITER 1` (or `MAX_ITER 200`
as a starting grid) read `ri_rs_grid/atom_*_rirs.ion` in the run directory, as printed in the outputs
("RI-RS grid points read from ri_rs_grid/atom_*_rirs.ion"). These files are included in the series folders.
Reading a stored grid was a test feature of the development builds and is not part of the pull request.
For the all-electron `*_tabulated_grid` series the files hold the tabulated grid.

Some inputs contain absolute paths on the cluster. G0W0: extra basis files (included in the run folders) and,
for runs that start from an earlier SCF, the wavefunction restart file (not included). d_lP runs of AlAs and
GaAs with aug-TZVP: the pseudopotential files `POTENTIALS` / `POTENTIALS_SOC`, which are not included.

## What is not included

- Wavefunction restart files, CP2K binaries, Slurm scripts and Slurm logs, empty stdout/stderr files, the RI-RS
  grids written by the grid optimiser (`optimized_atom_*_rirs.ion`).
- LiF cc-pVQZ RI 4 / RS 18: the runs for a = 3.86 and 3.90 Å did not finish within the 4 h time limit and were
  restarted; only their inputs are included. As stated in the PDF, Fig. 3 uses RI 3 / RS 14 for LiF.
- Runs that are superseded or not used in the PDF: frozen-grid runs with a development build that ignored
  `RI_AO_RATIO` (they were repeated, see `rpa_gth-hf_frozen_grid/`; only the grid-size test in
  `rpa_gth-hf_frozen_grid_size_test/` is kept from that build, where the number of RI functions is therefore
  the same for all RS values), a repeated QZ parameter scan, earlier Si all-electron RPA attempts and
  reference runs, experimental variants of the analytic d_lP that are not in the pull request, earlier
  all-electron pc-2 d_lP runs, and G0W0 runs of diamond with aug-DZVP made with a development build that had a
  bug in the analytic d_lP (since fixed; the runs in this repository use the fixed code), together with the
  diagnostic runs for that bug and cancelled or aborted G0W0 runs.

## Outputs that did not finish

The outputs are included as they are. These series contain outputs without "PROGRAM ENDED":

| Folder | Finished / runs |
|---|---|
| `si_equation_of_state_gth/pbe_only/Si_all-electron_{QZVPP-MOLOPT-PBE-ae,aug-TZVP-MOLOPT-ae,aug-pc-2,aug-pc-3}_k8x8x8` | 0 / 9 each |
| `si_equation_of_state_gth/rpa_gth-pbe/Si_GTH-PBE_cc-pVQZ-GTH-HF-q4_*_EPS_PGF_ORB1e-14` | 5 / 9 each |
| `si_equation_of_state_gth/rpa_gth-pbe_cc-pVQZ_parameter_scan/Si_GTH-PBE_cc-pVQZ-GTH-HF-q4_k6x6x6_RI8_RS{14,30}` | 0 / 3 each |
| `si_equation_of_state_gth/rpa_gth-hf_frozen_grid_optimisation_runs/..._RI4_RS30_grid_optimisation` | 0 / 1 (the grid was written) |
| `si_equation_of_state_gth/rpa_gth-hf_frozen_grid_size_test/..._RI4_RS30_grid_frozen_from_a5.41` | 8 / 9 |
| `c_sic_bn_mgo_lif_equation_of_state_gth-hf/LiF_GTH-HF_cc-pVQZ-..._RI4_RS18` | 7 / 9 (2 not finished, see above) |
| `dlp_analytic_vs_quadrature/` (most runs) | stopped on purpose after d_lP, see above |
