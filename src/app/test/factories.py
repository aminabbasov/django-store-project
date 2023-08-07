import factory


class BaseFormFactory(factory.Factory):
    class Meta:
        model = None
        strategy = factory.BUILD_STRATEGY
    
    @classmethod
    def init_params(cls):
        """
        Custom method to give init params to forms.
        """
        return {}
    
    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        params = cls.init_params()
        if params:
            return model_class(**params, data=kwargs)
        
        return model_class(data=kwargs)
