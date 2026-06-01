import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib
from legacy.filtro import RaisedCosineFilter

matplotlib.use('TkAgg')
plt.style.use('bmh')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------

# 1) Varios filtros con distintos alpha superpuestos en dominio temporal

alphas = [0.1, 0.25, 0.5, 0.75, 1.0]
span = 6
sps = 8

plt.figure(figsize=(10, 5))

for i, alpha in enumerate(alphas):
    f = RaisedCosineFilter(alpha=alpha, span=span, sps=sps, rrc=False)
    t = np.arange(-len(f.taps)//2, len(f.taps)//2 + 1) / sps
    plt.stem(t[:len(f.taps)], f.taps,
             linefmt=f'C{i}-', markerfmt=f'C{i}o', basefmt=' ',
             label=f'$\\alpha = {alpha}$')

plt.title('Respuesta en tiempo - Filtro RC con distintos $\\alpha$',
          fontsize=16, color='navy')
plt.xlabel('Tiempo [periodos de simbolo]', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'varios_filtros_time.png'), dpi=150)
plt.close()

# ---------------------------------------------------------------------------

# 2) Varios filtros con distintos alpha superpuestos en dominio frecuencial

plt.figure(figsize=(10, 5))

for alpha in alphas:
    f = RaisedCosineFilter(alpha=alpha, span=span, sps=sps, rrc=False)
    H = np.fft.fftshift(np.fft.fft(f.taps, 1024))
    freq = np.linspace(-0.5, 0.5, len(H), endpoint=False)
    plt.plot(freq, 20 * np.log10(np.abs(H) + 1e-6),
             label=f'$\\alpha = {alpha}$')

plt.title('Respuesta en Frecuencia - Filtro RC con distintos $\\alpha$',
          fontsize=16, color='navy')
plt.xlabel('Frecuencia [$\\times\\pi$ rad/muestra]', fontsize=12)
plt.ylabel('Magnitud [dB]', fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'varios_filtros_freq.png'), dpi=150)
plt.close()

# ---------------------------------------------------------------------------

# 3) Comparación RC vs RRC (time + freq lado a lado)

rc = RaisedCosineFilter(alpha=0.25, span=8, sps=8, rrc=False)
rrc = RaisedCosineFilter(alpha=0.25, span=8, sps=8, rrc=True)
t = np.arange(-len(rc.taps)//2, len(rc.taps)//2 + 1) / sps

H_rc = np.fft.fftshift(np.fft.fft(rc.taps, 1024))
H_rrc = np.fft.fftshift(np.fft.fft(rrc.taps, 1024))
freq = np.linspace(-0.5, 0.5, len(H_rc), endpoint=False)

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.stem(t[:len(rc.taps)], rc.taps,
         linefmt='C0-', markerfmt='C0o', basefmt=' ', label='RC')
plt.stem(t[:len(rrc.taps)], rrc.taps,
         linefmt='C1-', markerfmt='C1o', basefmt=' ', label='RRC')
plt.title('Respuesta en tiempo', fontsize=16, color='navy')
plt.xlabel('Tiempo [periodos de simbolo]', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(freq, 20 * np.log10(np.abs(H_rc) + 1e-6), label='RC')
plt.plot(freq, 20 * np.log10(np.abs(H_rrc) + 1e-6), '--', label='RRC')
plt.title('Respuesta en Frecuencia', fontsize=16, color='navy')
plt.xlabel('Frecuencia [$\\times\\pi$ rad/muestra]', fontsize=12)
plt.ylabel('Magnitud [dB]', fontsize=12)
plt.grid(True)
plt.legend()

plt.suptitle('Comparacion RC vs RRC ($\\alpha=0.25$)', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'rc_vs_rrc.png'), dpi=150)
plt.close()
