import streamlit as st
from funciones import carga_de_datos, filtrar_datos, preparar_analisis

st.set_page_config(page_title="Analisis de Ventas", page_icon="💻",layout="wide")

df = carga_de_datos()

st.title("Analisis de Ventas de productos tecnologicos.")
st.write("Bienvenido a la aplicacion de analisis de ventas de porductos tegnologicos.")

Inicio,Exploracion,Analisis = st.tabs(["Inicio","Exploracion","Analisis"])

with Inicio:
    st.header("Mis datos de ventas")
    st.write("El data set contiene informacion sobre las ventas"
              "de productos tecnologicos,fechas,metodos de pago y otros"
              " detalle relevantes.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("cantidad", f"{len(df):,}")
    c2.metric("Ingresos totales", f"{df["total_venta"].sum():,}")
    c3.metric("Promedio de ingresos por mes", f"{df["total_venta"].sum() / df["mes"].nunique():,.2f}")
    c4.metric("Unidades totales vendidas", f"{df["Cantidad"].sum():,}")
    c5.metric("Promedio unidades vendidas por mes", f"{df["Cantidad"].sum() / df["mes"].nunique():,}")

st.subheader("Resumen del conjunto de datos")
columnas = ["mes","categoria","Producto","cantidad","total_venta",]
st.dataframe(df[columnas].head(10), use_container_width=True)   

with Exploracion:
    st.header("Exploracion de los datos")
    st.write("Selecciona algunos filtros yobservamos como ocurren los cambios")

    Estacion = st.selectbox("Selecciona la estacion",["Todas"]+ list(df["Estacion N"].unique()))
    Clima = st.selectbox("Selecciona el clima",["Todos"] + list(df["Clima N"].unique()))
    ano = st.selectbox("Selecciona el Ano",["Todos"] + list(df["Ano"].unique()))
    Mes =  st.selectbox("Selecciona el mes",["Todos"] + ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"])

    filtrado = filtrar_datos(df,Estacion, Clima, ano, Mes)
    st.info(f"Se han filtrado {len(filtrado):,} registros.")

    columnas = ["datetime", "Estacion N", "Clima N", "temp", "humidity","count"]
    st.dataframe(filtrado[columnas], use_container_width=True, height=350)

    if st.checkbox("Mostrar resumen estadistico"):
        st.dataframe(filtrado[["temp", "humidity", "windspeed", "count"]].describe().round(2), use_container_width=True)

    if st.checkbox("Mostrar datos faltantes"):
        st.dataframe(filtrado.isnull().sum().to_frame(name="Faltantes"), use_container_width=True)



with Analisis:
    st.header("Análisis descriptivo")
    st.write("Aquí solo visualizamos cómo se distribuyen las rentas de bicicletas en diferentes categorías.")

    opcion = st.selectbox("¿Qué desea analizar?", ["Rentas por mes", "Rentas por hora", "Rentas por estación", "Rentas según el clima"])

    datos_grafico, tipo = preparar_analisis(df, opcion)

    st.subheader(opcion)
    if tipo == "linea":
        st.line_chart(datos_grafico)
    else:
        st.bar_chart(datos_grafico)

    st.dataframe(datos_grafico, use_container_width=True)