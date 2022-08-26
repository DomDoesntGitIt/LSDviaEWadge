import plotly.graph_objects as go
import warnings
from dataclasses import dataclass
from .spacer import SpaceManager
from .read import Level, Transition, read
from .styles import levelstyles
import numpy as np
import copy


class Canvas(go.Figure):
    transition_defaults = dict(showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=1.5, arrowcolor='black', text='', yanchor='bottom')
    level_defaults = dict(line=dict(color='black'))
    
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.update_layout(xaxis=go.layout.XAxis(visible=False, autorange=False, range=(-0.05,1.05)),
                           yaxis=go.layout.YAxis(visible=False),
                           template='simple_white',
                           margin=dict(t=20,l=20,b=20,r=20))
    
    def add_level(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0, style: str='',
                  name='', spin='', parity='',
                  trace_kw={}, annotations_kw={}):
        
        
        
        trace_kw = copy.deepcopy(trace_kw)
        if width>1 or width<0:
            raise ValueError("width is relative width and must be between 0 and 1")
        
        
        
        for default in self.level_defaults.keys():
            if default not in trace_kw.keys():
                trace_kw[default] = self.level_defaults[default]
        
        style= style.lower()
        Style = levelstyles[style]
        levelstyle = Style(x, y, width, height)
        trace_kw["mode"] = 'lines'
        trace_kw["showlegend"] = False
        trace = levelstyle.get_line(**trace_kw)
        self.add_trace(trace)
        
        
        annotations = levelstyle.get_annotations(name=name, spin=spin, parity=parity)
        # self.update_layout(annotations=annotations)
        for anno in annotations:
            self.add_annotation(**anno, **annotations_kw)
            
    def add_transition(self, px=None, py=None, dx=None, dy=None, **kwargs):
        if None in [px,py,dx,dy]:
            raise ValueError(f"(px,py,dx,dy) must all be specified: {px,py,dx,dy} not valid")
        if px<0 or px>1 or dx<0 or dx>1:
            raise ValueError("x positions must be in relative units")
        
        kwargs = copy.deepcopy(kwargs)
              
        for default in self.transition_defaults.keys():
                if default not in list(kwargs.keys()):
                    kwargs[default] = self.transition_defaults[default]
                    
        kwargs["xref"] = 'x'
        kwargs["axref"] = 'x'
        kwargs['yref'] = 'y'
        kwargs['ayref'] = 'y'
        
        self.add_annotation(x=dx, y=dy, ax=px, ay=py, **kwargs)
            
    def read_from_nlv(self, filename:str, spacing=100, x_points=np.linspace(0.2,0.8,10),
                      transition_sort: callable = None, proportional=False, br_widths=False,
                      auto_sort: bool = True, level_kw={}, transition_kw={}):
        levels, transitions = read(filename)
        
        float_levels = []
        for level in levels:
            float_levels.append(level.energy)
        
        if 'style' in level_kw.keys():
            Style = levelstyles[level_kw['style']]
            reverse = Style(0,0,0,0).reverse
        else:
            reverse=False
        
        
        spc_mng = SpaceManager(x_points, float_levels, spacing=spacing, reverse=reverse)
        
        
        defaults = dict(x=0.5, width=1, style='flat', height=10, trace_kw=dict(line=dict(color='black')))
        level_kw_cp = copy.deepcopy(level_kw) 
        for default in defaults.keys():
                if default not in list(level_kw.keys()):
                    level_kw_cp[default] = defaults[default]
        
        # make the levels
        for level in levels:            
            available_y = spc_mng.get_spaced_y(level.energy)
            # print(level.energy, available_y)
            if level.spin == None:
                spin = ''
            else:
                spin = str(level.spin)
                
            if level.parity == None:
                parity = ''
            else:
                parity = str(level.parity)

            if proportional:
                # level_kw_cp = copy.deepcopy(level_kw) 
                level_kw_cp['height'] += abs(available_y - level.energy)
                self.add_level(y=level.energy, name=str(level.energy), spin=spin, parity=parity, **level_kw_cp)
                #undo the change
                level_kw_cp['height'] -= abs(available_y - level.energy)
            else:
                self.add_level(y=available_y, name=str(level.energy), spin=spin, parity=parity, **level_kw_cp)
            
        
        if transition_sort is None:
            transitions.sort(key=lambda transition: transition.parent.energy)
        else:
            transitions.sort(key=transition_sort)
            
        
        # make the transitions
        
            
        
        for i,transition in enumerate(transitions):
            cpy_transition_kw = copy.deepcopy(transition_kw)
            
            if auto_sort:
                #try to minimize the width with simple algorithm
                available_x = spc_mng.get_path(transition.parent.energy, transition.daughter.energy)
            else:
                available_x = spc_mng.xspace[-i]    
            
            available_y_head = spc_mng.get_spaced_y(transition.daughter.energy)
            available_y_tail = spc_mng.get_spaced_y(transition.parent.energy)
            
            if br_widths:
                if "arrowwidth" in cpy_transition_kw.keys():
                    try:
                        cpy_transition_kw["arrowwidth"] *= (1+transition.branching_ratio)
                    except TypeError:
                        pass
                else:
                    try:
                        cpy_transition_kw["arrowwidth"] = self.transition_defaults["arrowwidth"] * (1+transition.branching_ratio)
                    except TypeError:
                        pass
            
            if proportional:
                self.add_transition(px=available_x,
                                    dx=available_x,
                                    py=transition.parent.energy,
                                    dy=transition.daughter.energy,
                                    **cpy_transition_kw)
            else:
                self.add_transition(px=available_x,
                                    dx=available_x,
                                    py=available_y_tail,
                                    dy=available_y_head,
                                    **cpy_transition_kw)
        
        
        
        
            
        


    