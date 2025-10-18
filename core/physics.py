import numpy

#Constants
gravity     =   9.80665             #Standard Gravity           [m/s^2]
R_universal =   8.31446261815324    #Universal Gas Constant     [J⋅K^−1⋅mol^−1]

def specificGasConstant(M, R):
    """
    Specific Gas Constant
    M   :   Molar Mass
    R   :   Specific Gas Constant
    R'  :   Universal Gas Constant

    0 = R' / M - R
    """
    return (
        (R_universal / M) - R
    )

def temperatureRatio(Ma, T, T_s, gamma):
    """
    Isentropic Temperature Ratio

    Ma      :   Mach Number @ Point X
    T       :   Temperature @ Point X
    T_s     :   Stagnation Temperature
    gamma   :   Ratio Of Specific Heats

    0 = T / T_s - [1 + 1/2 * (gamma - 1) * Ma ^ 2]
    """
    return (
        T / T_s - (1 + 0.5 * (gamma - 1) * Ma ** 2) ** (-1)
    )

def pressureRatio(Ma, P, P_s, gamma):
    """
    Isentropic Pressure Ratio

    Ma      :   Mach Number @ Point X
    P       :   Pressure @ Point X
    P_s     :   Stagnation Temperature
    gamma   :   Ratio Of Specific Heats

    0 = P / P_s - [1 + 1/2 * (gamma - 1) * Ma ^ 2] ^ (gamma / (gamma - 1))
    """

    return (
        P /P_s - (1 + 0.5 * (gamma - 1) * Ma ** 2) ** (-gamma / (gamma - 1))
    )

def areaMachRelation(A_t, A_e, Ma_t, Ma_e, gamma):
    """
    Area-Mach Relation

    A_t     :   Area @ Throat
    A_e     :   Area @ Exit
    Ma_t    :   Mach Number @ Throat
    Ma_e    :   Mach Number @ Exit
    gamma   :   Ratio Of Specific Heats

    0 = A_y / A_x - Ma_x / Ma_y * sqrt(((1 + (gamma - 1) / 2 * Ma_y ^ 2) / (1 + (gamma - 1) / 2 * Ma_x ^ 2)) ^ ((gamma + 1) / (gamma - 1)))
    """

    return (
        A_e / A_t - Ma_t / Ma_e * numpy.sqrt(((1 + (gamma - 1) / 2 * Ma_e ** 2) / (1 + (gamma - 1) / 2 * Ma_t ** 2)) ** ((gamma + 1) / (gamma - 1)))
    )

def exitVelocity(P_e, P_s, T_s, v_e, R, gamma):
    """
    Isentropic Exit Velocity

    P_e     :   Pressure @ Exit
    P_s     :   Stagnation Pressure
    T_s     :   Stagnation Temperature
    v_e     :   Velocity @ Exit
    gamma   :   Ratio Of Specific Heats
    R       :   Specific Gas Constant

    0 = v_e - sqrt((2 * gamma) / (gamma - 1) * R * T_s * (1 - (P_e / P_s) ** ((gamma - 1) / gamma)))
    """

    return(
        v_e - numpy.sqrt((2 * gamma) / (gamma - 1) * R * T_s * (1 - (P_e / P_s) ** ((gamma - 1) / gamma)))
    )

def massFlow(A_t, mdot, P_s, T_s, R, gamma):
    """
    Choked Mass Flow

    A_t     :   Area @ Throat    
    mdot    :   Mass Flow Rate
    P_e     :   Pressure @ Exit
    P_s     :   Stagnation Pressure
    T_s     :   Stangation Temperature
    gamma   :   Ratio Of Specific Heats
    R       :   Specific Gas Constant

    0 = mdot - A_t * P_s * sqrt(gamma / (R * T_s)) * (2 / (gamma + 1)) ^ ((gamma + 1) / (2 * (gamma - 1)))
    """

    return (
        mdot - A_t * P_s * numpy.sqrt(gamma / (R * T_s)) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1)))
    )

def thrust(A_e, F, mdot, P_a, P_e, v_e):
    """
    Thrust

    A_e     :   Area @ Exit
    F       :   Force
    mdot    :   Mass Flow Rate
    P_a     :   Pressure @ Ambient
    P_e     :   Pressure @ Exit
    v_e     :   Velocity @ Exit

    0 = F - mdot * v_e + (P_e - P_a) * A_e
    """

    return (
        F - (mdot * v_e + (P_e - P_a) * A_e)
    )

def temperatureEquivalence(T_c, T_s):
    """
    Temperature Equivalence

    T_c     :   Temperature @ Chamber
    T_s     :   Temperature @ Stagnation

    0 ≈ T_c - T_s
    """

    return (
        T_c - T_s
    )

def pressureEquivalence(P_c, P_s):
    """
    Pressure Equivalence

    P_c     :   Pressure @ Chamber
    P_s     :   Pressure @ Stagnation

    0 ≈ P_c - P_s
    """

    return (
        P_c - P_s
    )

def flowRelation(P, P_s, T, T_s, gamma):
    """
    Isentropic Flow Relation

    P       :   Pressure @ Point X
    P_s     :   Pressure @ Stagnation
    T       :   Temperature @ Point X
    T_s     :   Temperature @ Stagnation
    gamma   :   Ratio of Specific Heats
    """
    return (P / P_s) - ((T / T_s) ** (gamma / (gamma - 1)))