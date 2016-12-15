#@auth.requires_login()
def administrarUsuarios():
    grid = SQLFORM.grid(db.auth_user,
                        create = False,
                        deletable = False,
                        editable=True,
                        details=True,
                        csv = True,
                        exportclasses = dict(cvs = False,
                                             xml = False,
                                             csv_with_hidden_cols = False,
                                             tsv_with_hidden_cols = False,
                                             tsv = False,
                                             json = False )
                       )
    return locals()

def subscribe():
    suscribir = len(request.args) == 0 or request.args[0]==str(True)
    setSuscripcion(suscribir)
    return True