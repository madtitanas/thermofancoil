import math
import logging


#logger = logging.getLogger(__name__)



class Panel():

    def __init__(self, model, height,depth,length,n):
        #TODO should I have the type here e.g. 22/33/
        self.model =model
        self.height=height
        self.depth=depth
        self.length=length
        #the n dimesionless value depending on the geometry og the radiator
        self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        self.ThermalOutput={}


    def addThermalOutputData(self,ThermalOutput,Tzi,Tpi,Tii):
        # this fucntion add thermal Output data as a function of Tz,Tp,Ti provided by the manufacturer
        # Tzi   :   supply water functional temperature Celcious (Flow temperature)
        # Tpi   :   return water functional temperature Celcious (Return temperature
        # Tii   :   Room functional temperature Celcious          (Room temperature)
        # ThermalOutput  :   Thermal output in Watts Celcious
        self.ThermalOutput[Tzi,Tpi,Tii]=ThermalOutput


    def calculate_thermal_output(self,Tzi,Tpi,Tii):


        # this function will calculate the Thermal Output for values Tz,Tp,Ti that are not included in the factory values

        #Checking
        #  this function will calculate the Thermal Output for values Tz,Tp,Ti that are not included in the factory values


        #TODO the reason this is not implemented is becasue ti have not decided where the table with the factory values
        #TODO will be loaded.
        #TODO The best idea would be that the Fancoils are actually three different normal panels, one for each speed
        #TODO setting, but we need to load the values somewhere...
        pass


    def _deeltaTe(self,Tz,Tp,Ti):
        #Tz :   supply water temperature
        #Tp :   return water temperature
        #Ti :   Room temperature
        #print "Tz,Tp,Ti:",Tz,Tp,Ti
        #print "Tp-Ti:",Tp-Ti
        #print "Tz-Ti",Tz-Ti
        #print  math.log((Tz-Ti)/(Tp-Ti))
        #print ">",Tz-Tp, math.log((Tz-Ti)/(Tp-Ti))
        return (Tz-Tp)/(math.log((Tz-Ti)/(Tp-Ti)))

    def _thermalOutput(self,Tzi,Tpi,Tii,Tzn,Tpn,Tin,Fn,n):
        # Tzi   :   supply water functional temperature
        # Tpi   :   return water functional temperature
        # Tii   :   Room functional temperature
        # Tz    :   supply water reference temperature
        # Tp    :   return water reference temperature
        # Ti    :   Room reference temperature
        # Fn    :   Reference Thermal Output
        # n     :   n value that depends on the radiator geometry

        return Fn*pow(self._deeltaTe(Tzi,Tpi,Tii)/self._deeltaTe(Tzn,Tpn,Tin),n)


    def _nFactor(self,Tzi,Tpi,Tii,Tzn,Tpn,Tin,Fn,Fi):
        # Tzi   :   supply water functional temperature
        # Tpi   :   return water functional temperature
        # Tii   :   Room functional temperature
        # Tz    :   supply water reference temperature
        # Tp    :   return water reference temperature
        # Ti    :   Room reference temperature
        # Fn    :   Reference Thermal Output
        # Fi    :   Functional Thermal Output
        #print ">",math.log(Fn)-math.log(Fi),math.log(self._deeltaTe(Tzn,Tpn,Tin)/self._deeltaTe(Tzi,Tpi,Tii)),(math.log(Fn)-math.log(Fi))/(math.log(self._deeltaTe(Tzn,Tpn,Tin)/self._deeltaTe(Tzi,Tpi,Tii)))
        #return (math.log(Fn)-math.log(Fi))/(math.log(self._deeltaTe(Tzi,Tpi,Tii)/self._deeltaTe(Tzn,Tpn,Tin)))
        #TODO there was a change form the previous value here sot that n is not negative. Please verify the formula
        #I have
        return (math.log(Fn)-math.log(Fi))/(math.log(self._deeltaTe(Tzn,Tpn,Tin)/self._deeltaTe(Tzi,Tpi,Tii)))




class FanCoilPanel(Panel):
 #   def addThermalOutputData(self,ThermalOutput,Tzi,Tpi,Tii,FanSpeed):
        # this function add thermal Output data as a function of Tz,Tp,Ti provided by the manufacturer
        # Tzi   :   supply water functional temperature Celcious (Flow temperature)
        # Tpi   :   return water functional temperature Celcious (Return temperature
        # Tii   :   Room functional temperature Celcious          (Room temperature)
        # ThermalOutput  :   Thermal output in Watts Celcious
        #self.ThermalOutput[Tzi,Tpi,Tii,FanSpeed]=ThermalOutput

    #FanCoils also have the Fanspeed factor


 def lowest_setting_for_thermal_output(self,ThermalOutput,MaxWaterInTemp=70):
        #TODO is there a reason to have MaxWaterinTemp > 70 for fancoils
        #this function will start from lowest Tzi,Tpi value (30/25)
        #and will try to calculate which setting of (Tzi.,Tpi) will achieve the thermal output given in the Argument
        #Argument is supposed to be in KWatts
        #TODO for the moment we only work with Tzi-Tpi=5

        if (ThermalOutput <0.5 or ThermalOutput > 15):
            return None
        RetValue={}
        for i in range(MaxWaterInTemp-30):
            #TODO the dictionary index should not be hardcoded
            Result=self.calculate_thermal_output1(30.0 + i, 25 + i, 20.0)
            #TODO this should be moved in a debug function using a log file
            logging.debug("Checking for %f at %s/%s and we got %s %s %s",ThermalOutput,str(30.0 + i),str(25 + i),Result['min'],Result['mid'],Result['max'])
            if Result['min']>=ThermalOutput:
                RetValue['min']=str(30.0 + i)+"/"+str(25 + i)
                logging.debug("panel.lowest_setting_for_thermal_output|Found for min %s/%s", str(30.0 + i), str(25 + i))
                return RetValue #this assumes that 'min' is providing also the smallest ThermalOutput of all settings (fanspeed).
            if Result['mid']>=ThermalOutput and 'mid' not in RetValue:
                RetValue['mid']=str(30.0 + i)+"/"+str(25 + i)
                logging.debug("panel.lowest_setting_for_thermal_output|Found for mid %s/%s", str(30.0 + i), str(25 + i))
            if Result['max'] >= ThermalOutput and 'max' not in RetValue:
                RetValue['max'] = str(30.0 + i)+"/"+str(25 + i)
                logging.debug("panel.lowest_setting_for_thermal_output|Found for max %s/%s", str(30.0 + i), str(25 + i))

        return RetValue

 def calculate_thermal_output1(self, Tzi, Tpi, Tii):
        # this function will calculate the Thermal Output for values Tz,Tp,Ti that are not included in the factory values

        #Check the values
        if (Tzi<=Tpi or Tii>Tpi or Tii>Tzi or Tii>30 or Tii<0 or Tzi<20 or Tpi<20):
            return None


        # TODO
        # We assume that the Tzi,Tpi,Tii values will be between two reference values
        # we want to find those values upper,low and calculate the nFactor for this range
        # this way we are calculating an nFactor value for the range that the requested values Tzi,Tpi,Tii are in
        # for example if we are asked to calculate the thermal output for 40/34/20 and we ares searching for the closest reference values that
        # the requested values are. Eg the reference values can be 40/30/20 and 40/35/20. We calculate the nFactor based on the range
        # 40/30/20 and 40/35/20
        Tout_low = {}
        Tout_up  = {}
        Deltas={}
        #Find the closest Tz,Tp,Ti values to the ones given by the factory
        thermaloutputenum=enumerate(self.ThermalOutput)
        for idx,(Tz,Tp,Ti,speed,tout) in thermaloutputenum:
            (Tz,Tp,Ti)=(Tz*1.0,Tp*1.0,Ti*1.0) #TODO fix this casting thingie
            delta=math.sqrt((Tzi-Tz)*(Tzi-Tz)+(Tpi-Tp)*(Tpi-Tp)+(Tii-Ti)*(Tii-Ti)) #Euclidian distance as metric
            Deltas[delta]=Tz,Tp,Ti
            #print ">",Tz,Tp,Ti,speed,tout
            #if (idx==0 or delta<mindelta ):
            #    mindelta=delta
            #    (lowTz,lowTp,lowTi,mspeed,mtout)=(Tz,Tp,Ti,speed,tout)

        #safecoding
        if(len(Deltas)<2):
            return None

        #TODO we need to find the "next best thing"
        #this is the closest value after the minimum
        (upTz,upTp,upTi)=Deltas[sorted(list(Deltas.keys()))[1]]
        (lowTz, lowTp, lowTi)=Deltas[sorted(list(Deltas.keys()))[0]]

        #Runnig once more to find all the outputs for all speeds
        #print "looking for",minTz,minTp,minTi
        for idx, (Tz, Tp, Ti, speed, tout) in enumerate(self.ThermalOutput):
            #logging.debug("idx=%d Tz=%f Tp=%f, Ti=%f, speed=%s, tout=%f",idx,Tz, Tp, Ti, speed, tout)
            if (Tz==lowTz and Ti==lowTi and Tp==lowTp):
                Tout_low[speed]=tout
            if (Tz==upTz and Ti==upTi and Tp==upTp):
                Tout_up[speed]=tout


        #Now that we have found the closest values to the required ones we can calculate the thermal Output
        #but in the case of fan coils we have to return three values on for every speed setting
        #in this case we have to run through the list again to find

        #print " Closet value",lowTz,lowTp,lowTi,Tout_low
        #print " Next value", upTz, upTp, upTi, Tout_up

        # Find the factory values that are closest to the the input triplet
        # (maybe the metric should be the distance in 3d Cartesian system)
        Ret={}
        for speed in Tout_low:
            #print speed
            n=self._nFactor(lowTz,lowTp,lowTi,upTz,upTp,upTi,Tout_up[speed],Tout_low[speed])
            #print n
            Ret[speed]=self._thermalOutput(Tzi, Tpi, Tii, lowTz,lowTp,lowTi, Tout_low[speed],n)
            #Ret[speed] = self._thermalOutput(Tzi, Tpi, Tii, lowTz, lowTp, lowTi, Tout_low[speed], n)

        return Ret


class InnovaRs600(FanCoilPanel):

    def __init__(self):
        self.model ="Innova-Rs600"
        #1337x579x131
        self.height=0.579
        self.depth=0.131
        self.length=1.137
        #the n dimesionless value depending on the geometry og the radiator
        #TODO for innova this is unknown, we can calculate but I am not sure if this is the correct approach
        #self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        self.ThermalOutput=[ ( 40 , 35 , 20 ,"min", 1.25),
                    ( 40 , 25 , 20 ,"min", 0.70),
                    ( 45 , 40 , 20 ,"min", 1.61),
                    ( 45 , 35 , 20 ,"min", 1.40),
                    ( 50 , 45 , 20 ,"min", 1.98),
                    ( 50 , 40 , 20 ,"min", 1.79),
                    ( 55 , 50 , 20 ,"min", 2.34),
                    ( 55 , 45 , 20 ,"min", 2.16),
                    ( 60 , 55 , 20 ,"min", 2.70),
                    ( 60 , 50 , 20 ,"min", 2.52),
                    ( 60 , 45 , 20 ,"min", 2.32),
                    ( 70 , 65 , 20 ,"min", 3.41),
                    ( 70 , 60 , 20 ,"min", 3.25),
                    ( 70 , 55 , 20 ,"min", 3.07),
                    ( 70 , 50 , 20 ,"min", 2.87),
                    ( 80 , 70 , 20 ,"min", 3.98),
                    ( 80 , 65 , 20 ,"min", 3.82),
                    ( 80 , 60 , 20 ,"min", 3.63),
                    ( 40 , 35 , 20 ,"mid", 1.88),
                    ( 40 , 25 , 20 ,"mid", 0.96),
                    ( 45 , 40 , 20 ,"mid", 2.43),
                    ( 45 , 35 , 20 ,"mid", 2.10),
                    ( 50 , 45 , 20 ,"mid", 2.98),
                    ( 50 , 40 , 20 ,"mid", 2.67),
                    ( 55 , 50 , 20 ,"mid", 3.52),
                    ( 55 , 45 , 20 ,"mid", 3.23),
                    ( 60 , 55 , 20 ,"mid", 4.06),
                    ( 60 , 50 , 20 ,"mid", 3.78),
                    ( 60 , 45 , 20 ,"mid", 3.48),
                    ( 70 , 65 , 20 ,"mid", 5.15),
                    ( 70 , 60 , 20 ,"mid", 4.89),
                    ( 70 , 55 , 20 ,"mid", 4.60),
                    ( 70 , 50 , 20 ,"mid", 4.28),
                    ( 80 , 70 , 20 ,"mid", 5.98),
                    ( 80 , 65 , 20 ,"mid", 5.71),
                    ( 80 , 60 , 20 ,"mid", 5.42),
                    ( 40 , 35 , 20 ,"max", 2.23),
                    ( 40 , 25 , 20 ,"max", 1.09),
                    ( 45 , 40 , 20 ,"max", 2.88),
                    ( 45 , 35 , 20 ,"max", 2.48),
                    ( 50 , 45 , 20 ,"max", 3.53),
                    ( 50 , 40 , 20 ,"max", 3.16),
                    ( 55 , 50 , 20 ,"max", 4.19),
                    ( 55 , 45 , 20 ,"max", 3.83),
                    ( 60 , 55 , 20 ,"max", 4.83),
                    ( 60 , 50 , 20 ,"max", 4.49),
                    ( 60 , 45 , 20 ,"max", 4.11),
                    ( 70 , 65 , 20 ,"max", 6.13),
                    ( 70 , 60 , 20 ,"max", 5.80),
                    ( 70 , 55 , 20 ,"max", 5.45),
                    ( 70 , 50 , 20 ,"max", 5.07),
                    ( 80 , 70 , 20 ,"max", 7.10),
                    ( 80 , 65 , 20 ,"max", 6.77),
                    ( 80 , 60 , 20 ,"max", 6.41),
                    ]





class InnovaRs800(FanCoilPanel):

    def __init__(self):
        self.model ="Innova-Rs800"
        #1337x579x131
        self.height=0.579
        self.depth=0.131
        self.length=1.337
        #the n dimesionless value depending on the geometry og the radiator
        #TODO for innova this is unknown, we can calculate but I am not sure if this is the correct approach
        #self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        self.ThermalOutput=[ ( 40 , 35 , 20 ,"min", 1.28),
                    ( 40 , 25 , 20 ,"min", 0.71),
                    ( 45 , 40 , 20 ,"min", 1.68),
                    ( 45 , 35 , 20 ,"min", 1.31),
                    ( 50 , 45 , 20 ,"min", 2.06),
                    ( 50 , 40 , 20 ,"min", 1.80),
                    ( 55 , 50 , 20 ,"min", 2.45),
                    ( 55 , 45 , 20 ,"min", 2.20),
                    ( 60 , 55 , 20 ,"min", 2.84),
                    ( 60 , 50 , 20 ,"min", 2.60),
                    ( 60 , 45 , 20 ,"min", 2.32),
                    ( 70 , 65 , 20 ,"min", 3.61),
                    ( 70 , 60 , 20 ,"min", 3.39),
                    ( 70 , 55 , 20 ,"min", 3.15),
                    ( 70 , 50 , 20 ,"min", 2.86),
                    ( 80 , 70 , 20 ,"min", 4.16),
                    ( 80 , 65 , 20 ,"min", 3.93),
                    ( 80 , 60 , 20 ,"min", 3.69),
                    ( 40 , 35 , 20 ,"mid", 2.00),
                    ( 40 , 25 , 20 ,"mid", 1.02),
                    ( 45 , 40 , 20 ,"mid", 2.60),
                    ( 45 , 35 , 20 ,"mid", 2.21),
                    ( 50 , 45 , 20 ,"mid", 3.19),
                    ( 50 , 40 , 20 ,"mid", 2.84),
                    ( 55 , 50 , 20 ,"mid", 3.78),
                    ( 55 , 45 , 20 ,"mid", 3.45),
                    ( 60 , 55 , 20 ,"mid", 4.38),
                    ( 60 , 50 , 20 ,"mid", 4.05),
                    ( 60 , 45 , 20 ,"mid", 3.69),
                    ( 70 , 65 , 20 ,"mid", 5.55),
                    ( 70 , 60 , 20 ,"mid", 5.25),
                    ( 70 , 55 , 20 ,"mid", 4.91),
                    ( 70 , 50 , 20 ,"mid", 4.55),
                    ( 80 , 70 , 20 ,"mid", 6.43),
                    ( 80 , 65 , 20 ,"mid", 6.12),
                    ( 80 , 60 , 20 ,"mid", 5.78),
                    ( 40 , 35 , 20 ,"max", 2.88),
                    ( 40 , 25 , 20 ,"max", 1.34),
                    ( 45 , 40 , 20 ,"max", 3.72),
                    ( 45 , 35 , 20 ,"max", 3.21),
                    ( 50 , 45 , 20 ,"max", 4.56),
                    ( 50 , 40 , 20 ,"max", 4.10),
                    ( 55 , 50 , 20 ,"max", 5.40),
                    ( 55 , 45 , 20 ,"max", 4.96),
                    ( 60 , 55 , 20 ,"max", 6.24),
                    ( 60 , 50 , 20 ,"max", 5.82),
                    ( 60 , 45 , 20 ,"max", 5.33),
                    ( 70 , 65 , 20 ,"max", 7.90),
                    ( 70 , 60 , 20 ,"max", 7.50),
                    ( 70 , 55 , 20 ,"max", 7.06),
                    ( 70 , 50 , 20 ,"max", 6.58),
                    ( 80 , 70 , 20 ,"max", 9.18),
                    ( 80 , 65 , 20 ,"max", 8.77),
                    ( 80 , 60 , 20 ,"max", 8.32)]












class InnovaRs1000(FanCoilPanel):

    def __init__(self):
        self.model ="Innova-Rs1000"
        #1537x579x131
        self.height=0.579
        self.depth=0.131
        self.length=1.537
        #the n dimesionless value depending on the geometry og the radiator
        #TODO for innova this is unknown, we can calculate but I am not sure if this is the correct approach
        #self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        self.ThermalOutput=[( 40 , 35 , 20 ,"min", 2.34),
                    ( 40 , 25 , 20 ,"min", 1.23),
                    ( 45 , 40 , 20 ,"min", 3.01),
                    ( 45 , 35 , 20 ,"min", 2.64),
                    ( 50 , 45 , 20 ,"min", 3.68),
                    ( 50 , 40 , 20 ,"min", 3.35),
                    ( 55 , 50 , 20 ,"min", 4.35),
                    ( 55 , 45 , 20 ,"min", 4.05),
                    ( 60 , 55 , 20 ,"min", 5.02),
                    ( 60 , 50 , 20 ,"min", 4.73),
                    ( 60 , 45 , 20 ,"min", 4.38),
                    ( 70 , 65 , 20 ,"min", 6.34),
                    ( 70 , 60 , 20 ,"min", 6.08),
                    ( 70 , 55 , 20 ,"min", 5.78),
                    ( 70 , 50 , 20 ,"min", 5.42),
                    ( 80 , 70 , 20 ,"min", 7.41),
                    ( 80 , 65 , 20 ,"min", 7.14),
                    ( 80 , 60 , 20 ,"min", 6.83),
                    ( 40 , 35 , 20 ,"mid", 2.65),
                    ( 40 , 25 , 20 ,"mid", 1.32),
                    ( 45 , 40 , 20 ,"mid", 3.42),
                    ( 45 , 35 , 20 ,"mid", 2.98),
                    ( 50 , 45 , 20 ,"mid", 4.17),
                    ( 50 , 40 , 20 ,"mid", 3.79),
                    ( 55 , 50 , 20 ,"mid", 4.93),
                    ( 55 , 45 , 20 ,"mid", 4.57),
                    ( 60 , 55 , 20 ,"mid", 5.68),
                    ( 60 , 50 , 20 ,"mid", 5.35),
                    ( 60 , 45 , 20 ,"mid", 4.95),
                    ( 70 , 65 , 20 ,"mid", 7.19),
                    ( 70 , 60 , 20 ,"mid", 6.88),
                    ( 70 , 55 , 20 ,"mid", 6.53),
                    ( 70 , 50 , 20 ,"mid", 6.12),
                    ( 80 , 70 , 20 ,"mid", 8.40),
                    ( 80 , 65 , 20 ,"mid", 8.07),
                    ( 80 , 60 , 20 ,"mid", 7.71),
                    ( 40 , 35 , 20 ,"max", 3.30),
                    ( 40 , 25 , 20 ,"max", 1.52),
                    ( 45 , 40 , 20 ,"max", 4.26),
                    ( 45 , 35 , 20 ,"max", 3.71),
                    ( 50 , 45 , 20 ,"max", 5.23),
                    ( 50 , 40 , 20 ,"max", 4.72),
                    ( 55 , 50 , 20 ,"max", 6.18),
                    ( 55 , 45 , 20 ,"max", 5.70),
                    ( 60 , 55 , 20 ,"max", 7.12),
                    ( 60 , 50 , 20 ,"max", 6.68),
                    ( 60 , 45 , 20 ,"max", 6.15),
                    ( 70 , 65 , 20 ,"max", 9.01),
                    ( 70 , 60 , 20 ,"max", 8.60),
                    ( 70 , 55 , 20 ,"max", 8.12),
                    ( 70 , 50 , 20 ,"max", 7.60),
                    ( 80 , 70 , 20 ,"max", 10.56),
                    ( 80 , 65 , 20 ,"max", 10.07),
                    ( 80 , 60 , 20 ,"max", 9.59),
                    ]



class AermecUL36(FanCoilPanel):

    def __init__(self):
        self.model ="AermecUL36"
        self.height=0.606
        self.depth=0.173
        self.length=1.200
        #the n dimesionless value depending on the geometry og the radiator
        #self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        self.ThermalOutput=[(70,60 ,20 ,"max", 5.76),
                            (70, 60, 20, "mid", 4.87),
                            (70, 60, 20, "min", 3.53),
                            (50, 40, 20, "max", 3.54),
                            (40, 30, 20, "max", 1.94),
                            (60, 50, 20, "max", 4.66),
                            (50, 40, 20, "mid", 2.90),
                            (40, 30, 20, "mid", 1.59),
                            (60, 50, 20, "mid", 3.82),
                            (50, 40, 20, "min", 2.08),
                            (40, 30, 20, "min", 1.14),
                            (60, 50, 20, "min", 2.74),
                            ]



class GalletiEstro12(FanCoilPanel):

    def __init__(self):
        self.model ="GalletiEstro12"
        self.height=0.564
        self.depth=0.251
        self.length=1.614
        #the n dimesionless value depending on the geometry og the radiator
        #self.n=n
        #Holds the factory Thermal output that the manufacturer is providing, as a function of Tz,Tpi,!ii
        #TODO for this fancoil the 50/40 is the Eurovent value. I dont understand this value is exactly the 40 part is
        #an assumption.
        #self.ThermalOutput=[(50, 40, 20, "max", 3.54),
        #                    (50, 40, 20, "mid", 2.90),
        #                   (50, 40, 20, "min", 2.08),
        #                    (70, 60, 20, "max", 11.50),
        #                    (70, 60, 20, "mid", 3.08),
        #                    (70, 60, 20, "min", 1.70),
        #                    (50, 40, 20, "max", 3.54),
        #                    (50, 40, 20, "mid", 2.90),
        #                    (50, 40, 20, "min", 2.08),
        #                    ]
        self.ThermalOutput = [(50, 40, 20, "max",13.560),
                              (50, 40, 20, "mid", 10.400),
                              (50, 40, 20, "min", 8.360),
                              (70, 60, 20, "max", 24.670),
                              (70, 60, 20, "mid", 18.750),
                              (70, 60, 20, "min", 15.02),
                              (60, 50, 20, "max", 19.15),
                              (60, 50, 20, "mid", 14.61),
                              (60, 50, 20, "min", 11.75),
                              (45, 40, 20, "max", 12.21),
                              (45, 40, 20, "mid", 9.29),
                              (45, 40, 20, "min", 7.45),
                            ]
