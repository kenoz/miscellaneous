import re


class CSV_date(object):
    """
    This class aims to harmonize date format from a table's date column.
    This package has been developed to fix information provided by the TRY plant trait database. 

    Attributes:
        date_range (str): input date
        pattern (dict): dictionnary of date patterns described by regular expression.

    Methods:
        convert: convert input date(s) as follows: 'YYYY-MM-DD'.
    """

    def __init__(self, date_range, noDate='Nan', noM='00', noD='00'):
        self.date_range = date_range
        self.pattern = [
            {'name': 'pattern01',
             'ex': "'1990' -> '1990-00-00'",
             'pattern': r'^(19|20)\d{2}$'},
            {'name': 'pattern02',
             'ex': "'1990-05' -> '1990-05-00'",
             'pattern': r'^(19|20)\d{2}-(0[1-9]|1[0-2])$'},
            {'name': 'pattern03',
             'ex': "'1990-05-05' -> '1990-05-05'",
             'pattern': r'^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'},
            {'name': 'pattern04',
             'ex': "'1990-Feb' -> '1990-02-00'",
             'pattern': r'((19|20)\d{2})-(\w{3})$'},
            {'name': 'pattern05',
             'ex': "'1990-5-5' -> '1990-05-05'",
             'pattern': r'^((19|20)\d{2})-([1-9]|1[0-2])-([1-9]|[12][0-9]|3[01])$'},
            {'name': 'pattern06',
             'ex': "'(1990/1991)-(05/06)-(05/06)' -> start:'1990-05-05', end:'1991-06-06'",
             'pattern': r'\(((19|20)\d{2})/((19|20)\d{2})\)-\((0[1-9]|1[0-2])/(0[1-9]|1[0-2])\)-\((0[1-9]|[12][0-9]|3[01])/(0[1-9]|[12][0-9]|3[01])\)$'},
            {'name': 'pattern07',
             'ex': "'1990-5' -> '1990-05-00'",
             'pattern': r'^((19|20)\d{2})-([1-9]|1[12])$'},
            {'name': 'pattern08',
             'ex': "'(1990/1991)' -> start:'1990-00-00', end:'1991-00-00'",
             'pattern': r'^\(((19|20)\d{2})/((19|20)\d{2})\)$'},
            {'name': 'pattern09',
             'ex': "'1990-(05/06)' -> start:'1990-00-00', end:'1991-00-00'",
             'pattern': r'^((19|20)\d{2})-\((0[1-9]|1[0-2])/(0[1-9]|1[0-2])\)$'},
            {'name': 'pattern10',
             'ex': "'(1990/1991)-(05/06)' -> start:'1990-05-00', end:'1991-06-00'",
             'pattern': r'^\(((19|20)\d{2})/((19|20)\d{2})\)-\((0[1-9]|1[0-2])/(0[1-9]|1[0-2])\)$'},
            {'name': 'pattern11',
             'ex': "'(1990/1991)-(05/06)-05' -> start:'1990-05-05', end:'1991-06-05'",
             'pattern': r'^\(((19|20)\d{2})/((19|20)\d{2})\)-\((0[1-9]|1[0-2])/(0[1-9]|1[0-2])\)-(0[1-9]|[12][0-9]|3[01])$'},
            {'name': 'pattern12',
             'ex': "'1990-5/6' -> start:'1990-05-00', end:'1991-06-00'",
             'pattern': r'^((19|20)\d{2})-([1-9]|1[0-2])/([1-9]|1[0-2])$'},
            {'name': 'pattern13',
             'ex': "'(1990/1991)-05-05' -> start:'1990-05-05', end:'1991-05-05'",
             'pattern': r'^\(((19|20)\d{2})/((19|20)\d{2})\)-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'},
            {'name': 'pattern14',
             'ex': "'1990-Summer' -> start:'1990-05-05', end:'1991-05-05'",
             'pattern': r'^(\d{4})-(Spring|Summer|Automn|Winter)$'},
            {'name': 'pattern15',
             'ex': "'1990-June-July' -> start:'1990-06-00', end:'1991-07-00'",
             'pattern': r'^(\d{4})-(January|February|March|April|May|June|July|August|September|October|November|December)-(January|February|March|April|May|June|July|August|September|October|November|December)$'},
            {'name': 'pattern16',
             'ex': "'(1990/1991)-Summer' -> start:'1990-07-00', end:'1991-09-00'",
             'pattern': r'^\((\d{4})/(\d{4})\)-(Spring|Summer|Automn|Winter)$'},
            {'name': 'pattern17',
             'ex': "'1990-05-(05/06)' -> start:'1990-05-05', end:'1990-05-06'",
             'pattern': r'^(\d{4})-(0[1-9]|1[0-2])-\((0[1-9]|[12][0-9]|3[01])/(0[1-9]|[12][0-9]|3[01])\)$'},
            {'name': 'pattern18',
             'ex': "'1990/1991' -> start:'1990-00-00', end:'1991-00-00'",
             'pattern': r'^(\d{4})/(\d{4})$'}
            #{'name': 'pattern19',
            #'ex': "'1990/1991-growing season' -> start:'1990-??-00', end:'1991-??-00'",
            #'pattern': r'unknown'}
        ]

    def convert(self, no_date='NaN', d_month='00', d_day='00'):
        """
        Detect the input date pattern and convert it into the 'YYYY-MM-DD' format.

        Args:
            no_date (str, optional): value returned if no detected date. Defaults to 'NaN'.
            d_month (str, optional): value if no detected date's month. Defaults to '00'.
            d_day (str, optional): value if no detected date's day. Defaults to '00'.

        Returns:
            CSV_date.start_date (str): fornatted date (mono-date or time-range's start date).
            CSV_date.end_date (str): fornatted date of time-range's end date.
            """
        for patt in self.pattern:
            #print(patt['name'])
            #print(self.date_range)
            self.match = re.match(patt['pattern'], self.date_range)
            if self.match is not None:
                patt_search = patt['name']
                break
            else:
                patt_search = 'default'

        if patt_search == 'pattern00':
            self.start_date = no_date
            self.end_date = no_date
        if patt_search == 'pattern01':
            self.start_date = f"{self.match.group(0)}-{d_month}-{d_day}"
            self.end_date = no_date
        if patt_search == 'pattern02':
            self.start_date = f"{self.match.group(0)}-{d_day}"
            self.end_date = no_date
        if patt_search == 'pattern03':
            self.start_date = f"{self.match.group(0)}"
            self.end_date = no_date
        if patt_search == 'pattern04':
            month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            self.start_date = f"{self.match.group(1)}-{month.index(self.match.group(3))+1:02d}-{d_day}"
            self.end_date = no_date
        if patt_search == 'pattern05':
            self.start_date = f"{self.match.group(1)}-{int(self.match.group(3)):02d}-{int(self.match.group(4)):02d}"
            self.end_date = no_date
        if patt_search == 'pattern06':
            self.start_date = f"{self.match.group(1)}-{self.match.group(5)}-{self.match.group(7)}"
            self.end_date = f"{self.match.group(3)}-{self.match.group(6)}-{self.match.group(8)}"
        if patt_search == 'pattern07':
            self.start_date = f"{self.match.group(1)}-{int(self.match.group(3)):02d}-{d_day}"
            self.end_date = no_date
        if patt_search == 'pattern08':
            self.start_date = f"{self.match.group(1)}-{d_month}-{d_day}"
            self.end_date = f"{self.match.group(3)}-{d_month}-{d_day}"
        if patt_search == 'pattern09':
            self.start_date = f"{self.match.group(1)}-{self.match.group(3)}-{d_day}"
            self.end_date = f"{self.match.group(1)}-{self.match.group(4)}-{d_day}"
        if patt_search == 'pattern10':
            self.start_date = f"{self.match.group(1)}-{self.match.group(5)}-{d_day}"
            self.end_date = f"{self.match.group(3)}-{self.match.group(6)}-{d_day}"
        if patt_search == 'pattern11':
            self.start_date = f"{self.match.group(1)}-{self.match.group(5)}-{self.match.group(7)}"
            self.end_date = f"{self.match.group(3)}-{self.match.group(6)}-{self.match.group(7)}"
        if patt_search == 'pattern12':
            self.start_date = f"{self.match.group(1)}-{int(self.match.group(3)):02d}-{d_day}"
            self.end_date = f"{self.match.group(1)}-{int(self.match.group(4)):02d}-{d_day}"
        if patt_search == 'pattern13':
            self.start_date = f"{self.match.group(1)}-{self.match.group(5)}-{self.match.group(6)}"
            self.end_date = f"{self.match.group(3)}-{self.match.group(5)}-{self.match.group(6)}"
        if patt_search == 'pattern14':
            season = {'Spring':['04','06'], 'Summer':['07','09'],'Automn':['10','12'],'Winter':['01','03']}
            self.start_date = f"{self.match.group(1)}-{season[self.match.group(2)][0]}-{d_day}"
            self.end_date = f"{self.match.group(1)}-{season[self.match.group(2)][1]}-{d_day}"
        if patt_search == 'pattern15':
            month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            self.start_date = f"{self.match.group(1)}-{month.index(self.match.group(2))+1:02d}-{d_day}"
            self.end_date = f"{self.match.group(1)}-{month.index(self.match.group(3))+1:02d}-{d_day}"
        if patt_search == 'pattern16':
            season = {'Spring':['04','06'], 'Summer':['07','09'],'Automn':['10','12'],'Winter':['01','03']}
            self.start_date = f"{self.match.group(1)}-{season[self.match.group(3)][0]}-{d_day}"
            self.end_date = f"{self.match.group(2)}-{season[self.match.group(3)][1]}-{d_day}"
        if patt_search == 'pattern17':
            self.start_date = f"{self.match.group(1)}-{self.match.group(2)}-{self.match.group(3)}"
            self.end_date = f"{self.match.group(1)}-{self.match.group(2)}-{self.match.group(4)}"
        if patt_search == 'pattern18':
            self.start_date = f"{self.match.group(1)}-{d_month}-{d_day}"
            self.end_date = f"{self.match.group(2)}-{d_month}-{d_day}"
        if patt_search == 'default':
            self.start_date = "ALERT"
            self.end_date = "ALERT"

        return self.start_date, self.end_date
