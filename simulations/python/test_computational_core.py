import numpy as np
from computational_core import ClinicalStressTestEngine

def test_generate_patient_parameters():
    engine = ClinicalStressTestEngine()
    params = engine.generate_patient_parameters()

    assert "D_cort" in params
    assert "k_cort_burst" in params
    assert "initial_B_cort" in params
    assert "D_peg" in params
    assert "D_pvp" in params
    assert "initial_peg" in params
    assert "initial_pvp" in params

    assert params["D_cort"] > 0
    assert params["k_cort_burst"] > 0
    assert params["initial_B_cort"] > 0
    assert params["D_peg"] > 0
    assert params["D_pvp"] > 0
    assert params["initial_peg"] > 0
    assert params["initial_pvp"] > 0

def test_pde_system_stochastic():
    engine = ClinicalStressTestEngine()
    p = engine.generate_patient_parameters()

    # Create a mock initial state vector
    N = engine.N
    y = np.ones(8 * N)

    t = 0.0
    dy = engine.pde_system_stochastic(t, y, p)

    assert len(dy) == 8 * N

    dC_ibu  = dy[0:N]
    dC_egcg = dy[N:2*N]
    dC_syn  = dy[2*N:3*N]
    dH_gel  = dy[3*N:4*N]
    dC_cort = dy[4*N:5*N]
    dB_cort = dy[5*N:6*N]
    dC_peg  = dy[6*N:7*N]
    dC_pvp  = dy[7*N:8*N]

    # Assert boundaries (Zero flux on left boundary)
    assert dC_ibu[0] == dC_ibu[1]
    assert dC_egcg[0] == dC_egcg[1]
    assert dH_gel[0] == dH_gel[1]
    assert dC_syn[0] == dC_syn[1]
    assert dC_cort[0] == dC_cort[1]
    assert dC_peg[0] == dC_peg[1]
    assert dC_pvp[0] == dC_pvp[1]

    # Cortisone depletion
    # Assuming in_gel area is on the left
    # Boundary is handled differently, so check an inner node within gel
    assert dB_cort[1] < 0

def test_run_stress_trial():
    engine = ClinicalStressTestEngine()
    res = engine.run_stress_trial(trial_id=1, time_days=1)

    assert "trial_id" in res
    assert "params" in res
    assert "pathogen_at_boundary" in res
    assert "reduction_pct" in res
    assert "failed" in res
    assert "final_profile" in res

    assert len(res["final_profile"]) == engine.N
