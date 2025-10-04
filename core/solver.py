import physics


eqVars_dict = {
    "specificGasContent"    :   frozenset({"R", "M"}),                                              #Specific Gas Constant
    "temperatureRatio"      :   frozenset({"Ma", "T", "T_s", "gamma"}),                             #Isentropic Temperature Ratio
    "pressureRatio"         :   frozenset({"Ma", "P", "P_s", "gamma"}),                             #Isentropic Pressure Ratio
    "areaMachRelation"      :   frozenset({"A_x", "A_y", "Ma_x", "Ma_y", "gamma"}),                 #Area-Mach Relation
    "exitVelocity"          :   frozenset({"P_e", "P_s", "T_s", "v_e", "gamma", "R"}),              #Isentropic Exit Velocity
    "massFlow"              :   frozenset({"A_t", "mdot", "P_e", "P_s", "T_s", "gamma", "R"}),      #Choked Mass Flow
    "thrust"                :   frozenset({"A_e", "F", "mdot", "P_a", "P_e", "v_e"}),               #Thrust
}


def reciever(inputVars, derivedVars):
    running = True

    while running:
        running = False
        for equation_id, equationVars in eqVars_dict.items():
            for subequationVars in equationVars:
                unknownVars = subequationVars - list(inputVars.keys) - list(derivedVars.keys)
                knownVars = subequationVars - unknownVars
                if len(unknownVars) == 1:
                    physicsSolver(equation_id, knownVars)
                    running = True


def physicsSolver(equation_id, knownVars):
    equation = getattr(physics, equation_id)
    result = equation(knownVars)
    return result