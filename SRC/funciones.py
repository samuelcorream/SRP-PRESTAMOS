from datetime import datetime 
from rich import print
def ValidarNombreApellido(nombre:str)->bool:
    #longitud no puede tener menos de tres letras
    #no puede tener numeros
    longitud = len(nombre)
    if longitud >= 3:
        #la longitud ta ok, ya puedo validar los numeros
        # validador = True
        numeros = '0123456789'
        for letra in nombre:
            if letra in numeros:
                return False
        return True
    else:
        return False

def ValidarCedula(cedula: str) -> bool:
    longitud = len(cedula)
    if longitud >= 3 and longitud <= 15:
        if cedula.isdigit():  # Usamos isdigit() para asegurar que solo sean números
            return True
        else:
            return False
    else:
        return False

def validar_correo(correo):
    correo = correo.strip()
    if " " in correo:
        return False
    if correo.count("@") != 1:
        return False
    partes = correo.split("@")
    usuario = partes[0]
    dominio = partes[1]
    if len(usuario) == 0 or len(dominio) == 0:
        return False
    if dominio.count(".") < 1 or dominio.startswith(".") or dominio.endswith("."):
        return False
    ultimo_punto = dominio.rfind(".")
    extension = dominio[ultimo_punto + 1:]
    if len(extension) < 2:
        return False
    return True
def Validar_Tiempo(tiempo:str)->bool:
    opciones=["5","10","15","30"]
    if tiempo in opciones:
        return True
    else:
        return False
def obtener_fecha_hoy():
    try:
        # Obtiene la fecha y hora actual del sistema
        ahora = datetime.now()
        
        # Formatea la fecha en formato día/mes/año
        fecha_formateada = ahora.strftime("%d/%m/%Y")
        
        return fecha_formateada    
    except Exception as e:
        # Captura cualquier error inesperado
        return f"Error al obtener la fecha: {e}"
def Validar_objeto(objeto:str)->bool:
    longitud=len(objeto)
    if longitud<=3:
        return False
    else:
        return True
def Validar_Categoria(categoria:str)->bool:
    categorias=["videojuegos","libros","musica y video","herramientas","video","dinero","miscelaneo y varios"]
    if categoria in categorias:
        return True
    else:
        return False
def Validar_precio(precio:str)->bool:
    if precio.isnumeric():
        return True
    else:
        return False
def Estado(estado:str)->bool:
    Estados=["excelente","bueno","regular","malo"]
    if estado in Estados:
        return True
    else:
        return False
def registrar_prestamo_logica(id_item: str, cedula_usuario: str, items: dict, prestamos: dict, usuarios: dict) -> bool:
    """
    Controla la transferencia de un ítem del inventario al diccionario de préstamos.
    Retorna True si el préstamo fue exitoso, o False si ocurrió un error.
    """
    if cedula_usuario not in usuarios:
        print("[bold red]Error: El usuario no está registrado en el sistema.[/bold red]")
        return False
    if id_item not in items:
        print("[bold red]¡Error: El ID del ítem no existe en el inventario o ya fue prestado.![/bold red]")
        return False
        
    datos_item = items.pop(id_item)
    
    # MODIFICADO: Guardamos el objeto datetime real y actual de este preciso momento
    fecha_hoy = datetime.now()
    
    prestamos[id_item] = {
        'Objeto': datos_item['Objeto'],
        'Categoria': datos_item['Categoria'],
        'Precio': datos_item['Precio'],
        'Estado': datos_item['Estado'],
        'Cedula_Usuario': cedula_usuario,
        'Fecha_Prestamo': fecha_hoy # Objeto datetime listo para operaciones matemáticas
    }
    return True
    
def consultar_items_mas_30_dias(prestamos: dict, usuarios: dict):
    """
    Recorre los préstamos activos, calcula los días transcurridos
    respecto a la fecha actual (ingresada por pantalla) y muestra
    cuáles superan los 30 días.
    """
    print("\n\t[bold red]:: Artículos con más de 30 días de Préstamo ::[/bold red]")
    
    if len(prestamos) == 0:
        print("[yellow]No hay préstamos registrados en el sistema.[/yellow]")
        return

    # Pedimos la fecha actual por pantalla para calcular los días (igual que en la devolución)
    while True:
        fecha_ingresada = input("Ingrese la fecha actual para verificar (Formato: DD/MM/AAAA): ").strip()
        try:
            fecha_actual = datetime.strptime(fecha_ingresada, "%d/%m/%Y")
            break
        except ValueError:
            print("[red]Formato de fecha incorrecto. Intente de nuevo usando DD/MM/AAAA.[/red]")

    contador_morosos = 0
    print("-" * 60)
    
    # Recorremos el diccionario usando funciones incorporadas (items y ciclos estándar)
    for id_item, datos in prestamos.items():
        fecha_prestamo = datos['Fecha_Prestamo']
        diferencia = fecha_actual - fecha_prestamo
        dias_transcurridos = diferencia.days
        if dias_transcurridos > 30:
            contador_morosos += 1
            cedula_u = datos['Cedula_Usuario']
            nombre_completo = f"{usuarios[cedula_u]['nombre']} {usuarios[cedula_u]['apellido']}"
            
            print(f"[bold]ID Ítem:[/bold] {id_item}")
            print(f"  [b]Objeto:[/b] {datos['Objeto']} | [b]Categoría:[/b] {datos['Categoria']}")
            print(f"  [b]Prestado a:[/b] {nombre_completo} (CC: {cedula_u})")
            print(f"  [b]Días transcurridos:[/b] [red]{dias_transcurridos} días[/red]")
            print("-" * 60)
            
    if contador_morosos == 0:
        print("[green]¡Excelente! Ningún artículo supera los 30 días de préstamo actualmente.[/green]")
def consultar_articulos_prestados(prestamos: dict, usuarios: dict):
    """
    Recorre el diccionario de préstamos activos y muestra en consola
    los detalles del artículo junto con la información del usuario que lo tiene.
    """
    print("\n\t[bold cyan]:: Listado de Artículos Prestados Actualmente ::[/bold cyan]")
    
    # Función incorporada len() para verificar si el diccionario está vacío
    if len(prestamos) == 0:
        print("[yellow]No hay ningún artículo prestado en este momento. ¡Todo está en el inventario![/yellow]")
        return

    print("=" * 65)
    
    # Recorremos los préstamos usando el método incorporado .items()
    for id_item, datos in prestamos.items():
        cedula_u = datos['Cedula_Usuario']
        
        # Obtenemos el nombre y apellido del usuario dueño de esa cédula
        nombre_u = usuarios[cedula_u]['nombre']
        apellido_u = usuarios[cedula_u]['apellido']
        correo_u = usuarios[cedula_u]['correo']
        
        # Formateamos la fecha almacenada para que MJ la lea fácilmente (DD/MM/AAAA)
        fecha_texto = datos['Fecha_Prestamo'].strftime('%d/%m/%Y')
        
        # Impresión de la ficha del artículo prestado
        print(f"[bold]ID Artículo:[/bold]  {id_item}")
        print(f"  [b]Objeto:[/b]        {datos['Objeto']}")
        print(f"  [b]Categoría:[/b]     {datos['Categoria'].capitalize()}")
        print(f"  [b]Valor Inicial:[/b]  ${datos['Precio']:.2f}")
        print(f"  [b]Estado Inicial:[/b] {datos['Estado'].capitalize()}")
        print(f"  [b]Prestado a:[/b]     {nombre_u} {apellido_u} (CC: {cedula_u})")
        print(f"  [b]Contacto:[/b]       {correo_u}")
        print(f"  [b]Fecha Préstamo:[/b] {fecha_texto}")
        print("-" * 65)
        
    print(f"[bold green]Fin del reporte. Total de artículos prestados: {len(prestamos)}[/bold green]\n")
def modulo_administrador(usuarios: dict, prestamos: dict, total_devoluciones: int, lista_ventas: list):
    """
    Caso 6: Menú restringido que calcula estadísticas simples.
    """
    usuario = input("Usuario Administrador: ")
    clave = input("Contraseña: ")
    if usuario != "admin" or clave != "1234":
        print("❌ Acceso denegado. Credenciales incorrectas.")
        return

    # Sumamos los totales de las ventas guardadas
    dinero_ventas = 0.0
    for venta in lista_ventas:
        dinero_ventas += venta['Total']

    print("\n" + "="*50)
    print("      📊 REPORTE DEL PANEL DE ADMINISTRACIÓN      ")
    print("="*50)
    print(f"• Préstamos activos actuales: {len(prestamos)}")
    print(f"• Ítems devueltos con éxito: {total_devoluciones}")
    print(f"• Total de ventas forzosas: {len(lista_ventas)}")
    print(f"• Total dinero recaudado: ${dinero_ventas:.2f}")
    
    print("\n• Lista de usuarios en el sistema:")
    if len(usuarios) == 0:
        print("  No hay usuarios registrados.")
    for cedula, datos in usuarios.items():
        print(f"  - {datos['nombre']} {datos['apellido']} (CC: {cedula})")
    print("="*50 + "\n")
