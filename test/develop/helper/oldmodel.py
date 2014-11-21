'''
Created on Nov 14, 2014

@author: rhf
'''

import pprint as pp

class OldModel(object):
    '''
    Loads and builds SasView based models
    '''


    def __init__(self, modelname, **pars):
        '''
        Constructor
        '''
        self.modelname = modelname
        self.pars = self._scaleSld(pars)
        self.model = None
        
    def _buildModel(self, force=False):
        """
        Build a model
        """
        
        if force or self.model is None: 
            modelname  = self.modelname
            sans = __import__('sans.models.'+modelname)
            ModelClass = getattr(getattr(sans.models,modelname,None),modelname,None)
            if ModelClass is None:
                raise ValueError("could not find model %r in sans.models"%modelname)
            self.model = ModelClass()                    
            self._setPolydispersitityParams()
            
            
    
    def getModel(self):
        self._buildModel()
        return self.model
    
    def eval(self,data,nIterations=1):
        model = self.getModel()
        for _ in range(nIterations):
            ret = model.evalDistribution(data)
        return ret
        
    def _scaleSld(self,pars):
        """
        For parameters starting with sld multiplies the value for 1e-6 
        """
        return dict((p, (v*1e-6 if ( p.startswith('sld') or p.endswith('sld') ) else v)) for p,v in pars.items())
    
    def _setPolydispersitityParams(self):
        for k,v in self.pars.items():
            if k.endswith("_pd"):
                self.model.dispersion[k[:-3]]['width'] = v
            elif k.endswith("_pd_n"):
                self.model.dispersion[k[:-5]]['npts'] = v
            elif k.endswith("_pd_nsigma"):
                self.model.dispersion[k[:-10]]['nsigmas'] = v
            elif k.endswith("_pd_type"):
                self.model.dispersion[k[:-8]]['type'] = v
            else:
                self.model.setParam(k, v)
        