from scipy.optimize import fsolve

import physics


#Equation var sets
eqVars_dict = {
    "specificGasConstant"       :   frozenset({"M", "R"}),                                              #Specific Gas Constant
    "temperatureRatio@Throat"   :   frozenset({"Ma_t", "T_t", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Throat
    "temperatureRatio@Exit"     :   frozenset({"Ma_e", "T_e", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Exit
    "pressureRatio@Throat"      :   frozenset({"Ma_t", "P_t", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Throat
    "pressureRatio@Exit"        :   frozenset({"Ma_e", "P_e", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Exit
    "areaMachRelation"          :   frozenset({"A_t", "A_e", "Ma_t", "Ma_e", "gamma"}),                 #Area-Mach Relation
    "exitVelocity"              :   frozenset({"P_e", "P_s", "T_s", "v_e", "R", "gamma"}),              #Isentropic Exit Velocity
    "massFlow"                  :   frozenset({"A_t", "mdot", "P_s", "T_s", "R", "gamma"}),             #Choked Mass Flow
    "thrust"                    :   frozenset({"A_e", "F", "mdot", "P_a", "P_e", "v_e"}),               #Thrust
}

#Var initial guesses
guess_dict = {
    "fddf0"     :   15
}

#Var aliases
varAlias_dict = {
    "Ma"    :   ["Ma_t", "Ma_e"],
    "P"     :   ["P_t", "P_e"],
    "T"     :   ["T_t", "T_e"],
}

#Eq's to be normalized
eqID_normalize = {
    "temperatureRatio@Throat", 
    "temperatureRatio@Exit",
    "pressureRatio@Throat",
    "pressureRatio@Exit",
}


#---------------------------------------------
# Iterative Solver
#---------------------------------------------
def equationSolver(inputVars, derivedVars):
    '''
    Solves equations
    '''
    running = True

    while running:
        running = False

        for eqID, eqVars in eqVars_dict.items():
            #Merge all known vars into a single list
            knownVars = {}
            knownVars.update({k: v for k, v in inputVars.items() if v is not None})
            knownVars.update({k: v for k, v in derivedVars.items() if v is not None})

            #Find the unknown vars for this equation
            eqVars_unknown = eqVars - knownVars.keys()

            #Make dict of vars used by equation
            usedVars = {var: knownVars.get(var, None) for var in eqVars}

            if len(eqVars_unknown) == 1:
                unknown = list(eqVars_unknown)[0]
                function = getattr(physics, eqID.split("@")[0])

                usedVars = varNormalizer(eqID, usedVars)

                #fsolve intermediary
                def equationRunner(guess):
                    usedVars_temp = usedVars.copy()
                    usedVars_temp[unknown] = float(guess)
                    return function(**usedVars_temp)
                
                guess = guess_dict.get(unknown, 1.0)
                
                result = fsolve(equationRunner, guess)

                return result


#---------------------------------------------
# Variable Normalizer
#---------------------------------------------
def varNormalizer(eqID, usedVars):
    """
    Normalizes Variable Names
    """

    if eqID in eqID_normalize:
        for generic, aliases in varAlias_dict.items():
            for alt in aliases:
                if alt in usedVars:
                    usedVars[generic] = usedVars.pop(alt)
    
    return usedVars


#Testing Stuff
inputVars = {
    "Ma_e": 5,
    "gamma": 1.3,
    "T_e": 1500,
}

derivedVars = {
}

result = equationSolver(inputVars, derivedVars)
print("Final results:", result)