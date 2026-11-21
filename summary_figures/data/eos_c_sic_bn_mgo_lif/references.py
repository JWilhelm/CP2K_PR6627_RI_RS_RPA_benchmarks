# Reference values (a0 in Å, B0 in GPa); None = not available. Papers in analysis/literature_eos/ (README.txt).
# PBE AE: WIEN2k, Tran & Blaha, PRB 83, 235118 (2011), Table III; MgO (not there): ACWF WIEN2k set,
#   Bosoni et al., Nat. Rev. Phys. 6, 45 (2024), BM fit of ACWF_oxides_PBE_v1_WIEN2k_results.json.
# PBE / RPA ONCV: Pitts, Contant, Hellgren, PRB 112, 085137 (2025), Table II (a0 only; no SiC).
# RPA PAW: Harl, Schimka, Kresse, PRB 81, 115126 (2010) as quoted in Patrick & Thygesen, JCP 143, 102802 (2015),
#   Table I; BN (not in Harl): Humer, Schlipf, Kresse, arXiv:2602.14923 (2026), Tables VII/VIII.
# exp.: zero-point corrected a0 and B0, Tran & Blaha Table III (MgO a0 Pitts Table II, B0 165 GPa not ZPC).
REF = {
    "C":   {"PBE AE": (3.575, 435), "PBE ONCV": (3.567, None), "RPA ONCV": (3.567, None),
            "RPA PAW": (3.572, 441), "exp.": (3.553, 455)},
    "SiC": {"PBE AE": (4.384, 213), "RPA PAW": (4.365, 223), "exp.": (4.346, 229)},
    "BN":  {"PBE AE": (3.628, 374), "PBE ONCV": (3.621, None), "RPA ONCV": (3.617, None),
            "RPA PAW": (3.621, 378), "exp.": (3.592, 410)},
    "MgO": {"PBE AE": (4.254, 149.0), "PBE ONCV": (4.255, None), "RPA ONCV": (4.200, None),
            "RPA PAW": (4.225, 168), "exp.": (4.189, 165)},
    "LiF": {"PBE AE": (4.069, 67.2), "PBE ONCV": (4.062, None), "RPA ONCV": (3.996, None),
            "RPA PAW": (3.998, 76), "exp.": (3.972, 76.3)},
}
