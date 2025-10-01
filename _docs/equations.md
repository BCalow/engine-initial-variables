# Equations

This document summerizes the governing equations used in the solver.
All equations are written in residual form in the code, but are written here with their possible rearrangements for clarity.

## Thermodynamic Relations

**Specific Gas Constant** 

$$
R = \frac{R'}{M}
$$


**Speed of Sound**

$$
c = \sqrt{\gamma R T}
$$


**Isentropic Temperature-Pressure Relation**

$$
\frac{T_x}{T_y} = \left(\frac{P_x}{P_y}\right) ^ {\left(\frac{\gamma}{\gamma - 1}\right)}
$$


**Isentropic Temperature Ratio**

$$
\frac{T}{T_0} = \left[1 + \frac{1}{2} \left(\gamma - 1\right) Ma ^ 2\right]^{-1}
$$


**Isentropic Pressure Ratio**

$$
\frac{P}{P_0} = \left[1 + \frac{1}{2} \left(\gamma - 1\right) Ma ^ 2\right] ^ {-\frac{\gamma}{\gamma - 1}}
$$


**Area-Mach Relation**

$$
\frac{A_y}{A_x} = \frac{Ma_x}{Ma_y} \sqrt{\left\{\frac{1 + \left[\frac{\gamma - 1}{2}\right] Ma_y ^ 2}{1 + \left[\frac{\gamma - 1}{2}\right] Ma_x ^ 2}\right\} ^ {\frac{\gamma + 1}{\gamma - 1}}}
$$


## Isentropic Flow

**Isentropic Exit Velocity**

$$
v_e = \sqrt{\frac{2 \gamma}{\gamma - 1} R T_0 \left[1 - \left(\frac{P_e}{P_0}\right) ^ {\frac{\gamma - 1}{\gamma}}\right]}
$$


**Choked Mass Flow**

$$
\dot{m} = A_t P_0 \sqrt{\frac{\gamma}{R T_0}}\left(\frac{2}{\gamma + 1}\right)^{\tfrac{\gamma + 1}{2(\gamma - 1)}}
$$


**Thrust**

$$
F = \dot{m} v_e + \left(P_e - P_a\right) A_e
$$