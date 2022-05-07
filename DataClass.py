from datetime import date, datetime
#\ Data class for the simplify imfomation
class simplifyTableInfo:
    def __init__(self, IdNumber, Dates, Times, City, District, Place, Altitude, User):
        self.IdNumber = IdNumber
        self.Dates = Dates  #\ 2020-07-25
        self.Times = Times  #\ 09:00:02
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


#\ Data class for DetailedTable infomation
class DetailedTableInfo(simplifyTableInfo):
    def __init__(self, IdNumber:str="", Dates:str="", Times:str="", City:str="", District:str="", Place:str="",
                Altitude:str="", User:str="", Latitude:str="", Longitude:str="", SpeciesFamily:str="",
                FilteredSpeciesList:list=[""], SpeciesList:list=[""], Description:str="", weather:str="", rarity:list=[""]):
        super(DetailedTableInfo, self).__init__(IdNumber, Dates, Times, City, District, Place, Altitude, User)
        self.Latitude               = Latitude
        self.Longitude              = Longitude
        self.SpeciesFamily          = SpeciesFamily
        self.FilteredSpeciesList    = FilteredSpeciesList
        self.SpeciesList            = SpeciesList
        self.Description            = Description
        self.weather                = weather
        self.rarity                 = rarity

        #\ handle the Description to make it print better
        self.Description = list(self.Description.split("\n"))
        self.Description = f"\n{' '*21}".join(self.Description)



    def __str__(self):
        '''
        return (super(DetailedTableInfo, self).__str__()+
                '\t[Latitude]: ' + self.Latitude +
                '\t[Longitude]: ' + self.Longitude +
                '\t[Species]: ' + self.Species +
                '\t[Description]: ' + self.Description)
        '''
        return  f'\n[----- {__name__} -----]' + \
                '\n-->[IdNumber]:       ' + self.IdNumber + \
                '\n-->[Dates]:          ' + self.Dates + \
                '\n-->[Times]:          ' + self.Times + \
                '\n-->[City]:           ' + self.City + \
                '\n-->[District]:       ' + self.District + \
                '\n-->[Altitude]:       ' + self.Altitude + \
                '\n-->[Place]:          ' + self.Place + \
                '\n-->[User]:           ' + self.User + \
                '\n-->[Latitude]:       ' + self.Latitude + \
                '\n-->[Longitude]:      ' + self.Longitude + \
                '\n-->[Species]:        ' + ", ".join(self.FilteredSpeciesList)+ \
                '\n-->[SpeciesFamily]:  ' + self.SpeciesFamily + \
                '\n-->[SpeciesList]:    ' + ", ".join(self.SpeciesList) + \
                '\n-->[Description]:    ' + self.Description + \
                '\n-->[weather]:        ' + self.weather + \
                '\n-->[rarity]:         ' + self.rarity




#\ Filter Object for the dragonfly data
class FilterObject:
    def __init__(self, UserFilter=None, SpeciesFilter=None, TimeFilter=None, RecordNotTodayDateFilter=None, KeepOrFilter=None):
        self.UserFilter = UserFilter #\ user to filter
        self.SpeciesFilter = SpeciesFilter #\ species to filter
        self.TimeFilter = TimeFilter #\ time to filter
        self.RecordNotTodayDateFilter = RecordNotTodayDateFilter #\ filter to decide whether to keep only today's data(Yes) or the data uploaded today but record other day(No)
        self.KeepOrFilter = KeepOrFilter #\ KeepOrFilter: indicate to do filter(False) or keep(True) the data if satisfied the condition

    #\ Filter to filter out the data with specific condition
    def DataFilter(self, Data:DetailedTableInfo)->list:
        """
        @params:
            Data: the data to filter, in DetaildTableInfo
        @return:
            (1)
            if KeepOrFilter True to keep the data
                True: keep
                False: not to keep to filter out
            if KeepOrFilter False to filter the data
                True: Filter out
                False: Not Filter out, so to keep it
            (2)
            Species_intersection_set:list of the filtered species
        """
        UserFilter_State = False
        SpeciesFilter_State = False
        TodayDataFilter_State = False

        #\ No input then return True, since nothing is going to filter
        if self.UserFilter is None and self.SpeciesFilter is None or \
            self.KeepOrFilter is None or self.RecordNotTodayDateFilter is None:
            print("[Warning] In DataFilter object the self.UserFilter is None and self.SpeciesFilter is None or self.KeepOrFilter is None or self.RecordNotTodayDateFilter is None:")
            return [True if self.KeepOrFilter is True else False, []]

        #\ User filter
        if self.UserFilter is not None:
            if len(self.UserFilter) > 0:
                UserFilter_State = Data.User in self.UserFilter

        #\ Species filter
        Species_intersection_set = []
        if self.SpeciesFilter is not None:
            if len(self.SpeciesFilter) > 0:
                Species_intersection_set = set(Data.SpeciesList) & set(self.SpeciesFilter)
                SpeciesFilter_State = len(Species_intersection_set) > 0

        #\ Time filter

        #\ Record Not Today Date Filter
        if self.RecordNotTodayDateFilter is not None and self.RecordNotTodayDateFilter is False:
            #\ Filter out the data that is old but upload to the database today and get the newer ID.
            #\ Time data got from web: 2020-01-12 -> datetime.datetime(2020,1,12) for comparison
            Check = True
            #\ This is the workaround that some user might forget to type the dates (0000-00-00)
            #\ It'll cause error when using datetime library
            try:
                datetime.strptime(Data.Dates, "%Y-%m-%d").date()
            except:
                Check = False
                print(f"[Warning] The time might not be vaild since user input incorrect: {Data.Dates}")

            if Check:
                TodayDataFilter_State =  datetime.strptime(Data.Dates, "%Y-%m-%d").date() != date.today()
                if TodayDataFilter_State:
                    print(f"Filter out the data(ID: {Data.IdNumber}) that's not record today({Data.Dates}) but submit today({date.today()})")

        #\ Considering all the filter and get the final result
        Filter_State = UserFilter_State & SpeciesFilter_State & TodayDataFilter_State
        if Filter_State:
            print(f"[INFO] In DataFilter() Filter_State: {Filter_State}, ID: {Data.IdNumber}, Species_intersection_set: {Species_intersection_set}")


        return [Filter_State if self.KeepOrFilter is True else not Filter_State, list(Species_intersection_set)]