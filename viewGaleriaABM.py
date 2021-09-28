#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import re
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from os import remove

class GaleriaFrame(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        #-----------------COMIENZO DE CAMPOS-----------------------
        self.miFrame = Frame(self, width=350, height=400)
        self.miFrame.pack()

        self.datacuadroNombre = StringVar()
        self.datacuadroApellido = StringVar()
        self.datacuadroRubro = StringVar()
        self.datacuadroFacturacion = StringVar()
        self.datacuadroNuevoNombre = StringVar()

        self.value = StringVar()
        self.value.set(str(self.calcularFacturaTotal()))

        self.cuadroNombre = Entry(self.miFrame, textvariable=self.datacuadroNombre)
        self.cuadroNombre.grid(row=1, column=1, padx=10, pady=1,columnspan=3)
        self.cuadroNombre.config(justify="center")

        self.cuadroApellido = Entry(self.miFrame, textvariable=self.datacuadroApellido)
        self.cuadroApellido.grid(row=2, column=1, padx=10, pady=10,columnspan=3)
        self.cuadroApellido.config(justify="center")

        self.cuadroRubro = Entry(self.miFrame, textvariable=self.datacuadroRubro)
        self.cuadroRubro.grid(row=1, column=5, padx=10, pady=10,columnspan=3)
        self.cuadroRubro.config(justify="center")

        self.cuadroFacturacion = Entry(self.miFrame, textvariable=self.datacuadroFacturacion)
        self.cuadroFacturacion.grid(row=2, column=5, padx=10, pady=10,columnspan=3)
        self.cuadroFacturacion.config(justify="center")

        #-----------------COMIENZO DE ETIQUETAS-----------------------

        self.NombreLabel = Label(self.miFrame, text="Nombre: ")
        self.NombreLabel.grid(row=1, column=0, padx=10, pady=10)

        self.ApellidoLabel = Label(self.miFrame, text="Apellido: ")
        self.ApellidoLabel.grid(row=2, column=0, padx=10, pady=10)

        self.RubroLabel = Label(self.miFrame, text="Rubro: ")
        self.RubroLabel.grid(row=1, column=4, padx=10, pady=10)

        self.FacturacionLabel = Label(self.miFrame, text="Facturacion: ")
        self.FacturacionLabel.grid(row=2, column=4, padx=10, pady=10)

        self.TotalFacturadoLabel = Label(self.miFrame, text="Total Facturado: ")
        self.TotalFacturadoLabel.grid(row=3, column=3, padx=10, pady=10)

        self.TotalFacturado = Label(self.miFrame, textvariable=self.value,fg="red",bg="white",font=("Times New Roman",20))
        self.TotalFacturado.grid(row=3, column=4, padx=10, pady=10)

        #-----------------Visor de Galeria Datos-----------------------

        self.miFrame_3 = Frame(self)
        self.miFrame_3.pack()

        self.tituloLabel=Label(self.miFrame_3,text="Datos Galeria",fg="blue",bg="white",font=("Times New Roman",20))
        self.tituloLabel.grid(row=0, column=1, padx=10, pady=10,sticky="we")

        self.treeGaleria = ttk.Treeview(self.miFrame_3,columns = ("APELLIDO","NOMBRE","LOCAL","RUBRO","FACTURACION"))
        self.treeGaleria.grid(row=1,column=1,padx=10,pady=10)
        self.treeGaleria['show']='headings'
        self.treeGaleria.heading('#0', text='column0', anchor=tk.W)
        self.treeGaleria.heading('#1', text='APELLIDO', anchor=tk.W)
        self.treeGaleria.heading('#2', text='NOMBRE', anchor=tk.W)
        self.treeGaleria.heading('#3', text='LOCAL', anchor=tk.W)
        self.treeGaleria.heading('#4', text='RUBRO', anchor=tk.W)
        self.treeGaleria.heading('#5', text='FACTURACION', anchor=tk.W)
        
        self.treeGaleria.column('#0',width=150,minwidth=150,stretch=tk.YES)
        self.treeGaleria.column('#1',width=100,minwidth=100,stretch=tk.YES)
        self.treeGaleria.column('#2',width=150,minwidth=150,stretch=tk.YES)
        self.treeGaleria.column('#3',width=50,minwidth=50,stretch=tk.YES)
        self.treeGaleria.column('#4',width=250,minwidth=250,stretch=tk.YES)
        self.treeGaleria.column('#5',width=100,minwidth=100,stretch=tk.YES)

        for row in self.consultarGaleria():
            self.treeGaleria.insert('',END, values=row)

        self.scrollVert2=Scrollbar(self.miFrame_3,command=self.treeGaleria.yview)
        self.scrollVert2.grid(row=1,column=2,sticky="nsnew")
        self.treeGaleria.config(yscrollcommand=self.scrollVert2.set)

        #-----------------COMIENZO DE BOTONES-----------------------
        
        self.miFrame_2 = Frame(self)
        self.miFrame_2.pack()

        self.botonCreate = Button(self.miFrame_2, text="Insertar", width=10,command=lambda:self.InsertarData())
        self.botonCreate.grid(row=4, column=0, padx=10, pady=10)

        self.botonModificarApellido =Button(self.miFrame_2, text="Modificar Por Apellido", width=25,command=lambda:self.ModificarApellido())
        self.botonModificarApellido.grid(row=4, column=1, padx=10, pady=10)

        self.NombreLabelNuevo = Label(self.miFrame_2, text="Apellido Nuevo: ")
        self.NombreLabelNuevo.grid(row=4, column=2, padx=10, pady=10)

        self.cuadroNuevoNombre = Entry(self.miFrame_2, textvariable=self.datacuadroNuevoNombre)
        self.cuadroNuevoNombre.grid(row=4, column=3, padx=10, pady=10,columnspan=3)
        self.cuadroNuevoNombre.config(justify="center")


    #-----------------METODOS-----------------------

    def UpdateTreeViewGaleria(self):
        for row in self.treeGaleria.get_children():
            self.treeGaleria.delete(row)
        for row in self.consultarGaleria():
            self.treeGaleria.insert('',END, values=row)

    def consultarGaleria(self):
        archivoGaleria = open('galeriaTP1.txt', "r")
        datos = []
        for linea in archivoGaleria:
            linea=linea.replace('\n',"")
            linea=re.sub('\t+', '\t', linea)
            tuplaDato=tuple(linea.split('\t'))
            datos.append(tuplaDato)
        archivoGaleria.close()
        #print(datos)
        return datos

    def calcularFacturaTotal(self):
        facturaTotal=0
        datos=self.consultarGaleria()
        for tupla in datos:
           facturaTotal += float(tupla[4])
        return facturaTotal

    def leerInfoInputBox(self):
        return [self.datacuadroNombre.get(),self.datacuadroApellido.get(),self.datacuadroRubro.get(),self.datacuadroFacturacion.get()]

    def borrarInputBox(self):
        self.datacuadroNombre.set("")
        self.datacuadroApellido.set("")
        self.datacuadroRubro.set("")
        self.datacuadroFacturacion.set("")
        self.datacuadroNuevoNombre.set("")
        #print("GaleriaView - Se borran todos los campos")

    def ultimoIndex(self):
        index=0
        datos=self.consultarGaleria()
        last = datos.pop()
        return int(last[2])+1

    def InsertarData(self):
        index=self.ultimoIndex()
        listadata=self.leerInfoInputBox()
        
        #data='\n'+listadata[0].ljust(50, '\t') + listadata[1].ljust(50, '\t') + str(index)+'\t'+listadata[2].ljust(80, '\t')+listadata[3]
        data=listadata[0]+'\t'+ listadata[1]+'\t'+str(index)+'\t'+listadata[2]+'\t'+listadata[3]+'\n'
        archivoGaleria = open('galeriaTP1.txt', "a")
        archivoGaleria.write(data)
        archivoGaleria.close()
        self.UpdateTreeViewGaleria()
        self.value.set(str(self.calcularFacturaTotal()))
        self.borrarInputBox()

    def ModificarApellido(self):
        datos=self.consultarGaleria()
        apellido=self.datacuadroApellido.get()
        for tupla in datos:
            if apellido in tupla:
                indice=datos.index(tupla)
                print(tupla)
                datos.remove(tupla)
                nuevaTupla=(self.datacuadroNuevoNombre.get(),tupla[1],tupla[2],tupla[3],tupla[4])
                datos.insert(indice,nuevaTupla)
                #datos.append(nuevaTupla)
                remove('galeriaTP1.txt')
                for lineas in datos:
                    escribirEnArchivo(lineas)
                self.UpdateTreeViewGaleria()
                self.borrarInputBox()


def escribirEnArchivo(unaLista):
    data=separarListaConTabulador(unaLista)
    archivoGaleria = open('galeriaTP1.txt', "a+")
    archivoGaleria.write(data)
    archivoGaleria.close()

def separarListaConTabulador(unaLista):
    return unaLista[0]+'\t'+ unaLista[1]+'\t'+unaLista[2]+'\t'+unaLista[3]+'\t'+unaLista[4]+'\n'

class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("GaleriaView Data - PL-JCL")
        
        self.notebook = ttk.Notebook(self)
        
        self.greeting_frame = GaleriaFrame(self.notebook)
        self.notebook.add(
            self.greeting_frame, text="Galeria Datos", padding=10)
        
        self.notebook.pack(padx=10, pady=10)
        self.pack()

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()