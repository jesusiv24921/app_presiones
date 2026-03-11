import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.title("Pump Intake Pressure Processor")

file = st.file_uploader("Subir archivo", type=["xlsx","csv"])

pozo = st.text_input("Nombre del pozo", value="CAN236")

if file is not None:

    if file.name.endswith("xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    df = df[['Fecha','Pump Intake Pressure (psia)']].copy()

    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    df['FECHA'] = df['Fecha'].dt.strftime('%Y-%m-%d')

    df = df.dropna()

    # GROUPBY
    data = df.groupby('FECHA')['Pump Intake Pressure (psia)'].mean().reset_index()

    fecha_max = data['FECHA'].max()
    fecha_min = data['FECHA'].min()

    data['Pozo'] = pozo

    data['Pump Intake Pressure (psia)'] = round(
        data['Pump Intake Pressure (psia)']
    ).astype(int)

    st.subheader("Datos procesados")

    st.dataframe(data)

    # GRAFICA
    fig = px.line(
        data,
        x='FECHA',
        y='Pump Intake Pressure (psia)',
        title=f"Pump Intake Pressure - {pozo}"
    )

    st.plotly_chart(fig, use_container_width=True)

    # EXPORTAR
    output_name = f"{pozo}-{fecha_min}-{fecha_max}.xlsx"

    buffer = io.BytesIO()

data.to_excel(buffer, index=False)

buffer.seek(0)

st.download_button(
    "Descargar Excel",
    data=buffer,
    file_name=output_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")