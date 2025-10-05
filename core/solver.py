from scipy.optimize import fsolve

import physics


#Equation variable sets
eqVars_dict = {
    "specificGasContent"        :   frozenset({"M", "R"}),                                              #Specific Gas Constant
    "temperatureRatio@Throat"   :   frozenset({"Ma_t", "T_t", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Throat
    "temperatureRatio@Exit"     :   frozenset({"Ma_e", "T_e", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Exit
    "pressureRatio@Throat"      :   frozenset({"Ma_t", "P_t", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Throat
    "pressureRatio@Exit"        :   frozenset({"Ma_e", "P_e", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Exit
    "areaMachRelation"          :   frozenset({"A_t", "A_e", "Ma_t", "Ma_e", "gamma"}),                 #Area-Mach Relation
    "exitVelocity"              :   frozenset({"P_e", "P_s", "T_s", "v_e", "R", "gamma"}),              #Isentropic Exit Velocity
    "massFlow"                  :   frozenset({"A_t", "mdot", "P_s", "T_s", "R", "gamma"}),             #Choked Mass Flow
    "thrust"                    :   frozenset({"A_e", "F", "mdot", "P_a", "P_e", "v_e"}),               #Thrust
}


#---------------------------------------------
# Initial Guess 
#---------------------------------------------



#---------------------------------------------
# Iterative Solver
#---------------------------------------------
def solver(inputVars, derivedVars):
    running = True

    while running:
        running = False
        for equation_id, equationVars in eqVars_dict.items():
            unknownVars = equationVars - list(inputVars.keys()) - list(derivedVars.keys)
            knownVars = equationVars - unknownVars
            if len(unknownVars) == 1:
                result = physicsSolver(equation_id, knownVars)
                derivedVars.update({unknownVars: result})
                running = True
    
    return derivedVars

"""
#Equation solver
def physicsSolver(equation_id, equationVars):
    equation_id = equation_id.split("@")[0]
    equation = getattr(physics, equation_id)
    result = fsolve(equation, equationVars, guess=)
    return result
"""