#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:34:30 2018

@author: federico
"""

import sys 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy import stats
import scipy.stats as ss
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import levene
from scipy.stats import shapiro
import traceback
from datetime import datetime
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import pathlib
import os
from PyQt5 import uic, QtWidgets 


qtCreatorFile = "morita.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) 

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow): 
    def __init__(self): 
        QtWidgets.QMainWindow.__init__(self) 
        Ui_MainWindow.__init__(self) 
        self.setupUi(self) 
               
        self.importar.clicked.connect(self.getxls)
        self.analizar.clicked.connect(self.plot1)
        self.analizar.clicked.connect(self.reporte)
        self.analizar.clicked.connect(self.progreso)
        
        print("Morita 1.0")

    def getxls(self): 
        if self.seleccionar != "":
            self.seleccionar.clear()
            self.independiente.clear()
            self.dependiente.clear()
            self.condicion.clear()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file') 
        if filePath != "": 
            self.datos = pd.ExcelFile(str(filePath))
            self.seleccionar.addItems(list(self.datos.sheet_names))
            self.cargar.clicked.connect(self.carga)
            
            pat = str(filePath)
        
            print('Archivo .xlsx cargado exitosamente.')
            print('----------------------------------------------')
            
            inic = "MORITA 1.0"
            sepa= "-------------------------------------------------------------------"
            
            tesla = inic + '\n\n' + sepa + '\n\n' + "Archivo  -- " + pat +  " -- cargado exitosamente." + '\n\n' + sepa + '\n\n' 
          
            self.resultado.setText(tesla)
        
        
    def carga (self):
        if self.independiente != "":
            
            self.independiente.clear()
            self.dependiente.clear()
            self.condicion.clear()      
            self.df=self.datos.parse(self.seleccionar.currentText())  
            self.independiente.addItems(list(self.df.columns.values))
            self.dependiente.addItems(list(self.df.columns.values))
            self.condicion.addItems(list(self.df.columns.values))
            
            hoj = str(self.seleccionar.currentText())
            
            inic = "MORITA 1.0"
            sepa= "-------------------------------------------------------------------"
            
            tesla = inic + '\n\n' + sepa + '\n\n' + "Página -- " + hoj + " -- seleccionada exitosamente." + '\n\n' + sepa + '\n\n'
            
            self.resultado.setText(tesla)
            
            self.barra.setValue(0)
            
        if self.independiente == "":

            self.df=self.datos.parse(self.seleccionar.currentText())  
            self.independiente.addItems(list(self.df.columns.values))
            self.dependiente.addItems(list(self.df.columns.values))
            self.condicion.addItems(list(self.df.columns.values))
            
            hoj = str(self.seleccionar.currentText())
            
            inic = "MORITA 1.0"
            sepa= "-------------------------------------------------------------------"
            
            tesla = inic + '\n\n' + sepa + '\n\n' + "Página -- " + hoj + " -- seleccionada exitosamente." + '\n\n' + sepa + '\n\n'
            
            self.resultado.setText(tesla)   
                  
        
    def progreso (self):            
        self.completed = 0
        
        while self.completed < 100 :
            self.completed += 0.0001
            self.barra.setValue(self.completed)
        
         
    def plot1 (self): 
        self.df=self.datos.parse(self.seleccionar.currentText())
        A=self.df[str(self.independiente.currentText())]
        B=self.df[str(self.dependiente.currentText())]
        C=self.df[str(self.condicion.currentText())]
        

        
        sns.set_style("darkgrid")       
        f, axes = plt.subplots(2, 2)    
        sns.barplot(x=A, y=B, hue=C, palette="bright",orient='v' , ax=axes[0,0])
        sns.boxplot(x=A, y=B, hue=C, palette="bright", orient='v' , ax=axes[0,1]) 
        sns.violinplot(x=A, y=B, hue=C, palette="bright", orient='v' , ax=axes[1,0])
        sns.stripplot(x=A, y=B, hue=C, palette="bright", orient='v' , ax=axes[1,1], jitter=True)
        
        
        f.patch.set_facecolor('darkgrey')
        plt.show()       
        print('----------------------------------------------')     
        print('Graficos generados exitosamente.')
        
      
        
    def reporte(self): 
        
        self.df1=self.datos.parse(self.seleccionar.currentText())          
        depe = str(self.dependiente.currentText())
        indepe = str(self.independiente.currentText())
        condi = str(self.condicion.currentText())
        
        try:
            inicio_st = str(depe + '~'  + indepe + '+' + condi + '+' + indepe + ':' + condi)        
            formula = inicio_st
            model = ols(formula, self.df1).fit()
            aov_table = anova_lm(model, typ=2)     
            anova2 = str(aov_table)
            
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            anova2 = "Los datos ingresados no son compatibles con los requisitos necesarios para generar el test de ANOVA DE DOS VIAS"
    
        lista = []
        kru = []
        tuk = []
        lev = []
        bart=[]

        try: 
            for name_group in self.df.groupby(indepe):
                samples = [PRUEBA[1] for PRUEBA in name_group[1].groupby(condi)[depe]]
                f_val, p_val = ss.f_oneway(*samples)           
                lista.append('Variable independiente: {}, F value: {:.4f}, p value: {:.4f}'.format(name_group[0], f_val, p_val))
                lista1 = '\n'.join(lista)
                lista2=str(lista1) 
                
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            lista2 = "error anova1"
        
        try:
            for name_group in self.df.groupby(indepe):
                samples1 = [PRUEBA[1] for PRUEBA in name_group[1].groupby(condi)[depe]]
                krus = ('Variable independiente: {}'.format(name_group[0])) + '\n' + str (stats.kruskal(*samples1))              
                kru.append(str(krus))
                kru1='\n\n'.join(kru)
            
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())
            kru1 = "error krustal"            
            
        try:
            for name, grouped_df in self.df.groupby(indepe):
                tu = ('Variable independiente: {}'.format(name)) + '\n' + str(pairwise_tukeyhsd(grouped_df[depe], grouped_df[condi]))
                tuk.append(tu)
                tuk1='\n\n'.join(tuk)
                
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc())   
            tuk1="error tuckey"
      
        try:
            for name_group in self.df.groupby(indepe):
                samples1 = [PRUEBA[1] for PRUEBA in name_group[1].groupby(condi)[depe]]
                leve = ('Variable independiente: {}'.format(name_group[0])) + '\n' + str (levene(*samples1))          
                lev.append(str(leve))
                leve1='\n\n'.join(lev)
                
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc()) 
            leve1="error tuk"
            
        try:
            for name_group in self.df.groupby(indepe):
                samples1 = [PRUEBA[1] for PRUEBA in name_group[1].groupby(condi)[depe]]
                bar = ('Variable independiente: {}'.format(name_group[0])) + '\n' + str (stats.bartlett(*samples1))              
                bart.append(str(bar))
                bart1='\n\n'.join(bart)
              
        except Exception as e:
            print("type error: " + str(e))
            print(traceback.format_exc()) 
            bart1="error bart"           
            
        pd.set_option('display.max_rows', 3500)         
        pd.set_option('display.max_columns', 3500)    
        grouped = self.df.groupby([indepe, condi])        
        shape = str(grouped[depe].apply(lambda x: shapiro(x)))      
        tes = str(grouped[depe].apply(lambda x: x.describe()))
        
        todo =self.df1[[indepe, condi, depe]]
        
        yes = str(todo)           
        
        separador1_st = "---------------------------------------------------------------------------" 
          
        resum_st = "TABLA RESUMEN" + '\n\n' + yes + '\n\n'
        descriptiva_st = "ESTADISTICA DESCRIPTIVA" + '\n\n' + tes + '\n\n'
        anova_st = "ANOVA DE UNA VIA" + '\n\n' + lista2 + '\n\n'    
        kru1_st = "TEST DE KRUSKAL - WALLIS" + '\n\n' + kru1 + '\n\n'    
        tukey_st = "TEST DE TUKEY HSD" + '\n\n' + tuk1 + '\n\n'    
        anova2_st = "ANOVA DE DOS VIAS" + '\n\n' + anova2 + '\n\n'   
        levene_st = "TEST DE LEVENE" + '\n\n' + leve1 + '\n\n'+ separador1_st + '\n' + "TEST DE BARTLETT" + '\n\n'  + bart1 +'\n\n'            
        shapiro_st = "TEST DE NORMALIDAD" + '\n\n' + shape + '\n\n'
               
        resumen_st = separador1_st + '\n' + resum_st + separador1_st + '\n'+ descriptiva_st + separador1_st + '\n'+ anova_st + separador1_st + '\n' +kru1_st + separador1_st + '\n' + tukey_st + separador1_st + '\n'+ anova2_st + separador1_st + '\n'+ levene_st + separador1_st + '\n'+ shapiro_st + separador1_st  
        
        cabecera = "Morita 1.0"
        tit= separador1_st + '\n\n'+ "TITULO: " + '\n\n' + "SUBTITULO: " + '\n\n' 
        hoy = "FECHA: " + str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        nombre = "Informe " + str(datetime.now().strftime('%d%m%Y %H%M%S'))
                                
        pathlib.Path(nombre).write_text(cabecera + '\n' + tit + hoy + '\n\n' +resumen_st)
        
        inic = "MORITA 1.0"
        sepa= "-------------------------------------------------------------------"
        
        direc= str(os.getcwd())
        
        tesla = inic + '\n\n' + sepa + '\n\n' + "Informe generado exitosamente." + '\n'  + "Directorio de almacenamiento: " + '\n\n'  + direc + '\n\n' + sepa + '\n\n' 
        
        self.resultado.setText(tesla)
        
        print('----------------------------------------------')     
        print('Informe generados exitosamente.')
        
      
        
if __name__ == "__main__": 
            app = QtWidgets.QApplication(sys.argv) 
            window = MyApp() 
            window.show() 
            app.exec_()
            
