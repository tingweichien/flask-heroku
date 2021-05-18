# Data class for the simplify imfomation
class simplifyTableInfo:
    def __init__(self, IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User):
        self.IdNumber = IdNumber
        self.Dates = Dates
        self.Times = Times
        self.City = City
        self.Dictrict = Dictrict
        self.Place = Place
        self.Altitude = Altitude
        self.User = User

    def __str__(self):
        return ('\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [Dictrict]: ' + self.Dictrict +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User)


# Data class for DetailedTable infomation
class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber:str, Dates:str, Times:str, City:str, Dictrict:str, Place:str,
                Altitude:str, User:str, Latitude:str, Longitude:str, SpeciesFamily:str,
                Species:str, Description:str, weather=None):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, Dictrict, Place, Altitude, User)
        self.Latitude       = Latitude
        self.Longitude      = Longitude
        self.SpeciesFamily  = SpeciesFamily
        self.Species        = Species
        self.Description    = Description
        self.weather        = weather

    def __str__(self):
        '''
        return (super(DetailedTableInfo, self).__str__()+
                '\t[Latitude]: ' + self.Latitude +
                '\t[Longitude]: ' + self.Longitude +
                '\t[Species]: ' + self.Species +
                '\t[Description]: ' + self.Description)
        '''
        print(  '\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [Dictrict]: ' + self.Dictrict +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User+
                '  [Latitude]: ' + self.Latitude +
                '  [Longitude]: ' + self.Longitude +
                '  [Species]: ' + self.Species +
                '  [SpeciesFamily]: ' + self.SpeciesFamily +
                '  [Description]: ' + self.Description +
                '  [weather]: ' + self.weather)