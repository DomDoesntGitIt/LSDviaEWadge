from dataclasses import dataclass
import numpy as np

@dataclass
class Level:
    energy: float = None
    spin: float = None
    parity: float = None
    

@dataclass
class Transition():
    '''class to encapsulate all the information about a transition, and policing
    the entry values'''
    parent: Level = None
    daughter: Level = None
    gamma: float = None
    branching_ratio: float = None


def read(filename):
    levels = []
    transitions = []
    
    with open(filename) as f:
        # iterate through the lines
        for line in f:
            # seperate out the three different columns
            line = line.replace(' ','')
            line = line.strip()
            gamma_collect = False
            cols = line.split('>')
            
            # handle the two levels
            for i,col in enumerate((cols[0],cols[2])):
                args = col.split(',')
                for j, arg in enumerate(args):
                    if arg == 'None':
                        args[j] = None
                        continue
                    try:
                        arg = float(arg)
                        args[j] = float(args[j])
                    except ValueError:
                        pass
                
                lev = Level(*args)
                if i == 0:
                    parent = lev
                else:
                    daughter = lev
                    
                found = False
                for level in levels:
                    if lev.energy == level.energy:
                        found = True
                if not found:
                    levels.append(lev)
            
            
            # handle the transition  
            args = cols[1].split(',')
            for j, arg in enumerate(args):
                    try:
                        args[j] = float(args[j])
                    except ValueError:
                        args[j] = None   
                        
            transition = Transition(parent, daughter, *args)
            transitions.append(transition)           
                    
    return levels, transitions