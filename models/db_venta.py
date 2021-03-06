# -*- coding: utf-8 -*-
db.define_table("formaPago",
                Field("descripcion", "string", label=T('Descripción'),required=True, notnull=True),
                format = '%(descripcion)s')
db.formaPago.descripcion.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar la forma de pago '),
                                     IS_NOT_IN_DB(db, 'formaPago.descripcion', error_message=' Ya existe ')]
db.formaPago.id.label='Número'

#zonas de entrega
db.define_table("zona",
                Field("descripcion", "string", required=True, notnull=True, label=T('Descripción')),
                Field("precio", "integer", required=True, notnull=True, label=T('Costo')),
                Field("dia", "string", required=True, notnull=True, label=T('Día/s')),
                format = '%(descripcion)s')
db.zona.descripcion.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar descripción '),
                                IS_NOT_IN_DB(db, 'zona.descripcion', error_message=' Ya existe ')]
db.zona.id.label='Número'

#Domicilios
db.define_table("domicilio",
                Field("idCliente", "reference auth_user", required=True, notnull=True, label=T('Cliente'), writable=False),
                Field("referencia", "string", required=True, notnull=True, label=T('Referencia del domicilio')),
                Field("calle", "string", required=True, notnull=True, label=T('Calle')),
                Field("numero", "integer", required=True, notnull=True, label=T('Nro ')),
                Field("piso", "string", label=T('Piso')),
                Field("departamento", "string", label=T('Depto')),
                Field("otros", "string", label=T('Otros ')),
                Field("idZona", "reference zona", label=T('Zona')),
                format = '%(calle)s - %(numero)s - %(idZona)s')
db.domicilio.idCliente.requires = [IS_NOT_EMPTY(error_message=' Falta ingresar descripción '),
                                   IS_IN_DB(db, 'auth_user.id',' %(last_name)s %(first_name)s ')]
db.domicilio.idZona.requires = IS_IN_DB(db, 'zona.id', ' %(descripcion)s')
db.domicilio.referencia.requires = IS_NOT_IN_DB(db, db.domicilio.referencia, error_message=T('Esa referencia ya existe'))
db.domicilio.id.label='Número'
db.domicilio.id.readable=False
db.domicilio.piso.represent = lambda v, r: '' if v is None else v
db.domicilio.departamento.represent = lambda v, r: '' if v is None else v
db.domicilio.otros.represent = lambda v, r: '' if v is None else v

############################################################################################################################
#ventas basico  db.tabla.campo.default = auth.user_id if auth.user else 0
db.define_table("venta",
    Field("idCliente", 'reference auth_user', writable=False, readable=True, label=T('Cliente Nro')),
    Field("fechaPedido","datetime", writable=False, readable=True, default=request.now, label=T('Fecha Pedido') ),
    Field("formaPago", 'reference formaPago',  label=T('Forma de pago') ),
    Field("importeTotal","string", label=T('Importe Total') ),
    Field("formaEntrega", 'string',  label=T('Forma de entrega') ),
    Field("fechaEntrega","datetime", default=None, label=T('Fecha Entrega') ),
    Field("costoEntrega", 'integer',  label=T('Costo de entrega') ),
    Field("idDomicilio", "reference domicilio", label=T('Domicilio')),
    Field("estado","string", label=T('Estado') ),
    Field("comentario", 'text',  label=T('Comentarios:') ),
    format = '%(id)s  - %(idCliente)s - %(fechaPedido)s ')

db.venta.idCliente.requires = IS_IN_DB(db, 'auth_user.id','%(first_name)s - %(last_name)s')
db.venta.formaPago.requires = IS_EMPTY_OR(IS_IN_DB(db, 'formaPago.id',' %(descripcion)s '))
db.venta.id.label ='Número'
db.venta.formaEntrega.requires= IS_EMPTY_OR(IS_IN_SET(["Acordar con el vendedor", "Entrega a domicilio", "Retira en local"]))
db.venta.idDomicilio.requires = IS_EMPTY_OR(IS_IN_DB(db, 'domicilio.id', '%(calle)s - %(numero)s - %(idZona)s'))
db.venta.estado.requires= IS_IN_SET(["Pendiente", "Espera acuerdo", "Pendiente confirmar fecha", "Delivery", "Retira", "Entregado"])
db.venta.costoEntrega.represent = lambda v, r: '' if v is None else v
db.venta.fechaEntrega.represent = lambda v, r: '' if v is None else v
db.venta.comentario.represent = lambda v, r: '' if v is None else v

#Detalle ventas
db.define_table("detalleVenta",
    Field("idVenta","integer", required=True, notnull=True, label=T('Nro de Venta ') ),
    Field("idProducto","integer", required=True, notnull=True, label=T('Producto ') ),
    Field("cantidad","integer", required=True, label=T(' Cantidad ') ),
    )
db.detalleVenta.idProducto.requires = IS_IN_DB(db,'producto.idProducto', ' %(nombre)s' )
db.detalleVenta.idVenta.requires = IS_IN_DB(db,'venta.id', '%(id)s  - %(idCliente)s - %(fechaPedido)s ' )
db.detalleVenta.id.label ='Número'
