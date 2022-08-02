import warnings
import numpy as np
import copy

class SpaceManager:
    '''class to oversee the placement of levels and decays so they don't overlap'''
    def __init__(self, xspace, levels, spacing=None, reverse=False):
        '''xspace is valid points in x to connect a transition to, levels are the different level,
        normalize regions even space the level in region ((lower,upper),) support multiple regions'''
        
        # dictionary for translating level to index in matrix
        self.dict_level = {}
        # track the allowed x positions
        self.xspace = xspace
        
        # change levels to a list of floats so we can sort them
        if not isinstance(levels, list):
            levels = list(levels)
        
        
        # sort levels so that there are in correct order this is necessary for identifying overlaps in grid
        
        self.levels = copy.deepcopy(levels)
        self.levels.sort()
        for i,level in enumerate(self.levels):
            # assign index to each level name
            self.dict_level[str(level)] = i
            
        # make a matrix of proper size to track what nodes have been taken
        self.space = np.zeros((len(levels),len(xspace)))
        
        # apply normalization to regions
        if spacing != None:
            # print(f'{spacing}, {reverse}')
            normalize_regions = self.get_normalized_regions(self.levels, spacing, reverse=reverse)
            # print(normalize_regions)
            self.spaced_y = copy.deepcopy(self.levels)
            self._make_room(normalize_regions, reverse=reverse)
            
        
    def _make_room(self, regions, reverse=False):
        '''function for calculating the spread out levels in a region'''
        for region in regions:
            count = 0
            bool_lst = []
            for level in self.levels:
                # tag levels within the region
                if level <= region[1] and level >= region[0]:
                    count += 1 # track how many levels in region
                    bool_lst.append(True)
                # elif level == 2849.6:
                #     print(f'wtf is this {region[0]}, {region[1]}')
                else:
                    bool_lst.append(False)
             
            # find even spacing of levels in that region
            even_spacing = (region[1] - region[0])/count
            track = 0
            
            if reverse:
                rng = range(len(self.levels)-1,0,-1)
                sign = -1
                j = 1
            else:
                rng = range(0,len(self.levels))
                sign = 1
                j = 0
            
            for i in rng:
                flag = bool_lst[i]
                # if tagged adjust the spaced_y to be correct
                if flag:
                    self.spaced_y[i] = sign*even_spacing*track + region[j]
                    track += 1
                
    
    def get_spaced_y(self, level):
        '''return properly spaced levels'''
        i = self.dict_level[str(level)]
        return self.spaced_y[i]
        
    def get_path(self, start_level, end_level):
        '''find viable path between parent and daughter level'''
        end_i = self.dict_level[str(start_level)]
        start_i = self.dict_level[str(end_level)]
        # slice the relevant nodes (nothing else matters)
        relevant_slice = self.space[start_i:end_i+1,:]
        
        # iterate backwards for cosmetic reasons
        for i in range(len(relevant_slice.T)-1, -1, -1):
            # select a column
            column = relevant_slice.T[i]
            # if column is all zeros then we can pass through
            if 1 not in column: 
                # path is no longer viable set the relevant slice of selected col to 1
                self.space[start_i:end_i,i] = 1
                # return the found x position
                return self.xspace[i]
        warnings.warn("Ran out of space appending to end")
        return self.xspace[-1]
    
    @staticmethod    
    def get_normalized_regions(levels, spacing, reverse=False):
        
        groups = []
        group_num = 0
        group_flag = False
        end = False
        # print(levels)
        if reverse:
            rng = range(len(levels)-2,0,-1)
            dr = 1
        else:
            rng = range(1,len(levels)-1)
            dr = -1
            
        for i in rng:
            # check if there any levels that are too close
            
            
            if abs(levels[i+dr]-levels[i]) < spacing:
                
                if group_flag == False:
                    groups.append([])               
                    groups[group_num].append(levels[i+dr])
                    groups[group_num].append(levels[i])
                    group_flag = True
                else:
                    groups[group_num].append(levels[i])
                    
                    
            elif group_flag == True:
                if abs(max(groups[group_num])-levels[i]) < len(groups[group_num])*spacing and reverse:
                    groups[group_num].append(levels[i])    
                elif abs(min(groups[group_num])-levels[i]) < len(groups[group_num])*spacing and not reverse:
                    groups[group_num].append(levels[i])
                else:
                    group_flag = False
                    group_num += 1
            
            
        normalize_regions = []
        # print(groups)
        for group in groups:
            if not reverse:
                normalize_regions.append((min(group)-1,min(group)+len(group)*spacing))
            else:
                normalize_regions.append((max(group)-len(group)*spacing,max(group)+1))
        # print(normalize_regions)
        return normalize_regions