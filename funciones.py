from pathlib import Path
import pandas as pd


Metodos_de_pago = {
    1:"Efectivo",
    2:"Transferencia",
    3:"Tarjeta de credito",
    4:"Tarjeta de débito"
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
    0:"Laptop",
    1:"Gaming",
    2:"Smartphone",
    3:"Tablet",
    4:"Accesorios",
    5:"Monitor",
    6:"Audio",
    
}


def carga_de_datos ():
    ruta = Path(__file__).parent / "ventas_limpias.csv"
    df = pd.read_csv(ruta)

    df["datetime"]=pd.to_datetime(df["datetime"])
    df["año"] = df["datetime"].dt.year
    df["mes"] = df["datetime"].dt.month
    df["mes_nombre"] = df["mes"].map(Meses)
    df["metodo_pago"] = df["metodo_pago"].map(Metodos_de_pago)

    return df


def filtrar_datos(df,Metodos_de_pago, Meses, Categoria):
    resultado = df.copy()

    if Metodos_de_pago != "Todos":
        resultado = resultado[resultado["metodo_pago"] == Metodos_de_pago]

    if Meses != "Todos":
         resultado = resultado[resultado["mes_nombre"] == Meses]

    if Categoria != "Todos":
            resultado = resultado[resultado["Categoria"] == Categoria]

    if año != "Todos":
         resultado = resultado[resultado["año"] == año]

    return  resultado



def preparar_analisis(df, opcion):
    if opcion == "Ventas por mes":
        datos = df.groupby("mes")["total_ventas"].sum().reindex(range(1,13))
        datos.index = [Meses[i] for i in datos.index]
        return datos.to_frame("Ventas"), "barras"

    if opcion == "Ventas por categoria":
        orden = ["laptop","gaming","smartphone","tablet","accesorios","monitor","audio"]
        datos = df.groupby("Categoria")["total_ventas"].sum().reindex(orden)
        return datos.to_frame("Ventas"),"barras"


    if opcion == "Ventas por metos de pago":
        orden = ["Efectivo","Transferencia","Tarjeta de credito","Tarjeta de débito"]
        datos = df.groupby("metodo_pago")["total_ventas"].sum().reindex(orden)
        return datos.to_frame("Ventas"),"barras"