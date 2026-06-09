from rich import print
from datetime import datetime 
import funciones
def MostrarMenu():
    # Eliminamos códigos de rich y pegamos a la izquierda para evitar sangrías del editor
    menu = """    ========================================================
           ✨ MENÚ DE OPCIONES - SRP PRÉSTAMOS ✨
    ========================================================
      1. Registrar Usuario
      2. Registrar Préstamo / Inventario
      3. Registrar Devolución o Venta
      4. Consultar Ítems con más de 30 días
      5. Consultar Artículos Prestados
      6. Autorización de Administrador
      7. Salir de la Aplicación
    ========================================================"""
    return menu

# Variables Globales -----------------------------------------
# Reducimos el espaciado para que la línea mida exactamente lo mismo que el letrero
ESPACIADO = 70

# Título ajustado y limpio de etiquetas de rich
titulo = """ ____  ____  ____    ____  ____  _____ ____ _____  _    __  __  ___  ____  
/ ___||  _ \|  _ \  |  _ \|  _ \| ____/ ___|_   _|/ \  |  \/  |/ _ \/ ___| 
\___ \| |_) | |_) | | |_) | |_) |  _| \___ \ | | / _ \ | |\/| | | | \___ \ 
 ___) |  _ <|  __/  |  __/|  _ <| |___ ___) || |/ ___ \| |  | | |_| |___) |
|____/|_| \_\_|     |_|   |_| \_\_____|____/ |_/_/   \_\_|  |_|\___/|____/ """
usuarios = {}
items={}
prestamos={}
devoluciones={}
historico_devoluciones = 0  
historico_ventas = []
OPCIONES_VALIDAS = ['1', '2', '3', '4', '5', '6', '7']
# Variables Globales -----------------------------------------
# inicio del ciclo del menu
while True:
    print('*'*ESPACIADO)
    print(titulo.center(ESPACIADO))
    print('')
    print('..::Bienvenidos::..'.center(ESPACIADO))
    print('*'*ESPACIADO)
    print(MostrarMenu())
    opcion = input('Favor registrar la opcion deseada-->  ')
    if opcion in OPCIONES_VALIDAS:
        match opcion:
            case '1':
                print('\tRegistrar Usuario')
                while True:
                    cedula = input('Favor ingresar la cedula  ')
                    if funciones.ValidarCedula(cedula)==True:
                        break  
                    else:
                        print("La cedula ingresada es incorrecta")
                while True:        
                    nombre = input('El nombre, por fis, ')
                    if funciones.ValidarNombreApellido(nombre)==True:
                        break
                    else:
                        print("El nombre ingresado es invalido")
                while True:        
                    apellido = input('El apellido, por fis, ')
                    if funciones.ValidarNombreApellido(apellido)==True:
                        break
                    else:
                        print("El apellido ingresado  es incorrecto")
                while True:
                    correo = input('El correo por fis, ')
                    if funciones.validar_correo(correo)==True:
                        break
                    else:
                        print("El correo ingresado no es el correcto")
                while True:
                    tiempo = input('Ingresa el tiempo por favor, ')
                    opciones=["5","10","15","30"]
                    if funciones.Validar_Tiempo(tiempo)==True:
                        break
                    else:
                        print("El tiempo ingresado no es el correcto")        
                usuarios[cedula] = {'nombre': nombre,
                                    'apellido': apellido, 
                                    'correo': correo,
                                    'tiempo':int(tiempo)}
                print("[bold green]¡Cargado con exito![/bold green]")
            case '2':
                print('\n\t[bold cyan]:: Registrar Prestamo / Inventario ::[/bold cyan]')
                # CORREGIDO: Usamos sub_opcion para no dañar la variable del menú principal
                sub_opcion = input("Ingresa una opcion:\n1. Para guardar en el inventario\n2. Para prestar segun el Id\n--> ")
                
                if sub_opcion == '1':
                    while True:
                        id_item = input("Ingresa el id del item: ")
                        if len(id_item) < 1:
                            print("Error: El id no puede estar vacio")
                        elif id_item in items or id_item in prestamos:
                            print("Error: El Id ya existe en el sistema")
                        else:
                            break
                    while True:
                        objeto = input("Que objeto vas a registrar: ")
                        if funciones.Validar_objeto(objeto):
                            print(f"El {objeto} fue validado con éxito")
                            break
                        else:
                            print("El nombre del objeto no cumple los parametros")
                    while True:
                        categoria = input("Ingresa la categoria del objeto: ").lower().strip()
                        if funciones.Validar_Categoria(categoria):
                            break
                        else:
                            print("Ingresaste mal la categoria, intenta de nuevo")
                    while True:
                        precio = input("Ingresa el precio: ")
                        if funciones.Validar_precio(precio):
                            break
                        else:
                            print("El precio ingresado no es valido")
                    while True:
                        estado = input("Ingrese el estado del objeto (Excelente, Bueno, Regular, Malo): ").lower().strip()
                        if funciones.Estado(estado):
                            break
                        else:
                            print("Ingresa de nuevo el estado del objeto")
                    
                    # CORREGIDO: El guardado ahora se ejecuta por fuera de los bucles una vez todo es válido
                    items[id_item] = {
                        'Objeto': objeto,
                        'Categoria': categoria,
                        'Precio': float(precio),
                        'Estado': estado
                    }
                    print(f"[bold green]¡El objeto '{objeto}' fue registrado en el inventario con éxito![/bold green]")
                    
                elif sub_opcion == '2':
                    print('\n\t-- Procesar Préstamo de Artículo --')
                    cedula_usuario = input('Ingresa la cédula del usuario: ')
                    id_item = input('Ingresa el ID del ítem a prestar: ')
                    
                    exito = funciones.registrar_prestamo_logica(id_item, cedula_usuario, items, prestamos, usuarios)
                    if exito:
                        print("[bold green]¡Préstamo realizado con éxito y removido del inventario![/bold green]")
                    else:
                        print("[bold yellow]No se pudo procesar el préstamo.[/bold yellow]")
                else:
                    print("Opción inválida dentro de Préstamos.")

            case '3':
                
                print('\n\t[bold cyan]:: Registrar Devolución o Generar Venta ::[/bold cyan]')
                id_item = input('Ingresa el ID del ítem que van a devolver: ')
                
                # 1. Validar si el ítem realmente está prestado
                if id_item not in prestamos:
                    print("[bold red]❌ Error: Este ítem no se encuentra prestado en el sistema de SRP.[/bold red]")
                else:
                    datos_p = prestamos[id_item]
                    cedula_u = datos_p['Cedula_Usuario']
                    nombre_u = usuarios[cedula_u]['nombre']
                    apellido_u = usuarios[cedula_u]['apellido']
                    
                    # 2. CAPTURA DE FECHA MANUAL POR PANTALLA
                    print(f"\nFecha en la que se prestó: [yellow]{datos_p['Fecha_Prestamo'].strftime('%d/%m/%Y')}[/yellow]")
                    
                    while True:
                        fecha_ingresada = input("Ingrese la fecha actual de devolución (Formato: DD/MM/AAAA): ").strip()
                        try:
                            # Convertimos el texto ingresado en pantalla a un objeto datetime real
                            fecha_actual = datetime.strptime(fecha_ingresada, "%d/%m/%Y")
                            
                            # Validar que la fecha de devolución no sea anterior a la de préstamo
                            if fecha_actual < datos_p['Fecha_Prestamo']:
                                print("[red]Error: La fecha de devolución no puede ser menor a la del préstamo.[/red]")
                                continue
                            break
                        except ValueError:
                            print("[red]Formatos de fecha incorrecto. Intente de nuevo usando el formato DD/MM/AAAA.[/red]")
                    
                    # 3. CÁLCULO DE DÍAS TRANSCURRIDOS CON DATETIME
                    fecha_prestamo = datos_p['Fecha_Prestamo']
                    diferencia = fecha_actual - fecha_prestamo
                    dias_transcurridos = diferencia.days 
                    
                    print(f"\n[bold yellow]Procesando transacción para:[/bold yellow] {nombre_u} {apellido_u} (CC: {cedula_u})")
                    print(f"Días de retención calculados: {dias_transcurridos} días")
                    
                    # 4. Regla de negocio: Si supera los 30 días se vende con el 23% de recargo
                    if dias_transcurridos > 30:
                        precio_base = float(datos_p['Precio'])
                        impuesto = precio_base * 0.23 # Impuesto por conchudez
                        total_pagar = precio_base + impuesto
                        
                        # IMPRESIÓN DE LA FACTURA EN PANTALLA
                        print("\n[bold red]==================================================[/bold red]")
                        print("[bold white on red]        SRP PRESTAMOS - FACTURA DE VENTA FORZOSA      [/bold white on red]")
                        print("[bold red]==================================================[/bold red]")
                        print(f"[bold]Cliente:[/bold]   {nombre_u} {apellido_u}")
                        print(f"[bold]Documento:[/bold] {cedula_u}")
                        print(f"[bold]Artículo:[/bold]  {datos_p['Objeto']} (ID: {id_item})")
                        print(f"[bold]Motivo:[/bold]    Superar el límite de 30 días de préstamo")
                        print("[bold red]--------------------------------------------------[/bold red]")
                        print(f" Subtotal (Adquisición):        ${precio_base:.2f}")
                        print(f" Impuesto por Conchudez (23%):  ${impuesto:.2f}")
                        print("[bold red]--------------------------------------------------[/bold red]")
                        print(f" [bold text white on red]TOTAL OBLIGATORIO A PAGAR:     ${total_pagar:.2f}[/bold text white on red]")
                        print("[bold red]==================================================[/bold red]\n")
                        
                        # Se saca de préstamos definitivamente porque ya pasa a ser propiedad del usuario
                        historico_ventas.append({'Total': total_pagar})
                        prestamos.pop(id_item)
                        print("[bold red]⚠️ El artículo ha sido removido de préstamos y marcado como VENDIDO.[/bold red]")
                        
                    else:
                        # Devolución exitosa dentro del tiempo (30 días o menos)
                        datos_retornados = prestamos.pop(id_item)
                        
                        # Se regresa al inventario de artículos disponibles
                        items[id_item] = {
                            'Objeto': datos_retornados['Objeto'],
                            'Categoria': datos_retornados['Categoria'],
                            'Precio': datos_retornados['Precio'],
                            'Estado': datos_retornados['Estado']
                        }
                        
                        # IMPRESIÓN DEL CERTIFICADO EN PANTALLA
                        print("\n[bold green]==================================================[/bold green]")
                        print("[bold white on green]            CERTIFICADO DE DEVOLUCIÓN             [/bold white on green]")
                        print("[bold green]==================================================[/bold green]")
                        print(f"[bold]Usuario:[/bold]    {nombre_u} {apellido_u}")
                        print(f"[bold]Cédula:[/bold]     {cedula_u}")
                        print(f"[bold]Artículo:[/bold]   {datos_retornados['Objeto']} (ID: {id_item})")
                        print(f"[bold]Tiempo útil:[/bold] {dias_transcurridos} días")
                        print(f"[bold]Estado:[/bold]     Devuelto a tiempo y disponible en Inventario")
                        print("[bold green]--------------------------------------------------[/bold green]")
                        print("       ¡Gracias por cuidar las cosas de SRP PRESTAMOS!       ")
                        print("[bold green]==================================================[/bold green]\n")
                        historico_devoluciones += 1
                        print("[bold green]✔️ Devolución asentada con éxito en el sistema.[/bold green]")
            case '4':
                print('\tConsultar Items con mas de 30 dias')
                funciones.consultar_items_mas_30_dias(prestamos, usuarios)
            case '5':
                funciones.consultar_articulos_prestados(prestamos, usuarios)
            case '6':
                print('\tAdministrador')
                funciones.modulo_administrador(usuarios, prestamos, historico_devoluciones, historico_ventas)
            case '7':
                print('Gracias por usar SRP PRESTAMOS')
                break
        
    else:
        error = 'Opcion no disponible, por favor vuelve a intentarlo.'
        print(error)
        continue
