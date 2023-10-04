"""config.py

Defines volcanoes and ASF projects to be used throughout the rest of the
module.

The volcano_list and asf_list defined here are used by default, but can
be overridden by providing a custom list to the InSARProcessor constructor. 
"""

from collections import defaultdict
try:
    from .filter_dates import filter_dates
except ImportError:
    from filter_dates import filter_dates

class VolcanoArea: # this stores needed information for locating a volcano area and processing it
    def __init__(self, volc_name, ul, lr, path, frame, asf_name, run_flag = 0):
        self.volc_name = volc_name # if aoi contains >1 volcanoes, label volc_name would only be one of them
        
        # Filter dates are defined in the seperate filter_dates.py file
        # just to keep things clean and managable.
        self.filter_dates = filter_dates.get((volc_name,path), []) # bad dates to skip (e.g. shifted-frame scenes)

        self.ul = ul # [x,y] aoi information, satellite coordinates of upper-left conner
        self.lr = lr # lower-right
        self.path = path # integer, same for frame
        self.frame = frame
        self.asf_name = asf_name # asf vertex project name, string, must be same as that shown on asf
        self.run_flag = run_flag # indicate whether to run or skip the processing of current volcano; 1 for run

    def update_flag(self, new_flag):
        self.run_flag = new_flag


class ASFArea:
    def __init__(self, asf_name, path, frame, last_date):
        self.asf_name = asf_name
        self.path = path
        self.frame = frame
        self.last_date = last_date

    def update_date(self,new_date):
        self.last_date = new_date

################# VOLCANO DEFINITIONS ####################
# order: volc_name, filter_dates, ul, lr, path, frame, asf_name
# Coordinates are in UTM projection.
seguam15 = VolcanoArea('seguam',[388200,5806000],[411800,5789000],15,419,'015_421')
chagulak15 = VolcanoArea('chagulak',[478400,5826500],[492200,5810900],15,419,'015_421')
yunaska15 = VolcanoArea('yunaska',[510200,5837500],[530200,5821300],15,419,'015_421')

kiska30 = VolcanoArea('kiska',[513500,5776800],[548600,5741000],30,420,'st_semisopochnoi_real')
davidof30 = VolcanoArea('davidof',[574600,5768000],[609300,5750700],30,420,'st_semisopochnoi_real')
semisopochnoi30 = VolcanoArea('semisopochnoi',[669600,5767700],[690700,5750000],30,420,'st_semisopochnoi_real')

makushin41044 = VolcanoArea('makushin410',[355800,5987000],[428600,5930000],44,410,'044_410')
akutan44 = VolcanoArea('akutan',[427000,6009000],[475000,5987000],44,410,'044_410')
westdahl44 = VolcanoArea('westdahl',[503000,6093000],[564000,6026700],44,410,'044_410')

okmok44 = VolcanoArea('okmok',[271300,5940000],[315800,5903000],44,415,'044_415')
makushin41544 = VolcanoArea('makushin415',[309000,5976000],[426800,5903000],44,415,'044_415')

edgecumbe50 = VolcanoArea('edgecumbe',[446764,6356464],[459347,6315619],50,182,'050_182')

gareloi59 = VolcanoArea('gareloi',[370600,5744700],[380500,5734000],59,420,'059_419')
takawangha59 = VolcanoArea('takawangha',[415000,5753200],[457400,5716100],59,420,'059_419')
kanaga59 = VolcanoArea('kanaga',[451000,5755000],[496800,5722500],59,420,'059_419')
moffett59 = VolcanoArea('moffett',[500600,5762000],[540000,5715000],59,420,'059_419')
greatsitkin59 = VolcanoArea('greatsitkin',[554000,5774600],[570000,5757000],59,420,'059_419')

amak73 = VolcanoArea('amak',[230000,6151500],[273000,6094000],73,407,'073_407')
pavlof73 = VolcanoArea('pavlof',[276000,6206000],[390000,6101000],73,407,'073_407')

unimak73 = VolcanoArea('unimak',[565700,6102000],[626000,6052000],73,412,'073_412')

edgecumbe79 = VolcanoArea('edgecumbe',[448000,6355000],[467000,6317500],79,186,'079_186')

kiska81 = VolcanoArea('kiska',[513500,5776500],[548800,5741000],81,166,'081_166')
davidof81 = VolcanoArea('davidof',[574400,5777700],[609500,5750700],81,166,'081_166')
semisopochnoi81 = VolcanoArea('semisopochnoi',[669700,5767500],[690600,5750000],81,166,'081_166')

atka88 = VolcanoArea('atka',[232000,5813000],[366500,5766000],88,418,'088_418')
seguam88 = VolcanoArea('seguam',[388400,5806000],[411500,5789600],88,418,'088_418')

ukinrek102 = VolcanoArea('ukinrek',[620000,6460000],[680000,6406000],102,397,'102_397')
martin102 = VolcanoArea('martin',[670000,6476000],[736500,6403000],102,397,'102_397')
trident102 = VolcanoArea('trident',[697100,6476800],[752800,6426700],102,397,'102_397')
katmai102 = VolcanoArea('katmai',[700000,6505000],[766000,6440000],102,397,'102_397')

aniakchak102 = VolcanoArea('aniakchak',[500000,6357000],[659000,6250000],102,402,'102_402')
blue102 = VolcanoArea('blue',[600000,6400000],[675000,6377000],102,402,'102_402')

buldir103 = VolcanoArea('buldir',[421000,5805000],[430200,5798800],103,419,'103_419')
kiska103 = VolcanoArea('kiska',[513000,5777000],[593900,5741500],103,419,'103_419')

cleveland117 = VolcanoArea('cleveland',[555000,5882600],[589900,5841000],117,417,'117_417')
vsevidof117 = VolcanoArea('vsevidof',[626300,5940000],[713200,5854300],117,417,'117_417')

spurr131 = VolcanoArea('spurr',[495000,6840000],[590000,6690000],131,388,'spurr')

augustine131 = VolcanoArea('augustine',[467000,6587000],[480800,6575500],131,393,'131_393')
redoubt131 = VolcanoArea('redoubt',[482579,6728984],[544694,6635304],131,393,'131_393')

snowy131 = VolcanoArea('snowy',[392635,6485168],[442269,6429478],131,398,'131_398')
knob131 = VolcanoArea('knob',[401149,6511651],[434126,6484394],131,398,'131_398')
kaguyak131 = VolcanoArea('kaguyak',[430231,6549376],[485921,6482697],131,398,'131_398')

buldir154 = VolcanoArea('buldir',[421000,5804900],[430700,5798800],154,166,'154_166')
kiska154 = VolcanoArea('kiska',[513200,5776800],[581500,5741800],154,166,'154_166')

moffett161 = VolcanoArea('moffett',[500300,5761700],[540100,5715500],161,418,'161_418')
greatsitkin161 = VolcanoArea('greatsitkin',[553800,5774700],[570700,5757700],161,418,'161_418')
atka161 = VolcanoArea('atka',[600600,5812000],[705200,5763000],161,418,'161_418')

veniaminof102 = VolcanoArea('veniaminof',[467500,6253000],[526900,6203000],102,407,'102_407')

###################### END VOLCANO DEFINITIONS ########################

# volcanoes to be processed
# user can add their own volcano processings here, just define them first
volcano_list = [seguam15, chagulak15, yunaska15, \
                kiska30, davidof30, semisopochnoi30, \
                makushin41044, akutan44, westdahl44, \
                okmok44, makushin41544, \
                edgecumbe50, \
                gareloi59, takawangha59, kanaga59, moffett59, greatsitkin59, \
                amak73, pavlof73, \
                unimak73, \
                edgecumbe79, \
                kiska81, davidof81, semisopochnoi81, \
                atka88, seguam88, \
                ukinrek102, martin102, katmai102, trident102, \
                aniakchak102, blue102, \
                veniaminof102, \
                kiska103, \
                cleveland117, vsevidof117, \
                spurr131, \
                augustine131, redoubt131, \
                snowy131, knob131, kaguyak131, \
                kiska154, \
                moffett161, greatsitkin161, atka161]

# Create an asf_name to multi-volcano lookup table
volc_lookup = defaultdict(list)
for volc in volcano_list:
    volc_lookup[volc.asf_name].append(volc)

# date-line projects
# kiska30
# kiska81

# The last_date strings here are random. They will be automatically corrected during processing.
path15_419 = ASFArea('015_421',15,419,'20230305')
path30_420 = ASFArea('st_semisopochnoi_real',30,420,'20230222')
path44_410 = ASFArea('044_410',44,410,'20230307')
path44_415 = ASFArea('044_415',44,415,'20230307')
path50_182 = ASFArea('050_182',73,412,'20230309')
path59_420 = ASFArea('059_419',59,420,'20230320')
path73_407 = ASFArea('073_407',73,407,'20230309')
path73_412 = ASFArea('073_412',73,412,'20230309')
path79_186 = ASFArea('079_186',79,186,'20230309')
path81_166 = ASFArea('081_166',81,166,'20230226')
path88_418 = ASFArea('088_418',88,418,'20230310')
path102_397 = ASFArea('102_397',102,397,'20230311')
path102_402 = ASFArea('102_402',102,402,'20220323')
path102_407 = ASFArea('102_407',102,407,'20220323')
path103_419 = ASFArea('103_419',103,419,'20230311')
path117_417 = ASFArea('117_417',117,417,'20230228')
path131_388 = ASFArea('spurr',131,388,'20230301')
path131_393 = ASFArea('131_393',131,393,'20230301')
path131_398 = ASFArea('131_398',131,398,'20230301')
path154_166 = ASFArea('154_166',154,166,'20230303')
path161_418 = ASFArea('161_418',161,418,'20230303')

# The list of ASF Projects to check/update by default.
# Can be overriden by providing a different list to the InSARProcessor
asf_list = [
    path15_419,path30_420,path44_410,path44_415,path50_182,
    path59_420,path73_407,path73_412,path79_186,path81_166,
    path88_418,path102_397,path102_402,
    path102_407,
    path103_419,
    path117_417,path131_388,path131_393,path131_398,
    path154_166,path161_418
]

###### DEBUG/TESTING #####
asf_list = [path44_410, path50_182, path81_166]
