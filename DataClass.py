# Data class for the simplify imfomation
class simplifyTableInfo:
    def __init__(self, IdNumber, Dates, Times, City, District, Place, Altitude, User):
        self.IdNumber = IdNumber
        self.Dates = Dates
        self.Times = Times
        self.City = City
        self.District = District
        self.Place = Place
        self.Altitude = Altitude
        self.User = User

    def __str__(self):
        return ('\n[IdNumber]: ' + self.IdNumber +
                '  [Dates]: ' + self.Dates +
                '  [Times]: ' + self.Times +
                '  [City]: ' + self.City +
                '  [District]: ' + self.District +
                '  [Altitude]: ' + self.Altitude +
                '  [Place]: ' + self.Place,
                '  [User]:' + self.User)


# Data class for DetailedTable infomation
class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber:str="", Dates:str="", Times:str="", City:str="", District:str="", Place:str="",
                Altitude:str="", User:str="", Latitude:str="", Longitude:str="", SpeciesFamily:str="",
                Species:str="", SpeciesList:list=[""], Description:str="", weather:str=""):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, District, Place, Altitude, User)
        self.Latitude       = Latitude
        self.Longitude      = Longitude
        self.SpeciesFamily  = SpeciesFamily
        self.Species        = Species
        self.SpeciesList    = SpeciesList
        self.Description    = Description
        self.weather        = weather

        #\ handle the Description to make it print better
        self.Description = list(self.Description.split("\n"))
        self.Description = f"\n{' '*18}".join(self.Description)



    def __str__(self):
        '''
        return (super(DetailedTableInfo, self).__str__()+
                '\t[Latitude]: ' + self.Latitude +
                '\t[Longitude]: ' + self.Longitude +
                '\t[Species]: ' + self.Species +
                '\t[Description]: ' + self.Description)
        '''
        return  f'\n[----- {__name__} -----]' + \
                '\n-->[IdNumber]: ' + self.IdNumber + \
                '\n-->[Dates]: ' + self.Dates + \
                '\n-->[Times]: ' + self.Times + \
                '\n-->[City]: ' + self.City + \
                '\n-->[District]: ' + self.District + \
                '\n-->[Altitude]: ' + self.Altitude + \
                '\n-->[Place]: ' + self.Place + \
                '\n-->[User]:' + self.User + \
                '\n-->[Latitude]: ' + self.Latitude + \
                '\n-->[Longitude]: ' + self.Longitude + \
                '\n-->[Species]: ' + self.Species + \
                '\n-->[SpeciesFamily]: ' + self.SpeciesFamily + \
                '\n-->[SpeciesList]: ' + ", ".join(self.SpeciesList) + \
                '\n-->[Description]: ' + self.Description + \
                '\n-->[weather]: ' + self.weather