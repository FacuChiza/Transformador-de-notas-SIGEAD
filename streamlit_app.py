import openpyxl
import streamlit as st
import pandas as pd
from PIL import Image

def redondear_nota(nota):
    try:
        if nota > 10:
            nota = nota / 10
        nota = round(nota, 1)
        return round(nota)
    except (ValueError, TypeError):
        return "Ausente"

def centrar_contenido():
    st.markdown(
        """
        <style>
        .stDataFrame { 
            margin: auto; 
        }
        .stMarkdown { 
            text-align: center; 
        }
        .block-container {
            padding-top: 40px;
            max-width: 80%; 
            padding-left: 10%;
            padding-right: 10%;
        }

        input:focus {
            outline: 2px solid #ffffff !important; 
            border-color: #ffffff !important; 
        }

        textarea:focus {
            outline: 2px solid #ffffff !important;
            border-color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


centrar_contenido()

st.title("Transformador de Planillas SIGEAD")

uploaded_file = st.file_uploader("Sube tu archivo Excel o ODS", type=["xlsx", "ods"])

nombre_materia = st.text_input("Nombre de la Materia", help="Ingrese el nombre completo de la materia.")
codigo_materia = st.text_input("Código de Materia", help="Ingrese el código de la materia asociado a las notas.")

if uploaded_file and nombre_materia and codigo_materia:
    try:
        file_extension = uploaded_file.name.split(".")[-1]
        file_extension = f".{file_extension}"
        if file_extension == ".xlsx":
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif file_extension == ".ods":
            df = pd.read_excel(uploaded_file, engine="odf")
        else:
            raise ValueError("Formato no soportado.")

        df.columns = ["Nom", "Ape", "Num", "Inst", "Depa", "Cues", "Ult"]
        df = df.drop(columns=["Nom", "Ape", "Inst", "Ult"])
        df.columns = ["Personal", "CursadaId", "Nota"]
        df["Nota"] = df["Nota"].apply(redondear_nota)
        df["CursadaId"] = codigo_materia

        st.write("Previsualización del archivo procesado:")
        st.dataframe(df, height=600, width=1000) 


        archivo_nombre = f"Archivo_Transformado_{nombre_materia}.csv"
        st.download_button(
            label="Descargar archivo transformado",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=archivo_nombre,
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error al procesar el archivo, por favor revise los datos o nombres de las columnas.           Aquí se muestra un ejemplo del formato correcto")
        imagen = Image.open("static/css/images/ejemplo.png")
        st.image(imagen, caption="Ejemplo de formato correcto", use_container_width=True)
