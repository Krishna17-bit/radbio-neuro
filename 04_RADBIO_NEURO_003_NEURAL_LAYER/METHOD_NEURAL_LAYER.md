# Neural model notes

Effective membrane dynamics are simulated as a compact leaky integrate-and-fire population:

\[
\frac{dV_i}{dt} = \frac{1}{\tau_\mathrm{eff}}\left(E_L - V_i + D_\mathrm{eff}\right) + \eta_i(t)
\]

where the RADBIO_NEURO_002 biology layer controls:

\[
\tau_\mathrm{eff} = \frac{\tau_m}{1 + k_L(1-ATP)}
\]

\[
V_{th,eff} = V_{th,0} + \Delta V_{th}(1-ATP)
\]

\[
D_\mathrm{eff} = D_0(0.08 + 0.92ATP) + g_{ROS}\Delta E_{fast}
\]

Interpretation:

- acute ROS can add a fast drive term through channel/redox effects,
- mitochondrial injury and ATP loss dominate slow suppression,
- ATP collapse cannot be fully rescued by acute ROS drive.

This model is intentionally conservative and modular so it can be replaced by a full Brian2 or NEURON Hodgkin-Huxley/AdEx implementation in the next iteration.
