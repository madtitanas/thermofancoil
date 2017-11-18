from HeatingPanels import Panel
import logging





#this is a test
def filterPlan(Plan,PanelList):
    return None



def implementPlan(Plan,PanelList):

    #TODO don;t like this part here
    MaxWaterInTemp = 90
    Panelplan={}


    #parse general rooms (under "All" key)
    if 'All' in Plan and 'limitation' in Plan['All']:
        if 'MaxWaterInTemp' in Plan['All']['limitation']:
            MaxWaterInTemp = Plan['All']['limitation']['MaxWaterInTemp']




    for room in Plan:
        #print room

        if room=="All":
            continue

        length_limit, depth_limit, height_limit = (None, None, None)  # reset the limitation on every loop
        if 'thermal-need' not in Plan[room] and room!="All":
            print "Invalid Plan, Thermal need is missing for ", room
            return
        need = Plan[room]['thermal-need']




        if 'limitation' in Plan[room]:
            if 'length' in Plan[room]['limitation']:
                length_limit = Plan[room]['limitation']['length']
                logging.debug("Length limit for room %s is at %s", room, length_limit)
            if 'depth' in Plan[room]['limitation']:
                depth_limit = Plan[room]['limitation']['depth']
                logging.debug("depth limit for room %s is at %s", room, depth_limit)
            if 'height' in Plan[room]['limitation']:
                height_limit = Plan[room]['limitation']['height']
                logging.debug("height limit for room %s is at %s", room, height_limit)



        Kati={}
        for panel in PanelList:
            logging.debug("checking panel %s for fitting", panel.model)
            if length_limit is not None and panel.length > length_limit or depth_limit is not None and panel.depth > depth_limit or height_limit is not None and panel.heigth > height_limit:
                logging.debug("panel %s does not fit: h=%s l=%s d=%s ", panel.model, repr(panel.height), repr(panel.length),
                              repr(panel.depth))
                pass
            else:
                setting=panel.lowest_setting_for_thermal_output(need,MaxWaterInTemp)
                if setting!={}:
                    Kati.update({panel.model:setting})
                #panel.model + " : " + repr(panel.lowest_setting_for_thermal_output(need)))
        Panelplan[room]=Kati


    return Panelplan


def main():


    logging.info('Started')
    rs600=Panel.InnovaRs600()
    rs800=Panel.InnovaRs800()
    rs1000=Panel.InnovaRs1000()
    ul36=Panel.AermecUL36()
    estro=Panel.GalletiEstro12()



    PanelList=[]
    PanelList.append(rs800)
    PanelList.append(rs600)
    PanelList.append(rs1000)
    PanelList.append(ul36)
    PanelList.append(estro)

    Plan = {"Kitchen": {'thermal-need': 3.81, 'limitation': {'length': 2.0}},
            "Bedroom ours": {'thermal-need': 2.57, 'limitation': {'length': 1.19}},
            "Laundry": {'thermal-need': 2.14,'limitation': {'length': 2.0}},
            "Bedroom 2": {'thermal-need': 3.81, 'limitation': {'length': 2.0}},
            "Hall": {'thermal-need': 2.14, 'limitation': {'length': 1.19}},
            "LivingRoom W": {'thermal-need': 2.13,'limitation': {'length': 2.0}},
            "LivingRoom E": {'thermal-need': 2.13,'limitation': {'length': 1.19}},
            "All":{'limitation':{'MaxWaterInTemp':55}}
            }




    for room in implementPlan(Plan,PanelList):
            print room,implementPlan(Plan,PanelList)[room]

    logging.info('Finished')


if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s|%(levelname)s|%(message)s',filename='thermal.log', level=logging.DEBUG)


    main()