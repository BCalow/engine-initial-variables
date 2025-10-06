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
# Iterative Solver
#---------------------------------------------
def equationSolver(inputVars, derivedVars):

    while running:
        running = False

        for eqID, eqVars in eqVars_dict:
            #Merge all known vars into a single list
            knownVars = inputVars.copy()
            knownVars.update(derivedVars)

            #Find the unknown vars for this equation
            eqVars_unknown = eqVars - knownVars.keys()

            #Make dict of vars used by equation
            usedVars = {var: knownVars.get(var, None) for var in eqVars}

            if len(eqVars_unknown) == 1:
                unknown = list(eqVars_unknown)[0]
                function = getattr(physics, eqID.split("@")[0])

                running = True
    
    def 