# -*- coding: utf-8 -*-


import sqlite3 as biblioteca
from gi.repository import Gtk
from InformeReportLab import ReportLab
settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True
class Biblioteca:

    """AKI ES DONDE VAMOS A DECLARAR LAS VARIABLES DE LAS VENTANAS QUE CREAMOS CON GLADE E INICIALIZAR LOS BUILDERS"""
    #EN ESTE APARTADO CREAMOS EL ACCESO A LAS VENTANAS CREADAS CON GLADE
    archivoVentanaPrincipal = "VentanaPrincipal1.glade"
    archivoVentanaConsulta = "VentanaConsulta.glade"
    archivoVentanaIntroducir = "VentanaIntroducir.glade"
    archivoVentanaEliminar = "VentanaEliminar.glade"
    archivoVentanaAlerta = "Alertacodigo.glade"
    archivoVentanaArticuloEliminado = "VentanaArticuloEliminado.glade"

    #DECLARACION DE LOS GTK BUILDER PARA LAS VENTANAS.
    builderVentanaAlerta = Gtk.Builder()
    builderVentanaPrincipal = Gtk.Builder()
    builderVentanaConsulta = Gtk.Builder()
    builderVentanaIntroducir = Gtk.Builder()
    builderVentanaEliminar = Gtk.Builder()
    builderVentanaArticuloEliminado = Gtk.Builder()

    #AKI TENEMOS LOS CONSTRUCTORES DE LAS INTERFACES
    builderVentanaPrincipal.add_from_file(archivoVentanaPrincipal)
    builderVentanaConsulta.add_from_file(archivoVentanaConsulta)
    builderVentanaIntroducir.add_from_file(archivoVentanaIntroducir)
    builderVentanaEliminar.add_from_file(archivoVentanaEliminar)
    builderVentanaAlerta.add_from_file(archivoVentanaAlerta)
    builderVentanaArticuloEliminado.add_from_file(archivoVentanaArticuloEliminado)

    #VENTANAS CONTENEDORAS
    ventanaEntrada = builderVentanaPrincipal.get_object("VentanaPrincipal")
    ventanaConsultas = builderVentanaConsulta.get_object("VentanaConsulta")
    ventanaIntroducir = builderVentanaIntroducir.get_object("VentanaIntroducir")
    ventanaEliminar = builderVentanaEliminar.get_object("VentanaEliminar")
    ventanaAlertaCodigo = builderVentanaAlerta.get_object("AlertaCodigo")
    ventanaAlertaArchivoEliminado = builderVentanaArticuloEliminado.get_object("VentanaArticuloEliminado")
    ventanaEntrada.show_all()
    #CONEXION A LA BASE DE DATOS Y CURSOR PARA PODER ACCEDER A ELLA
    bd = biblioteca.connect("biblioteca.dat")
    print(bd)
    cursor = bd.cursor()



#BUSQUEDA Y MODIFICACION:
    def al_buscar(self, busqueda):
        """METODO BUSQUEDAS"""
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaAutorConsultada.set_text("")
        self.cajaFechaConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        if self.RadioCod.get_active():
            #RECOGEMOS EL CODIGO DE LA CAJA DE TEXTO
            codigo = self.cajaIdConsulta.get_text().upper()
            #BUSCAMOS EL CODIGO QUE SE ENCUENTRA EN NUESTRA BASE DE DATOS POR EL CAMPO CODIGO
            self.cursor.execute("Select * from biblioteca where Codigo='"+codigo+"'")
            #RECORREMPS EL CURSOR Y LO MOSTRAMOS EN PANTALLA SI EXISTE
            for libro in self.cursor:
                self.cajaNombreConsultada.set_text(str(libro[1]))
                self.cajaPrecioConsultada.set_text(str(libro[2]))
                self.cajaCantidadConsultada.set_text(str(libro[3]))
                self.cajaAutorConsultada.set_text(str(libro[4]))
                self.cajaFechaConsultada.set_text(str(libro[5]))

        elif self.RadioNomb.get_active():
             #RECOJEMOS EL CODIGO QUE SE ENCUENTRA EN LA CAJA DE TEXTO
            nombre = self.cajaIdConsulta.get_text()
            #AKI LO BUSCAMOS EN LA BASE DE DATOS POR EL CAMPO NOMBRE
            self.cursor.execute("Select * from biblioteca where Nombre='"+nombre+"'")
            #Recorremos el cursor y mostraremos por pantalla si existe
            for libro in self.cursor:
                self.cajaNombreConsultada.set_text(str(libro[1]))
                self.cajaPrecioConsultada.set_text(str(libro[2]))
                self.cajaCantidadConsultada.set_text(str(libro[3]))
                self.cajaAutorConsultada.set_text(str(libro[4]))
                self.cajaFechaConsultada.set_text(str(libro[5]))




    def introducirStock(self, introducir):
        """Este metodo introduce o stock"""
        id = self.cajaIntroducirCodId.get_text().upper()
        nombre = self.cajaIntroducirNombre.get_text().upper()
        precio = self.cajaIntroducirPrecio.get_text().upper()
        cantidad = self.cajaIntroducirCantidad.get_text().upper()
        fecha = self.cajaIntroducirFecha.get_text().upper()
        autor = self.cajaIntroducirAutor.get_text().upper()

        self.limpiarIntroducir(self)
        print("inserte")
        self.cursor.execute("select codigo from biblioteca")
        #RECOJEMOS LOS CODIGOS DE LOS LIBROS PARA SABER SI ESTAN EN LA BASE
        codigos = self.cursor.fetchall()
        existe=False
        for producto in codigos:

            idCompare = str(producto)
            #SI ESTA EN LA BASE PASA A SER TRUE Y POR LO TANTO NO SE VOLVERA A INSERTAR EN LA BASE HASTA Q SEA ELIMINADOS
            if idCompare[2:4]==id:
                print("Ya esta en la base de datos!!")
                existe = True
                self.ventanaAlertaCodigo.show_all()

        if existe==False:
            #INCERTAMOS EN LA TABLA DE LA BASE
            self.cursor.execute("insert into biblioteca values('" + id + "','" + nombre + "','" + precio + "','" + cantidad + "','" + fecha + "','" + autor + "')")
            print("Insertado")
            #COMMITS PARA ASEGURARNOS QUE SE GUARDE EN LA BASE CORRECTAMENTE
            self.bd.commit()

        existe=False


    def al_modificar(self, modificacion):
        """ESTE ES EL METODO QUE NOS MODIFICARA LAS TABLAS EN LA BASE DE DATOS"""
        #LAS VARIABLES DEFINIDAS RECOJERAN EL TEXTO DE LAS CAJAS DE TEXTO
        nombre = self.cajaNombreConsultada.get_text().upper()
        precio = self.cajaPrecioConsultada.get_text().upper()
        cantidad = self.cajaCantidadConsultada.get_text().upper()
        autor = self.cajaAutorConsultada.get_text().upper()
        fecha = self.cajaFechaConsultada.get_text().upper()
        id = self.cajaIdConsulta.get_text().upper()
        #HACEMOS UNA ACTUALIZACION A LAS TABLAS CON LA CONSULTA UPDATE
        self.cursor.execute(
            "update biblioteca set Nombre ='" + nombre + "',Precio='" + precio + "',Cantidad='" + cantidad  + "',Autor='" + autor +"',Fecha='" + fecha + "'" + " where Codigo='" + id + "'")
        print("Modificado")
        self.consolaVenta.set_text("Artículo modíficado")
        #COMMITS
        self.bd.commit()
        #BORRAMOS CUADRO DE TEXTO UNA VEZ QUE SE HAYA MODIFICADO
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        self.cajaFechaConsultada.set_text("")
        self.cajaAutorConsultada.set_text("")


    def Eliminar(self, eliminado):
        """ESTO NOS ELIMINARA DE LA BASE DE DATOS"""
        #PARECIDO AL METODO BUSCAR PERO ESTE ELIMINARA
        cajaEliminar = self.cajaEliminar.get_text()
        self.cursor.execute("delete from biblioteca where Codigo ='" + cajaEliminar + "'")
        print("Borrado")
        self.ventanaAlertaArchivoEliminado.show_all()
        #COMMIT
        self.bd.commit()
        #BORRAMOS LA CAJA YA USADA
        self.cajaEliminar.set_text("")



#LIMPIAMOS CAMPOS
    def click_limpiarConsulta(self,limpieza):
        """LIMPIAMOS CAMPS"""
        self.cajaIdConsulta.set_text("")
        self.cajaNombreConsultada.set_text("")
        self.cajaPrecioConsultada.set_text("")
        self.cajaCantidadConsultada.set_text("")
        self.cajaAutorConsultada.set_text("")
        self.cajaFechaConsultada.set_text("")
        self.cajaNventas.set_text("")



    def limpiarIntroducir(self, introduccion):
        """ESTE METODO LIMPIA LOS CAMPOS"""
        self.cajaIntroducirCodId.set_text("")
        self.cajaIntroducirNombre.set_text("")
        self.cajaIntroducirPrecio.set_text("")
        self.cajaIntroducirCantidad.set_text("")
        self.cajaIntroducirFecha.set_text("")
        self.cajaIntroducirAutor.set_text("")


    def realizar_venta(self, venta):
        """ESTE METODO VENDE Y REDUCE EL CAMPPO DE CANTIDAD"""
        id = self.cajaIdConsulta.get_text().upper()
        cantidadInicial = self.cajaCantidadConsultada.get_text()
        cantidadVenta = self.cajaNventas.get_text()
        cantidadF = float(cantidadInicial) - float(cantidadVenta)
        cantidadI = int(cantidadF)
        cantidad = str(cantidadI)


        if cantidadI==0:
            self.cursor.execute("delete from biblioteca where Codigo ='" + id + "'")
            self.consolaVenta.set_text("            YA NO QUEDAN LIBROS!           ")
        elif cantidadI<=-1:
            self.consolaVenta.set_text("            LIBROS INSUFUCUENTES!        ")
        else:
            self.cursor.execute("update biblioteca set Cantidad='"+cantidad+"' where Codigo='"+id+"'")
            print("Modificado")
            self.cajaCantidadConsultada.set_text(str(int(cantidad)))
            self.consolaVenta.set_text("             LIBROS/S VENDIDO!!              ")

        self.bd.commit()


    def generar_informe(self, entrada):
        """INFORME REPORTLAB DE LA BASE DE DATOS"""
        ReportLab()




#FUNCION QUE NOS MUESTRA LAS VENTANAS SEGUN HACEMOS CLICK
    def click_introducir(self, entrada):
        """DEFINIMOS CLICK EN INNTRODUCIR"""
        self.ventanaEntrada.hide()
        self.ventanaIntroducir.show_all()


    def click_consultar(self, consulta):
        """DEFINIMOS CLICK EN CONSULTAR"""
        self.ventanaEntrada.hide()
        self.consolaVenta.set_text("")
        self.ventanaConsultas.show_all()


    def Eliminar_articulo(self,eliminado):
        """DEFINIMOS CLICK EN ELIMINAR"""
        self.ventanaEntrada.hide()
        self.ventanaEliminar.show_all()



#Funciones de vuelta a la ventana principal
    def click_volverConsulta(self, vuelta):
        """DEFINIMOS CLICK EN VOLVER"""
        self.click_limpiarConsulta(self)
        self.ventanaConsultas.hide()
        self.ventanaEntrada.show_all()


    def volverIntroducir(self, vuelta):
        """DEFINIMOS CLICK EN VOLVER"""
        self.limpiarIntroducir(self)
        self.ventanaIntroducir.hide()
        self.ventanaEntrada.show_all()


    def volverEliminar(self, vuelta):
        """DEFINIMOS CLICK EN VOLVER"""
        self.cajaEliminar.set_text("")
        self.ventanaEliminar.hide()
        self.ventanaEntrada.show_all()



#DECLARACION DE LOS MANEJADORES Y SEÑALES Y LA ENTRADA PRINCIPAL AL INICIAR LA APLICACION
    def __init__(self):
        """BOTONES CAJAS Y DEMAS"""
        #VENTANA PRINCIPAL PARA QUE SE MUESTRE

        self.ventanaEntrada.show_all();


        #EQUIVALENCIA GLADE PYTHON(MANEJADORES)
        manejadores = {
                  "click_limpiarConsulta":self.click_limpiarConsulta,
                  "click_volverConsulta":self.click_volverConsulta,
                  "limpiarCamposIntroducir":self.limpiarIntroducir,
                  "click_introducirStock":self.introducirStock,
                  "Eliminar_articulo":self.Eliminar_articulo,
                  "click_introducir": self.click_introducir,
                  "volverIntroducir":self.volverIntroducir,
                  "click_consultar": self.click_consultar,
                  "volverEliminar":self.volverEliminar,
                  "click_modificar":self.al_modificar,
                  "click_vender":self.realizar_venta,
                  "cerrarAlertaCodigo":self.alerta,
                  "informe":self.generar_informe,
                  "al_buscar":self.al_buscar,
                  "Terminar1":self.Terminar,
                  "Terminar2":self.Terminar,
                  "Terminar3":self.Terminar,
                  "Terminar":self.Terminar,
                  "Eliminar":self.Eliminar,
                  "botonOk":self.BotonOk
        }
        #CONEXION DE LOS CONTRUCTORES CON LOS MANEJADORES
        self.builderVentanaPrincipal.connect_signals(manejadores)
        self.builderVentanaConsulta.connect_signals(manejadores)
        self.builderVentanaIntroducir.connect_signals(manejadores)
        self.builderVentanaEliminar.connect_signals(manejadores)
        self.builderVentanaAlerta.connect_signals(manejadores)
        self.builderVentanaArticuloEliminado.connect_signals(manejadores)

        #RECOJEMOS LAS CAJAS DE LAS VENTANAS
        self.cajaIdConsulta = self.builderVentanaConsulta.get_object("cajaIdConsulta")
        self.cajaNventas = self.builderVentanaConsulta.get_object("cajaVenta")
        self.cajaNombreConsultada = self.builderVentanaConsulta.get_object("cajaNombreConsultada")
        self.consolaVenta = self.builderVentanaConsulta.get_object("LConsola")
        self.cajaPrecioConsultada = self.builderVentanaConsulta.get_object("cajaPrecioConsultada")
        self.cajaFechaConsultada = self.builderVentanaConsulta.get_object("cajaFechaConsultada")
        self.cajaAutorConsultada = self.builderVentanaConsulta.get_object("cajaAutorConsultada")
        self.cajaCantidadConsultada = self.builderVentanaConsulta.get_object("cajaCantidadConsultada")
        self.cajaIntroducirCodId = self.builderVentanaIntroducir.get_object("cajaIntroducirCodId")
        self.cajaIntroducirFecha = self.builderVentanaIntroducir.get_object("cajaIntroducirFecha")
        self.cajaIntroducirAutor = self.builderVentanaIntroducir.get_object("cajaIntroducirAutor")
        self.cajaIntroducirNombre = self.builderVentanaIntroducir.get_object("cajaIntroducirNombre")
        self.cajaIntroducirPrecio = self.builderVentanaIntroducir.get_object("cajaIntroducirPrecio")
        self.comboEstado = self.builderVentanaIntroducir.get_object("comboStock")
        self.cajaIntroducirCantidad = self.builderVentanaIntroducir.get_object("cajaIntroducirCantidad")
        self.cajaEliminar = self.builderVentanaEliminar.get_object("cajaEliminar")
        self.RadioCod = self.builderVentanaConsulta.get_object("radioCodigo")
        self.RadioNomb = self.builderVentanaConsulta.get_object("radioNombre")




    def alerta(self, alerta):
        """DEFINIMOS LA VENTANA DE ALERTA"""
        self.ventanaAlertaCodigo.hide()



    def BotonOk(self,ok):
        """DEFINIMOS EL CLICK OK"""
        self.ventanaAlertaArchivoEliminado.hide()



#FUNCION DE CIERRE DEL PROGRAMA
    def Terminar(self, dos, tres):
        """Definimos cel cierre del programa"""
        #Cerramos todas las ventanas y el main
        self.ventanaEntrada.connect("delete-event", Gtk.main_quit)
        self.ventanaIntroducir.connect("delete-event", Gtk.main_quit)
        self.ventanaEliminar.connect("delete-event", Gtk.main_quit)
        self.ventanaConsultas.connect("delete-event", Gtk.main_quit)
        Gtk.main_quit()


Biblioteca()
Gtk.main()
