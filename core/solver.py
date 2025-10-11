from scipy.optimize import fsolve
import numpy as np
import inspect

import core.physics as physics


# Equation var sets
eqVars_dict = {
    "specificGasConstant"       :   frozenset({"M", "R"}),                                              #Specific Gas Constant
    "temperatureRatio@Chamber"  :   frozenset({"Ma_c", "T_c", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Chamber
    "temperatureRatio@Throat"   :   frozenset({"Ma_t", "T_t", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Throat
    "temperatureRatio@Exit"     :   frozenset({"Ma_e", "T_e", "T_s", "gamma"}),                         #Isentropic Temperature Ratio @ Exit
    "pressureRatio@Chamber"     :   frozenset({"Ma_c", "P_c", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Chamber
    "pressureRatio@Throat"      :   frozenset({"Ma_t", "P_t", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Throat
    "pressureRatio@Exit"        :   frozenset({"Ma_e", "P_e", "P_s", "gamma"}),                         #Isentropic Pressure Ratio @ Exit
    "areaMachRelation"          :   frozenset({"A_t", "A_e", "Ma_t", "Ma_e", "gamma"}),                 #Area-Mach Relation
    "exitVelocity"              :   frozenset({"P_e", "P_s", "T_s", "v_e", "R", "gamma"}),              #Isentropic Exit Velocity
    "massFlow"                  :   frozenset({"A_t", "mdot", "P_s", "T_s", "R", "gamma"}),             #Choked Mass Flow
    "thrust"                    :   frozenset({"A_e", "F", "mdot", "P_a", "P_e", "v_e"}),               #Thrust
}

# Constants
constantVars = {
    "Ma_c"      :   0,
    "Ma_t"      :   1,
}

# Var initial guesses
guess_dict = {
    "fddf0"     :   15
}

# Var aliases
varAlias_dict = {
    "Ma"    :   ["Ma_t", "Ma_e", "Ma_c"],
    "P"     :   ["P_t", "P_e", "P_c"],
    "T"     :   ["T_t", "T_e", "T_c"],
}

# Eq's to be normalized
eqID_normalize = {
    "temperatureRatio@Chamber",
    "temperatureRatio@Throat", 
    "temperatureRatio@Exit",
    "pressureRatio@Chamber",
    "pressureRatio@Throat",
    "pressureRatio@Exit",
}


#---------------------------------------------
# Iterative Solver
#---------------------------------------------
def equationSolver(inputVars:dict):
    '''
    Solves equations
    '''

    # Raises TypeError if inputVars or derivedVars are not a dict
    if not isinstance(inputVars, dict):
        raise TypeError("inputVars must be a dict")

    running = True
    derivedVars = {}

    # Protection against infinite loops
    iteration_count = 0
    max_iterations = 50
    tol_r, tol_a = 1e-6, 1e-9   # Relative and absolute tolerances

    while running and iteration_count <= max_iterations:
        running = False


        for eqID, eqVars in eqVars_dict.items():
            #Merge all known vars into a single dict
            knownVars = {
                **{k:v for k,v in inputVars.items() if v is not None},
                **{k:v for k,v in derivedVars.items() if v is not None},
                **{k:v for k,v in constantVars.items() if v is not None}}

            #Find the unknown vars for this equation
            eqVars_unknown = eqVars - knownVars.keys()

            #Make dict of vars used by equation
            usedVars = {var: knownVars.get(var, None) for var in eqVars}

            if len(eqVars_unknown) != 1:
                print(f"Skipping {eqID}: unknowns = {eqVars_unknown}")
                continue  

            if len(eqVars_unknown) == 1:
                unknown = list(eqVars_unknown)[0]
                function = getattr(physics, eqID.split("@")[0])

                usedVars = varNormalizer(eqID, usedVars)

                for generic, aliases in varAlias_dict.items():
                    if unknown in aliases:
                        unknown = generic
                        break

                if unknown in derivedVars:
                    continue

                #fsolve intermediary
                def equationRunner(guess):
                    usedVars_temp = usedVars.copy()
                    usedVars_temp[unknown] = float(np.asarray(guess).item())

                    valid_args = inspect.signature(function).parameters.keys()
                    args = {k: v for k, v in usedVars_temp.items() if k in valid_args}

                    return function(**args)
                
                guess = guess_dict.get(unknown, 1.0)
                
                result = fsolve(equationRunner, guess)[0]
                if eqID in eqID_normalize:
                    for generic, aliases in varAlias_dict.items():
                        if unknown == generic:
                            for alt in aliases:
                                if alt in eqVars_dict[eqID]:
                                    prev = derivedVars.get(alt)
                                    if prev is None or not np.isclose(prev, result, rtol=1e-6, atol=1e-9):
                                        derivedVars[alt] = result
                                        running = True
                
                else:
                    prev = derivedVars.get(unknown)
                    if prev is None or not np.isclose(prev, result, rtol=1e-6, atol=1e-9):
                        derivedVars[unknown] = result
                        running = True

                print("Running")

    return derivedVars


#---------------------------------------------
# Constraint Checker
#---------------------------------------------
def constraintChecker(inputVars:dict):
    '''Checks for constraints and finds derived vars'''

    # Raises typeError if inputVars is not a dict
    if not isinstance(inputVars, dict):
        raise TypeError("inputVars must be a dict")
    
    running = True
    derivedVars = {}

    # Protection against infinite loops
    iteration_count = 0
    max_iterations = 50

    while running and iteration_count <= max_iterations:
        running = False
        iteration_count += 1

        for eqID, eqVars in eqVars_dict.items():
            # Merge all selected/known vars into a single dict
            selectedVars = {
                **{k:v for k,v in inputVars.items()},
                **{k:v for k,v in derivedVars.items()},
                **{k:v for k,v in constantVars.items()}}

            #Find the unknown vars for this equation
            eqVars_unknown = eqVars - selectedVars.keys()

            if len(eqVars_unknown) != 1:
                continue

            if len(eqVars_unknown):
                unknown = next(iter(eqVars_unknown))
            
                derivedVars[unknown] = None
                running = True

    print("finished")
    return derivedVars





#---------------------------------------------
# Variable Normalizer
#---------------------------------------------
def varNormalizer(eqID, usedVars):
    """Normalizes variable names"""

    if eqID in eqID_normalize:
        replacements = {}
        for generic, aliases in varAlias_dict.items():
            for alt in aliases:
                if alt in usedVars:
                    replacements[alt] = generic
        # Apply replacements after the loop to avoid concurrent modification
        for alt, generic in replacements.items():
            usedVars[generic] = usedVars.pop(alt)
    return usedVars