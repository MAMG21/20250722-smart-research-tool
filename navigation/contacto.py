import streamlit as st

def contact_page():
        # Divide la página en dos columnas: izquierda (1/3) y derecha (2/3)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image("https://www.unbosque.edu.co/sites/default/files/2024-06/logo.svg", width=350)

        with col2:
            st.markdown(
            "<h3 style='text-align: left; color: black; font-size: 35px'>Evaluación de la producción científica de investigadores con métricas y altmétricas a partir de bases de datos bibliográficas dinámicas</h1>",
            unsafe_allow_html=True)

            st.markdown("""
            **Autores del trabajo:**  
            - María Alejandra Marín Galán  
            - Nelson Julián Maya  

            **Dirección académica:**  
            - Director: Prof. Dr. Jorge Enrique García Farieta  
            - Codirector: Prof. Dr. Héctor Javier Hórtua  

            **Programa:**  
            Maestría en Estadística Aplicada y Ciencia de Datos  

            **Institución:**  
            Universidad El Bosque
            """)

            st.markdown(
            "<h3 style='text-align: left; color: black; font-size: 20px'>📞 ¿Deseas contactarnos?</h1>",
            unsafe_allow_html=True)

            st.info("""
            Puedes ponerte en contacto con nosotros a través de los siguientes medios:

            - 📧 Correo de María Alejandra: [mamaring@unbosque.edu.co](mamaring@unbosque.edu.co)  
            - 📧 Correo de Nelson Julián: [njmayag@unal.edu.co](njmayag@unal.edu.co) 
            - 🏫 Universidad El Bosque: [https://www.unbosque.edu.co](https://www.unbosque.edu.co)
            """)

