from abc import ABC, abstractmethod
import numpy as np
import plotly.graph_objects as go

class LevelStyle(ABC):
    x: np.ndarray
    y: np.ndarray
    spin_pos: np.ndarray
    parity_pos: np.ndarray
    name_pos: np.ndarray
    half_width: float
    reverse: bool = False # true if go through levels from top to bottom false if going through bottom to top
    
    @abstractmethod
    def __init__(x_pos, y_pos, width, height):
        pass
    
    @abstractmethod
    def get_line(self, **kwargs):
        pass
    
    @abstractmethod
    def get_annotations(self):
        pass
    
    
    
class Flat(LevelStyle):
    '''level style ________'''
    def __init__(self, x_pos, y_pos, width, height=None):
        '''give the x_pos, y_pos and width in absolute units'''
        self.half_width = width/2
        self.x = (x_pos-self.half_width, x_pos+self.half_width)
        self.y = (y_pos, y_pos)
        self.name_pos = (x_pos+self.half_width, y_pos)
        
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        annotation = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name} {spin}{parity}", yanchor='middle', xanchor='left', showarrow=False)
        return [annotation]
        
    # def labels(self, name='', spin='', parity=''):
    #     st = f"{name} {spin}{parity}"
    #     return [st]
    
    
class Platform(LevelStyle):
    '''level style __/---\__'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos-self.half_width+shift,
                  x_pos-self.half_width+1.5*shift,
                  x_pos+self.half_width-1.5*shift,
                  x_pos+self.half_width-shift,
                  x_pos+self.half_width)
        self.y = (y_pos-height,
                  y_pos-height,
                  y_pos,
                  y_pos,
                  y_pos-height,
                  y_pos-height)
        
        self.name_pos = (x_pos + self.half_width, y_pos-height)
        self.spin_pos = (x_pos - self.half_width, y_pos-height)
        self.parity_pos = (x_pos - self.half_width, y_pos-height)
        self.reverse = True
        
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        anno1 = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name}", yanchor='middle', xanchor='left', showarrow=False)
        anno2 = dict(x=self.spin_pos[0], y=self.spin_pos[1], xref='x', yref='y', text=f"{spin}{parity}", yanchor='middle', xanchor='right', showarrow=False)
        return [anno1, anno2]

    
class IPlatform(LevelStyle):
    '''level style --\__/--'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos-self.half_width+shift,
                  x_pos-self.half_width+1.5*shift,
                  x_pos+self.half_width-1.5*shift,
                  x_pos+self.half_width-shift,
                  x_pos+self.half_width)
        self.y = (y_pos+height,
                  y_pos+height,
                  y_pos,
                  y_pos,
                  y_pos+height,
                  y_pos+height)
        
        self.name_pos = (x_pos + self.half_width, y_pos+height)
        self.spin_pos = (x_pos - self.half_width, y_pos+height)
        self.parity_pos = (x_pos - self.half_width, y_pos+height)
            
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        anno1 = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name}", yanchor='middle', xanchor='left', showarrow=False)
        anno2 = dict(x=self.spin_pos[0], y=self.spin_pos[1], xref='x', yref='y', text=f"{spin}{parity}", yanchor='middle', xanchor='right', showarrow=False)
        return [anno1, anno2]
    
    
class Raised(LevelStyle):
    '''level style --\__/--'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos+self.half_width-1.5*shift,
                  x_pos+self.half_width-shift,
                  x_pos+self.half_width)
        self.y = (y_pos,
                  y_pos,
                  y_pos+height,
                  y_pos+height)
        
        self.name_pos = (x_pos + self.half_width, y_pos+height)
        self.spin_pos = self.name_pos
        self.parity_pos = self.name_pos
            
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        annotation = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name} {spin}{parity}", yanchor='middle', xanchor='left', showarrow=False)
        return [annotation]
    
    
class IRaised(LevelStyle):
    '''level style --\__/--'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos-self.half_width+shift,
                  x_pos-self.half_width+1.5*shift,
                  x_pos+self.half_width)
        self.y = (y_pos+height,
                  y_pos+height,
                  y_pos,
                  y_pos)
        
        self.name_pos = (x_pos - self.half_width + shift, y_pos+height)
        self.spin_pos = self.name_pos
        self.parity_pos = self.name_pos
            
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        annotation = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name} {spin}{parity}", yanchor='middle', xanchor='right', showarrow=False)
        return [annotation]

    
    
class Lowered(LevelStyle):
    '''level style --\__/--'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos+self.half_width-1.5*shift,
                  x_pos+self.half_width-shift,
                  x_pos+self.half_width)
        self.y = (y_pos,
                  y_pos,
                  y_pos-height,
                  y_pos-height)
        
        self.name_pos = (x_pos + self.half_width, y_pos-height)
        self.spin_pos = self.name_pos
        self.parity_pos = self.name_pos
        self.reverse = True
            
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        annotation = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name} {spin}{parity}", yanchor='middle', xanchor='left', showarrow=False)
        return [annotation]
    
    
    
class ILowered(LevelStyle):
    '''level style --\__/--'''
    def __init__(self, x_pos, y_pos, width, height):
        self.half_width = width/2
        shift = self.half_width/8
        
        self.x = (x_pos-self.half_width,
                  x_pos-self.half_width+shift,
                  x_pos-self.half_width+1.5*shift,
                  x_pos+self.half_width)
        self.y = (y_pos-height,
                  y_pos-height,
                  y_pos,
                  y_pos)
        
        self.name_pos = (x_pos - self.half_width + shift, y_pos-height)
        self.spin_pos = self.name_pos
        self.parity_pos = self.name_pos
        self.reverse = True
            
    def get_line(self, **kwargs):
        return go.Scatter(x=self.x, y=self.y, **kwargs)
    
    def get_annotations(self, name='', spin='', parity=''):
        annotation = dict(x=self.name_pos[0], y=self.name_pos[1], xref='x', yref='y', text=f"{name} {spin}{parity}", yanchor='middle', xanchor='left', showarrow=False)
        return [annotation]
    
    
levelstyles = {"platform": Platform, "iplatform": IPlatform, "flat": Flat, 'lowered': Lowered, 'raised': Raised, 'iraised': IRaised, 'ilowered': ILowered}