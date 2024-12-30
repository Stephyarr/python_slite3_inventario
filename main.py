from colorama import Fore, Back, Style, init
import sqlite3

# Iniciar colorama
init(autoreset=True)

# Conexion a la base de datos SQLite y creacion de cursor
# conexion = sqlite3.connect("databaseDatos.db")
conexion = sqlite3.connect("baseDatos.db")
cursor = conexion.cursor()

# Creamos la tabla

cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL
    );
""")
conexion.commit()
# No olvidar comitear los cambios en la base de datos

def menu():
    print("*" * 20)
    print(f"{Fore.GREEN}Menu de Opciones\n")
    print(f"{Back.LIGHTBLUE_EX}1. Agregar Producto ")
    print(f"{Back.LIGHTBLACK_EX}2. Mostrar Todo ")
    print(f"{Back.LIGHTBLUE_EX}3. Modificar Producto ")
    print(f"{Back.LIGHTBLACK_EX}4. Eliminar Producto ")
    print(f"{Back.LIGHTBLUE_EX}5. Reporte Bajo Stock")
    print(f"{Back.LIGHTBLACK_EX}6. Mostrar Producto ") 
    print(f"{Fore.RED}0. Salir ")
    print("*" * 20)

def producto_existe():
    id = int(input("ID del Producto : "))

    cursor.execute(f"""
        SELECT * FROM productos WHERE id = {id}
    """)

    product = cursor.fetchone()
    return product

def registrar_producto():
    print("Alta de Producto")
    
    while True:
        try:
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))

            cursor.execute(f"""
                INSERT INTO productos (nombre, precio, cantidad) VALUES ('{nombre}', {precio}, {cantidad})
                """)
            id = cursor.lastrowid
            
            conexion.commit()
            break
        except:
            print(f"{Back.LIGHTRED_EX}{Fore.BLACK}Error, Nombre Existente en la Base de Datos")

    print(f"{Fore.LIGHTGREEN_EX}Producto '{nombre}' agregada con ID - {id}.")

def mostrar_productos():
    print("Listado de Productos")

    cursor.execute("""
        SELECT * FROM productos
    """)

    productos = cursor.fetchall()

    if len(productos) == 0:
        print(f"{Fore.LIGHTMAGENTA_EX}Aun no tenemos productos cargadas en el sistema.")
    else:
        print("ID".ljust(5) + "nombre".ljust(30) + "precio".ljust(15) + "cantidad")
        
        # recorremos el diccionario
        for producto in productos:
            
            # AJUSTAR LOS INDICES DEBIDO AL NUEVO ID
            print(f"{str(producto[0]).ljust(5)}{producto[1].ljust(30)}{str(producto[2]). ljust(15)}{int(producto[3])}")

def actualizar_producto():

    product = producto_existe()

    if product:
        nuevo_precio = float(input(f"{Fore.BLUE}Precio: "))
        nueva_cantidad = float(input(f"{Fore.BLUE}Nueva cantidad: "))
        cursor.execute(f"""
            UPDATE productos SET cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE id = {product[0]};
        """)
        conexion.commit()

        print(f"{Back.LIGHTGREEN_EX}Producto ID Actulizado!!")
    else:
        print(f"{Fore.RED}El ID no Existe !!")

def eliminar_producto():
   
    product = producto_existe()

    if product:
        cursor.execute(f"""
            DELETE FROM productos WHERE id = {product[0]}
        """)
        print(f"{Back.CYAN}{Fore.BLACK}Se eliminó {product[1]} del listado")
        conexion.commit()
    else:
        print(f"{Fore.RED}El ID no Existe !!")


def reporte_stock():
    print(f"{Fore.BLUE}Listado de Productos Bajo Stock")
    limite = int(input("Limite Bajo stock: "))
    cursor.execute(f"""
        SELECT * FROM productos WHERE cantidad < {limite}
    """)
    productos = cursor.fetchall()

    if len(productos) == 0:
        print(f"{Fore.LIGHTMAGENTA_EX}Aun no tenemos productos con Bajo stock de ({limite}).")
    else:
        print("ID".ljust(5) + "nombre".ljust(30) + "cantidad")
        
        for producto in productos:
            if producto[3] <= limite:
            # AJUSTAR LOS INDICES DEBIDO AL NUEVO ID
                print(f"{str(producto[0]).ljust(5)}{producto[1].ljust(30)}{str(producto[3])}")

def mostrar_product():
    producto = producto_existe()

    if producto != None:
        print(
            f"{Fore.LIGHTYELLOW_EX}Nombre:", producto[1],
            f"{Fore.LIGHTYELLOW_EX}Precio:", producto[2],
            f"{Fore.LIGHTYELLOW_EX}Cantidad:",int(producto[3]), "unidades"
        )
    else:
        print(f"{Fore.LIGHTMAGENTA_EX}Producto no encontrado")
    conexion.close()


while True:
    menu()
    try:
        opcion = input(f"{Fore.BLUE}Ingresa una opcion: ")
        opcion = int(opcion)
    except:
        print(f"{Fore.LIGHTYELLOW_EX}Error! Ingrese una opcion valida")

    if opcion == 0:
                print("Nos vemos!")
                break
    elif opcion == 1:
                registrar_producto()        

    elif opcion == 2:
                mostrar_productos()

    elif opcion == 3:
                actualizar_producto()

    elif opcion == 4:
                eliminar_producto()

    elif opcion == 5:
                reporte_stock()

    elif opcion == 6:
                mostrar_product()
    

print("FIN DEL PROGRAMA")

# Cerramos la conexion a la base de datos al finalizar
conexion.close()