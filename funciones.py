from pathlib import Path
import pandas as pd


Metodos_de_pago = {
    1:"Efectivo",
    2:"Transferencia",
    3:"Tarjeta de credito",
    4:"Tarjeta de debito"
}


Meses = {
    1:"Enero",
    2:"Febrero",
    3:"Marzo",
    4:"Abril",
    5:"Mayo",
    6:"Junio",
    7:"Julio",
    8:"Agosto",
    9:"Septiembre",
    10:"Octubre",
    11:"Noviembre",
    12:"Diciembre"
}

Categoria = {
    1:"Laptop",
    2:"Gaming",
    3:"Smartphone",
    4:"Tablet",
    5:"Accesorios",
    6:"Monitor",
    7:"Audio"
}


ciudades = {
    1:" Monterrey",
    2:"Guadalajara",
    3:"Ciudad de Mexico",
    4:"Tijuana",
    5:"Puebla",
    6:"Cancun",
    7:"Queretaro",
    8:"Toluca",
    9:"Leon",
    10:"MMerida"
}


def carga_de_datos ():
    ruta = Path(__file__).parent / "ventas_limpias.xlsx"
    df = pd.read_excel(ruta)

    df["fecha"]=pd.to_datetime(df['fecha'])
    df["año"] = df['fecha'].dt.year
    df["mes"] = df['fecha'].dt.month
    df["mes_nombre"] = df["mes"].map(Meses)
    df["metodo_pago"] = df["metodo_pago"].map(Metodos_de_pago)
    df["ciudad"] = df["ciudad"].map(ciudades)

    return df


def filtrar_datos(df,metodo_pago, mes, categoria, ciudad, año):
    resultado = df.copy()

    if metodo_pago != "Todos":
        resultado = resultado[resultado["metodo_pago"] == metodo_pago]

    if mes != "Todos":
         resultado = resultado[resultado["mes_nombre"] == mes]

    if categoria != "Todos":
            resultado = resultado[resultado["categoria"] == categoria]

    if ciudad != "Todos":
        resultado = resultado[resultado["ciudad"] == ciudad]

    if año != "Todos":
         resultado = resultado[resultado["año"] == año]

    return  resultado



def preparar_analisis(df, opcion):
    if opcion == "Ventas por mes":
        datos = df.groupby("mes")["total_ventas"].sum().reindex(range(1,13))
        datos.index = [Meses[i] for i in datos.index]
        return datos.to_frame("Ventas"), "barras"

    if opcion == "Ventas por categoria":
        orden = ["Laptop","Gaming","Smartphone","Tablet","Accesorios","Monitor","Audio"]
        datos = df.groupby("Categoria")["total_ventas"].sum().reindex(orden)
        return datos.to_frame("Ventas"),"barras"


    if opcion == "Ventas por metos de pago":
        orden = ["Efectivo","Transferencia","Tarjeta de credito","Tarjeta de debito"]
        datos = df.groupby("metodo_pago")["total_ventas"].sum().reindex(orden)
        return datos.to_frame("Ventas"),"barras"