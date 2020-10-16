import os
import processing
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *


# boite de dialogue FSC
qfd=QFileDialog()

# boite de dialogue altitude de laneige
qid=QInputDialog()
qidTitre="Limite d'enneigement"
qidlabel="Determiner visuellement la limite d'enneigement en multiple de 100"
qidmode =QLineEdit.Normal
qiddefault ='2000'
resumesurf=''
txtsurf=''
surftot=0
#liste des couches chargees
root=QgsProject.instance().layerTreeRoot()

# titre de la boite de dialogue recherche epertoire FSC (fractional snow cover)
title='ouvrir un fichierraster FSC'

# repertoire parent des fichiers FSC
path="/home/knobuntu/QGis/FSC"


# repertoire de ravail
travail ="/home/knobuntu/QGis/travail/"

# le fichier elevation ( les espaces correspondent au tiret du bas
demalti="/home/knobuntu/QGis/alti/dem_alpes_lambert.tif"


# le repertoire des bassins versants
pathbassin="/home/knobuntu/QGis/bassinsversants/"

# repertoire de calcul des DEM superieurs a une altitude par pas de 100m precalcules avec demaltipoly.py
polyalti100="/home/knobuntu/QGis/alti/polyalti100/" 

#le format du fichier est polyalti100+ "demalpes"+limiteenneigement+".tif" exemple demalpes1800.tif
ficsurface=pathbassin+'surfnuage.txt'

# repertoire des fichiers FSC en partant du repertoire path
chemin=QFileDialog.getExistingDirectory(qfd, 'Selection du repertoire',path)


#liste des fichiers FSC dans le repertoire chemin
listedir=os.listdir(chemin)

#=============================================effacer le repertoire travail==================
liste=os.listdir(travail)
for fic in liste :
    fichier=os.path.join(travail,fic)
    os.remove(fichier)


#desactiver les vecteur surfaceneigebassin
for layer in QgsProject.instance().mapLayers().values():
    couchename= layer.name()
    x = couchename.find ('lambert')
    if x >-1 :                
        QgsProject.instance().layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False) 
    x=couchename .find('dem')
    if x> -1:
        iface.setActiveLayer(layer)
        print (couchename)    




# ============================boucle sur les  fichiers FSC  du reprtoire chemin ================
for fic in listedir:
    longueur=len(fic)
    fsc=fic[0:3]
   
    if (longueur==15) and (fsc=="FSC"):
        print (fic)
        chaine=fic[3:11]
        print (chaine)
        
        liste=fic.split('.')
        fsc=liste[0]
        liste= fsc.split('FSC')
        datefsc=liste[1]
        #fscusuel="FSC"+ datefsc +".tif"
        f=os.path.join(chemin,fic)

        #fichier FSC converti en lambert
        fsclambert =travail+'lambert'+fscusuel 
        fsclambertusuel='lambertFSC'+datefsc
        parametres={ 'DATA_TYPE' : 0, 'EXTRA' : '',
        'INPUT' : f, 'MULTITHREADING' : False, 'NODATA' : None, 'OPTIONS' : '', 'OUTPUT' : fsclambert, 'RESAMPLING' : 0, 'SOURCE_CRS' : None, 'TARGET_CRS' : QgsCoordinateReferenceSystem('EPSG:2154'), 'TARGET_EXTENT' : None, 'TARGET_EXTENT_CRS' : None, 'TARGET_RESOLUTION' : None }  
        resultat=processing.run('gdal:warpreproject',parametres)

        fsclambertcouche= iface.addRasterLayer(f,fsclambertusuel)

        #chargement du fichier stylefsc.qml des distinction des couches de neige
        fsclambertcouche.loadNamedStyle('/home/knobuntu/QGis/styles/stylefsc.qml')
        
        fsclambertcouche.triggerRepaint()

 
 
 
        
     #   fscusuelnuage="FSCnuage"+ datefsc +".tif"
     #   fscusuelneige="FSCneige"+ datefsc +".tif"
  
    # =============liste des bassins a traiter =============================

        bassins=['bassinDurance','bassinRomanche','bassinIsere']      
        bassinscourt=['Durance','Romanche','Isere']
    #=============
        f=os.path.join(chemin,fic)
        
        print (fscusuel)
        print (chemin)
        print (fic)
        #====================  bouclebassin ====================
        nbbassin=-1
        for bassin in bassins:
            nbbassin=nbbassin+1
            bassincourt=bassinscourt[nbbassin]
            bassinlong=pathbassin + bassin+".shp"
            #bassin="bassinTinee" #nomusuel du bassin 

            bassindate=bassincourt+datefsc


            #========================================#polygonisation des altitudes=======================
            vuebassin = QgsProject.instance().mapLayersByName(bassin)[0]
            vuebassin.updateExtents()
            canvas=iface.mapCanvas()
            canvas.setExtent(vuebassin.extent())
            canvas.refresh()
            #delimitation de la limite neige
            limiteneige, ok = QInputDialog.getText(qid, qidTitre, qidlabel, qidmode, qiddefault)
            print (limiteneige)
            #intlimit=int(limiteneige)
           
                
            
            alti100=polyalti100 + "demalpes"+limiteneige+".tif"
            #layer= iface.addRasterLayer(alti100,"alti100")
            
            polyalti=travail+'polyalti'+bassin+limiteneige+'.shp'
            polyaltiusuel='polyalti'+bassin+limiteneige
            polygonise=travail+'polygonise'+bassin+limiteneige+'.shp'
            extraction=travail+'extraction'+bassin+limiteneige+'.shp'
            simplifie=travail+'simplifie'+bassin+limiteneige+'.shp'
            
            ##decoupe=output raster
            ##elevation=output vector
            parametres={ 'ALPHA_BAND' : False, 'CROP_TO_CUTLINE' : True, 'DATA_TYPE' : 0, 'EXTRA' : '', 'INPUT' : alti100, 'KEEP_RESOLUTION' : False, 'MASK' : bassinlong, 'MULTITHREADING' : False, 'NODATA' : None, 'OPTIONS' : '', 'OUTPUT' : 'TEMPORARY_OUTPUT', 'SET_RESOLUTION' : False, 'SOURCE_CRS' : None, 'TARGET_CRS' : None, 'X_RESOLUTION' : None, 'Y_RESOLUTION' : None }
            decoupealti100=processing.run('gdal:cliprasterbymasklayer',parametres)
            # outputs_GDALOGRCLIPRASTERBYMASKLAYER_2=processing.runalg('gdalogr:cliprasterbymasklayer', demalti,bassin,'0',False,True,True,5,4,75.0,6.0,1.0,False,0,False,None,None)
 
            parametres={ 'BAND' : 1, 'EIGHT_CONNECTEDNESS' :False, 'EXTRA' : '', 'FIELD' : 'ELEVATION', 'INPUT' : decoupealti100['OUTPUT'], 'OUTPUT' :polygonise }
            polygonizedecoupealti100=processing.run('gdal:polygonize',parametres)
            #outputs_GDALOGRPOLYGONIZE_2=processing.runalg('gdalogr:polygonize', outputs_GDALOGRCLIPRASTERBYMASKLAYER_2['OUTPUT'],'ELEVATION',None)

            
            parametres={ 'FIELD' : 'ELEVATION', 'INPUT' : polygonise, 'OPERATOR' : 2, 'OUTPUT' :extraction, 'VALUE' : '0' }
            polygonizealti=processing.run('native:extractbyattribute',parametres)
            #outputs_QGISEXTRACTBYATTRIBUTE_2=processing.runalg('qgis:extractbyattribute', outputs_GDALOGRPOLYGONIZE_2['OUTPUT'],'ELEVATION',2,'0',polyalti)
  
            # simplification de la limite
            parametres={ 'INPUT' : extraction, 'METHOD' : 0, 'OUTPUT' : simplifie, 'TOLERANCE' : 40 }
            multipolyalti=processing.run('native:simplifygeometries',parametres)
            
            parametres={ 'FIELD' : 'ELEVATION', 'INPUT' : simplifie, 'OUTPUT' : polyalti }
            resultat=processing.run('gdal:dissolve',parametres)   
  
 
 
            #================Nuages sur neige=====================
      
            """ Pour calculer la surface de la neige masquée par des nuages 
                  on construit le raster obtenu par la decoupe du FSC de la Durance par le vecteur polyalti du bassin
            """
            
            # decoupe du raster fsc aux dimensions polyalti
           
            nuageNeigeBassin= travail+'nuageNeigeBassin'+bassindate+'.tif'
            print (nuageNeigeBassin)
            nuageNeigeBassinUsuel='nuageNeigeBassin'+bassindate
            parametres={ 'ALPHA_BAND' : False, 'CROP_TO_CUTLINE' : True, 'DATA_TYPE' : 0, 'EXTRA' : '', 'INPUT' : fsclambert, 'KEEP_RESOLUTION' : False, 'MASK' : polyalti, 'MULTITHREADING' : False, 'NODATA' : None, 'OPTIONS' : '', 'OUTPUT' : nuageNeigeBassin, 'SET_RESOLUTION' : False, 'SOURCE_CRS' : None, 'TARGET_CRS' : None, 'X_RESOLUTION' : None, 'Y_RESOLUTION' : None }
            resultat=processing.runAndLoadResults('gdal:cliprasterbymasklayer',parametres)          
            
            # ========================calcul des surfaces de neige masqués par nuages========================
 
            nuageNeige=QgsProject.instance().mapLayersByName(nuageNeigeBassinUsuel)[0]
            print(nuageNeige.name())

            nbXCells=nuageNeige.width()
            nbYCells=nuageNeige.height()
            etendue=nuageNeige.extent()

            print (nuageNeige.width(),nuageNeige.height())
            print (nuageNeige.extent())
            res=nuageNeige.dataProvider().sample(QgsPointXY(973161,6423521),1)
            print( res[0])
            largeurCell=etendue.width()/nbXCells
            hauteurCell=etendue.height()/nbYCells
            print (largeurCell)
            compteur=0
            for i in range(nbXCells):
                x=etendue.xMinimum()+i*largeurCell+1
                for j in range (nbYCells):
                    y=etendue.yMinimum()+j*hauteurCell+1
                    res=nuageNeige.dataProvider().sample(QgsPointXY(x,y),1)[0]
                    if res==30:
                        compteur += 1

            surfacenuageneige= int(compteur*largeurCell*hauteurCell/1000000)
            print ("surface neige nuage : ", surfacenuageneige)

            """
            #ecriture des surfaces dans polyaltiusuel
            polysurfaceneigenuage=QgsProject.instance().mapLayersByName(polyaltiusuel)[0]
            features=polysurfaceneigenuage.getFeatures()
            for feature in features:
                caps=polysurfaceneigenuage.dataProvider().capabilities()
                if caps & QgsVectorDataProvider.AddAttributes:
                    champs=polysurfaceneigenuage.fields()
                    if champs.indexFromName("SNeigeNuag") == -1:
                        res=polysurfaceneigenuage.dataProvider().addAttributes(
                        [QgsField("SNeigeNuag",QVariant.Int)])
                        polysurfaceneigenuage.updateFields()
                    attr={1:surfacenuageneige}
                    polysurfaceneigenuage.dataProvider().changeAttributeValues({ 0 : attr })
       

            """
        
            #---------===========================----traitement neige visible------------------------------

            
            # decoupe du raster fsclambert aux dimensions du bassin (bassinlong)
           
            neigeBassin= travail+'neigeBassin'+bassindate+'.tif'
            neigeBassinUsuel='neigeBassin'+bassindate
            parametres={ 'ALPHA_BAND' : False, 'CROP_TO_CUTLINE' : True, 'DATA_TYPE' : 0, 'EXTRA' : '', 'INPUT' : fsclambert, 'KEEP_RESOLUTION' : False, 'MASK' : bassinlong, 'MULTITHREADING' : False, 'NODATA' : None, 'OPTIONS' : '', 'OUTPUT' : neigeBassin, 'SET_RESOLUTION' : False, 'SOURCE_CRS' : None, 'TARGET_CRS' : None, 'X_RESOLUTION' : None, 'Y_RESOLUTION' : None }
            resultat=processing.runAndLoadResults('gdal:cliprasterbymasklayer',parametres)          
            
            # ========================calcul des surfaces de neige masqués par nuages========================
 
            neigeVisible=QgsProject.instance().mapLayersByName(neigeBassinUsuel)[0]
            print(neigeVisible.name())

            nbXCells=neigeVisible.width()
            nbYCells=neigeVisible.height()
            etendue=neigeVisible.extent()

            print (neigeVisible.width(),neigeVisible.height())
            print (neigeVisible.extent())
            largeurCell=etendue.width()/nbXCells
            hauteurCell=etendue.height()/nbYCells
            print (largeurCell)
            compteur=0
            for i in range(nbXCells):
                x=etendue.xMinimum()+i*largeurCell+1
                for j in range (nbYCells):
                    y=etendue.yMinimum()+j*hauteurCell+1
                    res=neigeVisible.dataProvider().sample(QgsPointXY(x,y),1)[0]
                    if res==82:
                        compteur += 1
                    if res>99:
                        compteur += 1
            surfaceneigeVisible= int(compteur*largeurCell*hauteurCell/1000000)
            print ("surface neige visible : ", surfaceneigeVisible)

            """
            #ecriture des surfaces dans polyaltiusuel
            polysurfaceneige=QgsProject.instance().mapLayersByName(polyaltiusuel)[0]
            features=polysurfaceneige.getFeatures()
            for feature in features:
            caps=polysurfaceneige.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddAttributes:
            champs=polysurfaceneige.fields()
            if champs.indexFromName("SNeigeVisi") == -1:
            res=polysurfaceneigenuage.dataProvider().addAttributes(
            [QgsField("SNeigeVisi",QVariant.Int)])
            polysurfaceneige.updateFields()
            attr={2:surfaceneigeVisible}
            polysurfaceneige.dataProvider().changeAttributeValues({ 0 : attr })
 
            """
            #ecriture des surfaces
            surfaceTotale = surfacenuageneige +surfaceneigeVisible
            txtsurf="{0} neige nuage {1} neige visible {2} total neige {3}\n".format(bassindate,surfacenuageneige,surfaceneigeVisible,surfaceTotale)
            print (txtsurf)
            
            fichier=open (ficsurface,"a")
            fichier.write(txtsurf)
            fichier.close
            
            #effacement nuageNeigeBassin et neigeBassin
            
            for layer in QgsProject.instance().mapLayers().values():
                
                couchename= layer.name()   
                x = couchename.find ('nuageNeige')
                if x>-1:
                    QgsProject.instance().removeMapLayers([layer.id()])
                x = couchename.find ('neigeBassin')
                if x>-1:
                    QgsProject.instance().removeMapLayer(layer.id())
                
            
            #fin boucle bassin       
            
    QgsProject.instance().removeMapLayer(fsclambertcouche.id())
w=QWidget()
info="operation terminee "+ bassin
QMessageBox.information(w, info,"Le resume des surfaces est dans le fichier surfaceneige dans le repertoire defini comme bassinsversant ")    
#fin
