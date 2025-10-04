import numpy

#Constants
gravity     =   9.80665             #Standard Gravity           [m/s^2]
R_universal =   8.31446261815324    #Universal Gas Constant     [J⋅K^−1⋅mol^−1]

def specificGasConstant(R, M):
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

def temperatureRatio(T, T_s, Ma, gamma):
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

def pressureRatio(P, P_s, gamma, Ma):
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

def areaMachRelation(A_x, A_y, Ma_x, Ma_y, gamma):
    """
    Area-Mach Relation

    A_x     :   Area @ Point X
    A_y     :   Area @ Point Y
    Ma_x    :   Mach Number @ Point X
    Ma_y    :   Mach Number @ Point Y
    gamma   :   Ratio Of Specific Heats

    0 = A_y / A_x - Ma_x / Ma_y * sqrt(((1 + (gamma - 1) / 2 * Ma_y ^ 2) / (1 + (gamma - 1) / 2 * Ma_x ^ 2)) ^ ((gamma + 1) / (gamma - 1)))
    """

    return (
        A_y / A_x - Ma_x / Ma_y * numpy.sqrt(((1 + (gamma - 1) / 2 * Ma_y ** 2) / (1 + (gamma - 1) / 2 * Ma_x ** 2)) ** ((gamma + 1) / (gamma - 1)))
    )

def exitVelocity(v_e, T_s, P_e, P_s, R, gamma):
    """
    Isentropic Exit Velocity

    P_e     :   Pressure @ Exit
    P_s     :   Stagnation Pressure
    T_s     :   Stagnation Temperature
    v_e     :   Velocity @ Exit
    gamma   :   Ratio Of Specific Heats
    R       :   Specific Gas Constan

    0 = v_e - sqrt((2 * gamma) / (gamma - 1) * R * T_s * (1 - (P_e / P_s) ** ((gamma - 1) / gamma)))
    """

    return(
        v_e - numpy.sqrt((2 * gamma) / (gamma - 1) * R * T_s * (1 - (P_e / P_s) ** ((gamma - 1) / gamma)))
    )

def massFlow(mdot, A_t, P_s, gamma, R, T_s, P_e):
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

def thrust(F, mdot, v_e, P_e, P_a, A_e):
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