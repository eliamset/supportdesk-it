from app import create_app, db
from app.models import Usuario, Categoria, Empleado, Tecnico, Ticket, Intervencion
from datetime import datetime, timedelta

app = create_app()

def seed():
    with app.app_context():
        # Crear tablas en caso de que no existan
        db.create_all()
        print("Tablas verificadas/creadas.")
        
        # 1. Crear usuarios base para autenticación si no existen
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin', rol='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("Usuario administrador creado: admin / admin123")
            
        if not Usuario.query.filter_by(username='tecnico01').first():
            tecnico_user = Usuario(username='tecnico01', rol='tecnico')
            tecnico_user.set_password('user123')
            db.session.add(tecnico_user)
            print("Usuario técnico creado: tecnico01 / user123")
            
        if not Usuario.query.filter_by(username='tecnico02').first():
            tecnico_user2 = Usuario(username='tecnico02', rol='tecnico')
            tecnico_user2.set_password('user123')
            db.session.add(tecnico_user2)
            print("Usuario técnico creado: tecnico02 / user123")

        # Crear usuarios empleados de prueba si no existen
        if not Usuario.query.filter_by(username='empleado01').first():
            empleado_user = Usuario(username='empleado01', rol='empleado')
            empleado_user.set_password('user123')
            db.session.add(empleado_user)
            print("Usuario empleado creado: empleado01 / user123")
            
        if not Usuario.query.filter_by(username='empleado02').first():
            empleado_user2 = Usuario(username='empleado02', rol='empleado')
            empleado_user2.set_password('user123')
            db.session.add(empleado_user2)
            print("Usuario empleado creado: empleado02 / user123")

        # 2. Crear categorías iniciales si no hay ninguna
        if not Categoria.query.first():
            categories = ['Hardware', 'Software', 'Red', 'Accesos', 'Otros']
            for name in categories:
                db.session.add(Categoria(nombre_categoria=name))
            print("Categorías base creadas.")
        db.session.commit()

        # Obtener categorías de referencia
        cat_hw = Categoria.query.filter_by(nombre_categoria='Hardware').first()
        cat_sw = Categoria.query.filter_by(nombre_categoria='Software').first()
        cat_red = Categoria.query.filter_by(nombre_categoria='Red').first()
        cat_acc = Categoria.query.filter_by(nombre_categoria='Accesos').first()
        cat_otr = Categoria.query.filter_by(nombre_categoria='Otros').first()

        # 3. Crear empleados si la tabla está vacía
        if not Empleado.query.first():
            employees_data = [
                {"nombre": "Juan Pérez", "area": "Contabilidad", "correo": "juan.perez@supportdesk.it", "telefono": "3001234567"},
                {"nombre": "María Gómez", "area": "Recursos Humanos", "correo": "maria.gomez@supportdesk.it", "telefono": "3007654321"},
                {"nombre": "Carlos Ruiz", "area": "Operaciones", "correo": "carlos.ruiz@supportdesk.it", "telefono": "3019876543"},
                {"nombre": "Laura Beltrán", "area": "Ventas", "correo": "laura.beltran@supportdesk.it", "telefono": "3023456789"}
            ]
            for emp in employees_data:
                db.session.add(Empleado(**emp))
            print("Empleados iniciales creados.")
        db.session.commit()

        # Obtener empleados de referencia
        emp_juan = Empleado.query.filter_by(nombre="Juan Pérez").first()
        emp_maria = Empleado.query.filter_by(nombre="María Gómez").first()
        emp_carlos = Empleado.query.filter_by(nombre="Carlos Ruiz").first()
        emp_laura = Empleado.query.filter_by(nombre="Laura Beltrán").first()

        # 4. Crear técnicos si la tabla está vacía
        if not Tecnico.query.first():
            technicians_data = [
                {"nombre": "Luis Torres", "especialidad": "Hardware y Soporte Físico", "estado": "activo"},
                {"nombre": "Ana Martínez", "especialidad": "Redes y Conectividad", "estado": "activo"},
                {"nombre": "Jorge Díaz", "especialidad": "Sistemas de Software", "estado": "activo"}
            ]
            for tech in technicians_data:
                db.session.add(Tecnico(**tech))
            print("Técnicos iniciales creados.")
        db.session.commit()

        # Obtener técnicos de referencia
        tech_luis = Tecnico.query.filter_by(nombre="Luis Torres").first()
        tech_ana = Tecnico.query.filter_by(nombre="Ana Martínez").first()
        tech_jorge = Tecnico.query.filter_by(nombre="Jorge Díaz").first()

        # 5. Crear tickets de prueba si no existen
        if not Ticket.query.first():
            # Fechas relativas para simulaciones realistas
            ahora = datetime.utcnow()
            hace_5_dias = ahora - timedelta(days=5)
            hace_4_dias = ahora - timedelta(days=4)
            hace_3_dias = ahora - timedelta(days=3)
            hace_2_dias = ahora - timedelta(days=2)
            hace_1_dia = ahora - timedelta(days=1)

            # Ticket 1: En progreso
            t1 = Ticket(
                descripcion="La pantalla de la computadora portátil no enciende, se escucha el ventilador pero no da video tras una caída menor.",
                prioridad="Alta",
                estado="En progreso",
                fecha_creacion=hace_3_dias,
                empleado_id=emp_juan.id,
                categoria_id=cat_hw.id
            )
            t1.tecnicos_asignados.append(tech_luis)
            db.session.add(t1)

            # Ticket 2: Abierto (sin técnico asignado aún)
            t2 = Ticket(
                descripcion="No puedo ingresar a mi correo corporativo en Outlook, sale error constante de contraseña inválida o cuenta bloqueada.",
                prioridad="Media",
                estado="Abierto",
                fecha_creacion=hace_1_dia,
                empleado_id=emp_maria.id,
                categoria_id=cat_acc.id
            )
            db.session.add(t2)

            # Ticket 3: Resuelto (con intervención)
            t3 = Ticket(
                descripcion="La impresora multifuncional de red del área de Ventas no responde ni conecta por wifi corporativo.",
                prioridad="Crítica",
                estado="Resuelto",
                fecha_creacion=hace_5_dias,
                fecha_cierre=hace_3_dias,
                empleado_id=emp_laura.id,
                categoria_id=cat_red.id
            )
            t3.tecnicos_asignados.append(tech_ana)
            db.session.add(t3)

            # Ticket 4: Cerrado (con intervención)
            t4 = Ticket(
                descripcion="Instalación del software ERP y configuración de firma digital requeridos para el cierre contable del mes.",
                prioridad="Baja",
                estado="Cerrado",
                fecha_creacion=hace_5_dias,
                fecha_cierre=hace_4_dias,
                empleado_id=emp_carlos.id,
                categoria_id=cat_sw.id
            )
            t4.tecnicos_asignados.append(tech_jorge)
            db.session.add(t4)

            # Guardar tickets para obtener sus IDs y crear las intervenciones asociadas
            db.session.commit()

            # 6. Crear intervenciones para tickets cerrados/resueltos
            i1 = Intervencion(
                ticket_id=t3.id,
                tecnico_id=tech_ana.id,
                descripcion="Se verificó el router de red de Ventas. Se detectó colisión de IP con otro dispositivo. Se reconfiguró una dirección IP estática en la impresora y se actualizaron los drivers en las estaciones de trabajo de los usuarios.",
                fecha=hace_4_dias
            )
            db.session.add(i1)

            i2 = Intervencion(
                ticket_id=t4.id,
                tecnico_id=tech_jorge.id,
                descripcion="Se instaló el cliente ERP versión 4.2.1, se importó el certificado digital proporcionado por la autoridad contable en el navegador Chrome del usuario y se realizó prueba de timbrado de facturas con éxito.",
                fecha=hace_4_dias
            )
            db.session.add(i2)
            
            print("Tickets de prueba e intervenciones creadas con éxito.")
            
        db.session.commit()
        print("Seed de base de datos completado exitosamente.")

if __name__ == '__main__':
    seed()
