import streamlit as st

def resource_page():
    st.divider()
    st.markdown(
        "<h3 style='text-align: center; color: black;'>📚 Referencias</h1>",
        unsafe_allow_html=True)
    
    st.markdown("**Artículos académicos**")

    st.markdown("""
    - Hirsch, J. E. (2005). An index to quantify an individual's scientific research output. *Proceedings of the National Academy of Sciences, 102*(46), 16569–16572. https://doi.org/10.1073/pnas.0507655102

    - Egghe, L. (2006). Theory and practise of the g-index. *Scientometrics, 69*(1), 131–152. https://doi.org/10.1007/s11192-006-0144-7

    - Zhang, C.-T. (2009). The e-index, complementing the h-index for excess citations. *PLoS One, 4*(5), e5429. https://doi.org/10.1371/journal.pone.0005429

    - Batista, P. D., Campiteli, M. G., Kinouchi, O., & Martinez, S. (2006). Is it possible to compare researchers with different scientific interests? *Scientometrics, 68*(1), 179–189. https://doi.org/10.1007/s11192-006-0110-7

    - Vinkler, P. (2010). Evaluating research using the relative publication citation impact with special emphasis on self-citations. *Scientometrics, 85*(2), 461–473. https://doi.org/10.1007/s11192-010-0195-7

    - Wang, D., Song, C., & Barabási, A.-L. (2013). Quantifying long-term scientific impact. *Science, 342*(6154), 127–132. https://doi.org/10.1126/science.1237825

    - Kinshuk, Patel, A., & Tadesse, D. (2011). A k-index for quantifying the impact of a researcher's work. *Scientometrics, 89*, 921–935.

    - Pudovkin, A. I. (2022). The fractional h-index: A new metric for scientific-impact assessment. *Journal of Informetrics, 16*(1), 101239.

    - Radicchi, F., Fortunato, S., & Castellano, C. (2009). A new order in the leader board of science. *Proceedings of the National Academy of Sciences, 106*(42), 17658–17663.
    """)

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    st.markdown("**Libros**")

    st.markdown("""
    - Sugimoto, C. R., & Larivière, V. (2018). *Measuring Research: What Everyone Needs to Know®*. Oxford University Press.

    - Garfield, E. (1979). *Citation Indexing: Its Theory and Application in Science, Technology, and Humanities*. Wiley.
    """)

    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    st.markdown("**Manuales / Documentos institucionales**")

    st.markdown("""
    - Ministerio de Ciencia, Tecnología e Innovación (Minciencias). (2024). *Guía de reconocimiento y medición de grupos e investigadores*. Bogotá, Colombia. Recuperado de https://minciencias.gov.co/sites/default/files/ckeditor_files/guia-reconocimiento-y-medicion-de-grupos-e-Investigadores.pdf

    - Google Scholar. (2011). *Google Scholar Metrics*. Recuperado de https://scholar.google.com/intl/en/scholar/metrics.html
    """)
