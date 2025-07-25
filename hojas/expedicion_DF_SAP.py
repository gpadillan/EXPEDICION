import os
import streamlit as st
import pandas as pd
from hojas.utils.plantilla_utils import generar_documento

# Solo una plantilla por ahora, pero dejamos estructura preparada para más
PLANTILLAS = {
    "SAP": "hojas/plantillas/TITULO_SAP.docx"
}

def run(df: pd.DataFrame):
    st.header("📄 Expedición título - SAP")

    df.columns = df.columns.str.strip()

    columnas_requeridas = [
        "NOMBRE", "APELLIDOS", "DNI ALUMNO", "Nº TITULO",
        "FECHA", "FECHA EXPEDICIÓN", "NOMBRE CURSO EXACTO EN TITULO", "PROMOCION EN LA QUE FINALIZA"
    ]

    if not all(col in df.columns for col in columnas_requeridas):
        st.error("❌ Faltan columnas requeridas en el Excel.")
        st.write("Esperadas:", columnas_requeridas)
        st.write("Encontradas:", list(df.columns))
        return

    df["NOMBRE_COMPLETO"] = df["NOMBRE"].astype(str).str.strip() + " " + df["APELLIDOS"].astype(str).str.strip()

    seleccionado = st.selectbox("Selecciona un alumno", df["NOMBRE_COMPLETO"].unique())
    plantilla_opcion = st.radio("Selecciona plantilla", list(PLANTILLAS.keys()))
    plantilla_path = PLANTILLAS[plantilla_opcion]

    if seleccionado:
        alumno = df[df["NOMBRE_COMPLETO"] == seleccionado].iloc[0]
        st.subheader("📋 Datos del alumno")
        st.write(alumno.astype(str))

        if st.button("🖨️ Generar PDF protegido"):
            try:
                pdf_path = generar_documento(alumno, plantilla_path)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Descargar PDF",
                        f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"❌ Error: {e}")
