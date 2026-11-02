class Singleton: 
    _instance = None 
    _initialized = False 

    def __new__(cls, **kwargs): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
            cls._initialized = False 
        return cls._instance

    def __init__(self, **kwargs):
        if self._initialized: 
            return 
        
        # set vars from kwards
        for name, value in kwargs.items(): 
            setattr(self, name, value)
            print(f'Set var: {name}={value}')
        self._initialized = True 

        # get list of class vars and find if any were left uninitialized
        singleton_vars = set([ 
            name for name, _ in vars(Singleton).items() if not name.startswith('__')
        ])

        subclass_vars = set([ 
            name for name, _ in vars(self.__class__).items() if not name.startswith('__')
        ])

        uninitialized_vars = set(filter(
            lambda x: x not in (subclass_vars - singleton_vars), 
            self.__class__.__annotations__.keys()
        ))

        # raise Exception if a var was left uninitialized 
        missing_vars = []
        for var in uninitialized_vars: 
            if var not in kwargs: 
                missing_vars.append(var)
        if len(missing_vars) > 0: 
            raise Exception(f'{self.__class__.__name__} initialized with improper kwargs ...'
                + f'missing the following uninitialized args: {', '.join(missing_vars)}')

# class SingletonSubclass(Singleton): 
#    value: str 
#
# s = SingletonSubclass(value = 'test')