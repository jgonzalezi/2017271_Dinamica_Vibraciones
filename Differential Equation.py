import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#Momento de inercia en kg*m^2
Ix = 7.6925375*10**-8.0
to = 0.008 #espesor
rho = 1250 #Densidad del material
I = Ix*to*rho

#Medidas en m
a = 0.065
b = 0.095
c = 0.01344

#Masas en Kg
m1 = 0.123
m2 = 0.123
m3 = 0.014

#Constante del resorte N/m
ko = 888.83

#Constante del amortiguador
co = 100



#Parámetros de la ecuacion
K = ko*b
C = co*a
M = (m2*a**2.0 + m1*b**2 + m3*c**2.0 + I)/c

#Calculo de wn
wn =(K/M)**0.5

#resolver la ecuacion
lam1 = (-C + (C**2 - 4*M*K)**0.5)/2*M
lam2 = (-C - (C**2 - 4*M*K)**0.5)/2*M

r = lam1.real
wp = lam1.imag

#Hallar la constante de amortiguamiento crítico
Cc = ((4*M*K)**0.5)/a

#Dado por las condiciones iniciales x(0)=0 y x'(0)=0
c1 = 0.01
c2 = 0.0

# Tiempo
t = np.linspace(0, 250, 1000)

if C<Cc:
    # Caso subamortiguado
    phi = np.arctan(c2/(r*c1))
    x = c1 * np.exp(r*t) * np.cos(wp*t - phi)
else:
    # Caso sobreamortiguado o críticamente amortiguado
    x = c1*np.exp(lam1*t)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(t, x)
plt.title('Respuesta del sistema')
plt.xlabel('Tiempo (s)')
plt.ylabel('Desplazamiento (m)')
plt.grid(True)
plt.show()