import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Verdad de tu Sueldo", layout="wide")

# --- ESTILO DESIGN SYSTEM (AZUL NEÓN / DARK MODE) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { color: #00f2ff; font-size: 40px; }
    .stSlider > div > div > div > div { background-color: #00f2ff; }
    .stAlert { background-color: #161b22; border: 1px solid #00f2ff; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #00f2ff; font-family: sans-serif;'>
        <p style='font-size: 0.8rem;'>Desarrollado con 🐍 <b>Python</b> por <b>Osmar Gutierrez</b></p>
        <p style='font-size: 0.7rem; color: #555;'>© 2026 Código Humano | Todos los derechos reservados</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- BARRA LATERAL: INPUTS ---
with st.sidebar:
    st.header("📊 Datos de Auditoría")
    st.markdown("---")
    
    salario_mensual = st.number_input("Salario Mensual Neto (MXN)", min_value=0, value=15000, step=500)
    horas_contrato_semana = st.number_input("Horas por contrato (Semanales)", min_value=1, value=40)
    
    st.subheader("🕵️ Gastos Ocultos (Mensuales)")
    g_ropa = st.number_input("Ropa / Imagen oficina", value=500)
    g_transporte = st.number_input("Transporte / Gasolina", value=2000)
    g_comidas = st.number_input("Comidas fuera", value=1500)
    g_cafe = st.number_input("Café / Antojos", value=600)
    
    st.subheader("👻 Tiempo Fantasma (Semanal)")
    t_trafico = st.slider("Horas de tráfico / Traslado", 0, 20, 5)
    t_estres = st.slider("Horas de estrés / Pendientes en casa", 0, 20, 5)

# --- LÓGICA DE CÁLCULO ---
# Asumimos 4.33 semanas por mes para mayor precisión
semanas_mes = 4.33

# 1. Salario por hora teórico
horas_mes_contrato = horas_contrato_semana * semanas_mes
salario_hora_teorico = salario_mensual / horas_mes_contrato

# 2. Salario real por hora
gastos_totales_mensuales = g_ropa + g_transporte + g_comidas + g_cafe
tiempo_fantasma_semanal = t_trafico + t_estres
horas_reales_mes = (horas_contrato_semana + tiempo_fantasma_semanal) * semanas_mes

salario_real_hora = (salario_mensual - gastos_totales_mensuales) / horas_reales_mes

# --- VISUALIZACIÓN PRINCIPAL ---
st.title("💸 La Verdad de tu Sueldo")
st.markdown("¿Cuánto vale realmente tu hora de vida después de pagar por trabajar?")

# Tarjetas de Métricas
col1, col2 = st.columns(2)
col1.metric("Lo que crees que ganas", f"${salario_hora_teorico:.2f} MXN/hr")
col2.metric("Lo que REALMENTE ganas", f"${salario_real_hora:.2f} MXN/hr")

st.markdown("---")

# Alerta Irónica
# Salario mínimo aproximado en México 2024 es ~$31 MXN/hr (depende de la zona)
if salario_real_hora < 45:
    st.error(f"🛑 **AUDITORÍA COMPLETA:** ¡Ganas menos que un paseador de perros! Tu salario real es de **${salario_real_hora:.2f}**. Estás subsidiando a tu jefe con tu tiempo y dinero.")
elif salario_real_hora < salario_hora_teorico * 0.5:
    st.warning("⚠️ **ALERTA:** Los gastos ocultos y el tiempo fantasma devoraron más del 50% de tu sueldo. Tu libertad está en oferta.")
else:
    st.success("✅ **STATUS:** Tu sueldo real es saludable, pero recuerda que el tiempo es el único recurso que no se recupera.")

# Gráfica de Barras Comparativa
fig = go.Figure()
fig.add_trace(go.Bar(
    x=['Sueldo Teórico', 'Sueldo Real'],
    y=[salario_hora_teorico, salario_real_hora],
    marker_color=['#333333', '#00f2ff'],
    text=[f"${salario_hora_teorico:.2f}", f"${salario_real_hora:.2f}"],
    textposition='auto',
))

fig.update_layout(
    title="Comparativa de Valor por Hora de Vida (MXN)",
    template="plotly_dark",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis_title="Pesos por Hora",
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.caption("Cálculo basado en el tiempo fantasma semanal y gastos operativos de oficina. Código Humano 2026.")