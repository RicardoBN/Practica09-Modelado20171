import sys, time
from PyQt4 import QtCore, QtGui, uic

estado = 0
estado_ter = 0
serpiente = []
dir = 3
class Servidor(QtGui.QMainWindow):
    def __init__(self): 
        super(Servidor, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.spinBox.valueChanged.connect(self.cambia_columnas)
        self.spinBox_2.valueChanged.connect(self.cambia_filas)
        self.doubleSpinBox.valueChanged.connect(self.cambia_ms)
        self.pushButton_2.clicked.connect(self.inicia)
        self.pushButton_3.clicked.connect(self.termina)
        self.setFocus()
        self.show()
    # Cambio de Movimiento    
    def keyPressEvent(self, event):
      global dir
      key = event.key()      
      if key == QtCore.Qt.Key_Left and dir != 4:
        dir = 2              
      if key == QtCore.Qt.Key_Right and dir != 2:
        dir = 4                
      if key == QtCore.Qt.Key_Up and dir != 3:
        dir = 1                
      if key == QtCore.Qt.Key_Down and dir != 1:
        dir = 3         
    # Inicio del juego     
    def inicia(self):
      global estado
      global serpiente
      print(estado)          
      self.pushButton_3.setText("Terminar")
      self.setFocus()      
      if estado == 0:
        estado = 1
        serpiente = []
        self.crea_serp(15)
        self.colorea_serp(serpiente)
        self.pushButton_2.setText("Pausar")
        self.cambia_ms()
      elif estado == 1:
        estado = 2
        self.pushButton_2.setText("Renaudar")
      elif estado == 2:
        estado = 1
        self.pushButton_2.setText("Pausar")
        self.cambia_ms()
      elif estado == 3:
        estado = 0
        self.inicia()    
    #Terminar el juego  
    def termina(self):
      global estado
      global dir             
      estado = 3
      dir = 3
      print("El juego ha terminado")
      self.pushButton_2.setText("Reiniciar")
      self.tableWidget.setColumnCount(0)
      self.tableWidget.setRowCount(0)
      self.tableWidget.setColumnCount(0)
      self.spinBox_2.setProperty("value", 20)
      self.spinBox.setProperty("value", 20)
      self.doubleSpinBox.setProperty("value", 0.05)
      self.tableWidget.setColumnCount(self.spinBox.value())
      self.tableWidget.setRowCount(self.spinBox_2.value())
    #Cambia el delay del programa y en este se actualizan las serpientes    
    def cambia_ms(self):
      global dir         
      tiempo = self.doubleSpinBox.value()
      while estado == 1:
        time.sleep(tiempo)       
        self.mueve_serpiente(serpiente,dir)         
        QtCore.QCoreApplication.processEvents()

    #Quita la cola y actualiza la cabeza con respecto a la dirección    
    def mueve_serpiente(self,serp,direc):
      print(direc)
      self.tableWidget.item(serp[0][0],serp[0][1]).setBackground(QtGui.QColor(255,255,255))
      limit_col = int(self.spinBox.value())-1
      limit_row = int(self.spinBox_2.value())-1
      cabeza = serp[-1]
      serp.pop(0)
      if direc == 1:
        if cabeza != [0, serp[-1][1]]: 
          serp.append([serp[-1][0]-1,serp[-1][1]]) #Movimiento hacia arriba
        else:
          serp.append([limit_row,serp[-1][1]])
      if direc == 2:
        if cabeza != [serp[-1][0],0]:
          serp.append([serp[-1][0],serp[-1][1]-1]) #Movimiento hacia la izquierda                                      
        else:
          serp.append([serp[-1][0], limit_row])
      if direc == 3:
        if cabeza != [limit_row, serp[-1][1]]:
          serp.append([serp[-1][0]+1,serp[-1][1]]) #Movimiento hacia abajo
        else:
          serp.append([0,serp[-1][1]])
      if direc == 4: 
        if cabeza != [serp[-1][0],limit_col]:
         serp.append([serp[-1][0], serp[-1][1]+1]) #Movimiento havia la derecha
        else:    
          serp.append([serp[-1][0], 0])
      for x in range(0,len(serp)-1):        
        self.colorea_serp(serp)
      for cuerpo in serp:
        if serp.count(cuerpo)>1:
          self.termina()
    #Cambio de columnas dinámico        
    def cambia_columnas(self):
      Columnas = int(self.tableWidget.columnCount())
      total = int(self.spinBox.value())
      if Columnas >= total:
        while Columnas >= total:
          self.tableWidget.removeColumn(Columnas)
          Columnas -= 1
      elif Columnas < total:
        while Columnas < total:
          self.tableWidget.insertColumn(Columnas)
          Columnas += 1
    #Cambio de filas dinámico      
    def cambia_filas(self):
      filas = int(self.tableWidget.rowCount())
      total = int(self.spinBox_2.value())
      if filas >= total:
        while filas >= total:
          self.tableWidget.removeRow(filas)
          filas -= 1
      elif filas < total:
        while filas < total:
          self.tableWidget.insertRow(filas)
          filas += 1
    #Crea una serpiente en       
    def crea_serp(self,tam):
        for x in range(0,tam):
          serpiente.append([x,0]) 
    def colorea_serp(self,serp):
      for cuerpo in serp:
        self.tableWidget.setItem(cuerpo[0],cuerpo[1], QtGui.QTableWidgetItem())
        self.tableWidget.item(cuerpo[0],cuerpo[1]).setBackground(QtGui.QColor(255,68,0))     
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    serv = Servidor()
    sys.exit(app.exec_())        
        
