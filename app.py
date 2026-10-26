import streamlit as st
from funciones import carga_de_datos, filtrar_datos, preparar_analisis

st.set_page_config(page_title="Analisis de Ventas", page_icon="💻",layout="wide")

df = carga_de_datos()

st.title("Analisis de Ventas de productos tecnologicos.")
st.write("Bienvenido a la aplicacion de analisis de ventas de porductos tecnologicos.")

Inicio,Exploracion,Analisis = st.tabs(["Inicio","Exploracion","Analisis"])

with Inicio:
    st.header("Mis datos de ventas")
    st.write("El data set contiene informacion sobre las ventas"
              "de productos tecnologicos,fechas,metodos de pago y otros"
              " detalle relevantes.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total transacciones realizadas", f"{len(df):,}")
    c2.metric("Ingresos totales", f"{df["total_venta"].sum():,}")
    c3.metric("Promedio de ingresos por mes", f"{df["total_venta"].sum() / df["mes"].nunique():,.2f}")
    c4.metric("Unidades totales vendidas", f"{df["cantidad"].sum():,}")
    c5.metric("Promedio unidades vendidas por mes", f"{df["cantidad"].sum() / df["mes"].nunique():,}")

    st.subheader("Resumen del conjunto de datos, top 10 productos que generan mas ingresos")
    columnas = [ "fecha","mes_nombre","categoria","producto","cantidad","total_venta"]

    df_ordenado = df.sort_values(
    by="total_venta",
    ascending=False
)

    st.dataframe(
        df_ordenado[columnas].head(12),
        use_container_width=True
    )


with Exploracion:
    st.header("Exploracion de los datos")

    mes = st.selectbox("Selecciona el mes",["Todas"]+ ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"])
    metodo_pago= st.selectbox("Selecciona el metodo de pago",["Todos"] + ["Efectivo","Tarjeta de credito","Tarjeta de debito","Transferencia"])
    año = st.selectbox("Selecciona el año",["Todos"] + list(df["año"].unique()))
    categorias =  st.selectbox("Selecciona la categoria",["Todos"] + ["Laptop","Gaming","Smartphone","Tablet","Accesorios","Monitor","Audio"])
    ciudad = st.selectbox("Selecciona la ciudad",["Todos"] + ["Monterrey","Guadalajara","Ciudad de Mexico","Tijuana","Puebla","Cancun","Queretaro","Toluca","Leon","Merida"])


    filtrado = filtrar_datos(df,metodo_pago	, mes, categorias, ciudad, año)
    st.info(f"Se han filtrado {len(filtrado):,} registros.")

    columnas = ["fecha","producto","cantidad","total_venta"]
    st.dataframe(filtrado[columnas], use_container_width=True, height=350) 


with Analisis:
    st.header("Análisis descriptivo")
    st.write("Aquí solo visualizamos cómo se distribuyen las ventas  en diferentes categorías.")

    opcion = st.selectbox("¿Qué desea analizar?", ["Ingreso total por mes", "Ingreso total por categorias", "Unidades vendidas por producto"])

    if opcion == "Ingreso total por mes":
        datos_grafico = (
            df.groupby("mes_nombre")["total_venta"]
            .sum()
            .reset_index()
        )
        datos_grafico.columns = ["Mes", "Ingresos"]
        tipo ="lineas"

    elif opcion == "Ingreso total por categorias":
        datos_grafico = (
            df.groupby("categoria")["total_venta"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        datos_grafico.columns = ["Categoria", "Ingresos"]
        tipo ="barras"

    else:
        datos_grafico = (
        df.groupby("producto")["cantidad"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

        datos_grafico.columns = ["Producto", "Unidades vendidas"]
        tipo = "horizontal"

    st.subheader(opcion)

    if tipo =="lineas":
        st.line_chart(
        datos_grafico.set_index("Mes")["Ingresos"]
    )
        
    elif tipo =="barras":
        st.bar_chart(
        datos_grafico.set_index(datos_grafico.columns[0])["Ingresos"],
        horizontal=False
    )

    else:
        st.bar_chart(
        datos_grafico.set_index("Producto")["Unidades vendidas"],
        horizontal=True
    )

    st.dataframe(
        datos_grafico,
        use_container_width=True,
        hide_index=True
    )