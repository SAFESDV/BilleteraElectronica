# -*- coding: utf-8 -*-

'''
Created on 29/4/2015

@author: SAFE SDV (SAFE Software DeVelopment) 
'''

from decimal import Decimal
from datetime import datetime
import hashlib
import uuid
from builtins import str

class Creditos(object):
    
    def __init__(self, monto, id_establecimiento):
        
        if (isinstance(monto, str) or isinstance(monto, bool) ):
            raise Exception("Debe ingresar un monto numérico")
        
        self.monto = Decimal(monto).quantize(Decimal('1.00'))
        self.fecha_transaccion = datetime.today()
        self.id_establecimiento = id_establecimiento

class Debitos(object):
    def __init__(self, monto, id_establecimiento):
        
        if (isinstance(monto, str) or isinstance(monto, bool) ):
            raise Exception("Debe ingresar un monto numérico")
        
        self.monto = Decimal(monto).quantize(Decimal('1.00'))
        self.fecha_transaccion = datetime.today()
        self.id_establecimiento = id_establecimiento
        
class BilleteraElectronica(object):

    def __init__(self, ID, nombre, apellido, CI, PIN):
        
        if (not isinstance(CI, int) or (CI <= 0)):
            raise Exception("La cedula suministrada nos es válida")
        
        if ((nombre == "" or apellido == "" or PIN == "") or
            not(isinstance(nombre, str)) or
            not(isinstance(apellido, str)) or
            not(isinstance(PIN, str))) :
            raise Exception("El nombre, apellido y el PIN deben ser una cadena de caracteres")
        
        self.ID = ID 
        self.nombre = nombre
        self.apellido = apellido
        self.CI = CI 
        
        #Comentario explicando que diablos es esto!!!! O.o
        salt = uuid.uuid4().hex
        self._PIN = hashlib.sha256(salt.encode() + PIN.encode()).hexdigest() + ':' + salt
            
        
        self.creditos = []
        self.debitos = []
        self._saldo = 0
        
    def _saldo(self):
        return Decimal(self._saldo).quantize(Decimal('1.00'))
            
    def Recargar(self,creditoEntrante):
        
        if (creditoEntrante.monto <= 0):
            raise Exception("No es posible recargar una cantidad no positiva")       

        self.creditos.append(creditoEntrante)
        self._saldo += creditoEntrante.monto
        
    def Consumir(self,debitoEntrante, PIN):
                
        if (debitoEntrante.monto <= 0):
            raise Exception("No es posible consumir una cantidad no positiva")     

        if (self._saldo - debitoEntrante.monto < 0):
            raise Exception("No tiene suficiente fondos para efectuar la operación")  
        
        PIN_prueba, salt = self._PIN.split(':')
        if PIN_prueba != hashlib.sha256(salt.encode() + PIN.encode()).hexdigest():
            raise Exception("El PIN suministrado es incorrecto, operación cancelada")
        
        self.debitos.append(debitoEntrante)
        self._saldo -= debitoEntrante.monto
