import numpy as np
import matplotlib.pyplot as plt
from legacy.tool.DSPtools import rcosine, resp_freq
from legacy.tool._fixedInt import arrayFixedInt

# Parametros generales
T = 1.0/1.0e9
Nsymb = 1000
os = 8

# Parametros de la respuesta en frecuencia
Nfreqs = 256

# Parametros del filtro de caida cosenoidal
beta = [0.0, 0.5, 1]  # roll-off
Nbauds = 16

# Parametros funcionales
Ts = T/os

# Calculo de tres pusos con diferente roll-off
(t, rc0) = rcosine(beta[0], T, os, Nbauds, Norm=False)
(t, rc1) = rcosine(beta[1], T, os, Nbauds, Norm=False)
(t, rc2) = rcosine(beta[2], T, os, Nbauds, Norm=False)

# 1. Respuesta al impulso

plt.figure(figsize=[14, 6])
plt.plot(t, rc0, 'ro-', linewidth=2.0, label=r'$\beta=0.0$')
plt.plot(t, rc1, 'gs-', linewidth=2.0, label=r'$\beta=0.5$')
plt.plot(t, rc2, 'k^-', linewidth=2.0, label=r'$\beta=1.0$')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.title('Respuesta al impulso de los filtros')
plt.legend()
plt.grid(True)
plt.savefig("../images/impulso.png")

# 2. Respuesta en frecuencia

[H0, A0, F0] = resp_freq(rc0, Ts, Nfreqs)
[H1, A1, F1] = resp_freq(rc1, Ts, Nfreqs)
[H2, A2, F2] = resp_freq(rc2, Ts, Nfreqs)

plt.figure(figsize=[14, 6])
plt.semilogx(F0, 20*np.log10(H0), 'r', linewidth=2.0, label=r'$\beta=0.0$')
plt.semilogx(F1, 20*np.log10(H1), 'g', linewidth=2.0, label=r'$\beta=0.5$')
plt.semilogx(F2, 20*np.log10(H2), 'k', linewidth=2.0, label=r'$\beta=1.0$')

plt.axvline(x=(1.0/Ts)/2.0, color='k', linewidth=1.5,
            linestyle='--', label=r'$F_s/2$')
plt.axvline(x=(1.0/T)/2.0, color='gray', linewidth=1.5,
            linestyle=':', label=r'$F_{baud}/2$')
plt.axhline(y=20*np.log10(0.5), color='k',
            linewidth=1.5, linestyle='-.', label='-6 dB')
plt.legend(loc=3)
plt.grid(True)
plt.title('Respuesta en frecuencia de los filtros')
plt.xlim(F2[1], F2[-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.savefig("../images/frecuencia.png")

# 3. Convolucion de los filtros con los simbolos a transmitir

# 3.1 Generacion de los simbolos a transmitir

symbolsI = 2*(np.random.uniform(-1, 1, Nsymb) > 0.0)-1
symbolsQ = 2*(np.random.uniform(-1, 1, Nsymb) > 0.0)-1

plt.figure(figsize=[14, 6])
plt.title('Distribucion de los simbolos')
plt.subplot(1, 2, 1)
plt.hist(symbolsI, label='Simbolos Re: %d' % Nsymb)
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')
plt.subplot(1, 2, 2)
plt.hist(symbolsQ, label='Simbolos Im: %d' % Nsymb, color='orange')
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')
plt.savefig("../images/simbolos.png")

# 3.2 Generacion de los simbolos a transmitir con ceros intercalados

zsymbI = np.zeros(os*Nsymb)
zsymbI[1:len(zsymbI):int(os)] = symbolsI
zsymbQ = np.zeros(os*Nsymb)
zsymbQ[1:len(zsymbQ):int(os)] = symbolsQ

plt.figure(figsize=[10, 6])
plt.title('Simbolos con ceros intercalados')
plt.subplot(2, 1, 1)
plt.plot(zsymbI, 'o')
plt.xlim(0, 100)
plt.grid(True)
plt.subplot(2, 1, 2)
plt.plot(zsymbQ, 'o', color='orange')
plt.xlim(0, 100)
plt.grid(True)
plt.savefig("../images/simbolos-zeros.png")

# 3.3 Convolucion de los simbolos con el filtro de caida cosenoidal

symb_out0I = np.convolve(rc0, zsymbI, 'same')
symb_out0Q = np.convolve(rc0, zsymbQ, 'same')

symb_out1I = np.convolve(rc1, zsymbI, 'same')
symb_out1Q = np.convolve(rc1, zsymbQ, 'same')

symb_out2I = np.convolve(rc2, zsymbI, 'same')
symb_out2Q = np.convolve(rc2, zsymbQ, 'same')

plt.figure(figsize=[10, 6])
plt.title('Simbolos convolucionados con el filtro de caida cosenoidal')
plt.subplot(2, 1, 1)
plt.plot(symb_out0I, 'r-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[0])
plt.plot(symb_out1I, 'g-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[1])
plt.plot(symb_out2I, 'k-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[2])
plt.xlim(1000, 1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.subplot(2, 1, 2)
plt.plot(symb_out0Q, 'r-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[0])
plt.plot(symb_out1Q, 'g-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[1])
plt.plot(symb_out2Q, 'k-', linewidth=2.0, label=r'$\beta=%2.2f$' % beta[2])
plt.xlim(1000, 1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.savefig("../images/simbolos-filtro.png")

# 3.4 Constelacion con fase optima

offset = 2  # fase optima
symbols = [(symb_out0I, symb_out0Q),
           (symb_out1I, symb_out1Q),
           (symb_out2I, symb_out2Q)]

plt.figure(figsize=[18, 6])
for i, (symbI, symbQ) in enumerate(symbols):
    plt.subplot(1, 3, i+1)
    plt.plot(symbI[100+offset:len(symbI)-(100-offset):os],
             symbQ[100+offset:len(symbQ)-(100-offset):os], '.', color='black')
    plt.title(f'Constelación - $\\beta={beta[i]}$')
    plt.xlabel('I')
    plt.ylabel('Q')
    plt.grid(True)
    plt.axis('equal')
plt.savefig("../images/constelacion.png")

# 4. Cuantización sobre cada filtro de caida cosenoidal

configs = [
    ("S_8-7_truncado", 8, 7, 'trunc'),
    ("S_8-7_redondeado", 8, 7, 'round'),
    ("S_3-2_truncado", 3, 2, 'trunc'),
    ("S_3-2_redondeado", 3, 2, 'round'),
    ("S_6-4_truncado", 6, 4, 'trunc'),
    ("S_6-4_redondeado", 6, 4, 'round')
]

runs = []

for name, int_width, frac_width, mode in configs:
    quantized_rc0 = arrayFixedInt(
        intWidth=int_width, fractWidth=frac_width, N=rc0,
        signedMode='S', roundMode=mode, saturateMode='saturate')
    quantized_rc1 = arrayFixedInt(
        intWidth=int_width, fractWidth=frac_width, N=rc1,
        signedMode='S', roundMode=mode, saturateMode='saturate')
    quantized_rc2 = arrayFixedInt(
        intWidth=int_width, fractWidth=frac_width, N=rc2,
        signedMode='S', roundMode=mode, saturateMode='saturate')
    runs.append((name, quantized_rc0, quantized_rc1, quantized_rc2))

# 5. Graficos de filtros de caida cosenoidal cuantizados en frecuencia

runs_trunc = [r for r in runs if 'truncado' in r[0]]
runs_round = [r for r in runs if 'redondeado' in r[0]]

# 5.1 Respuesta al impulso cuantizada

colores_imp = ['orange', 'green', 'blue']

for label_grupo, grupo in [('truncado', runs_trunc), ('redondeado', runs_round)]:

    imp_data = []
    for name, quantized_rc0, quantized_rc1, quantized_rc2 in grupo:
        rc0_q = np.array([c.fValue for c in quantized_rc0])
        rc1_q = np.array([c.fValue for c in quantized_rc1])
        rc2_q = np.array([c.fValue for c in quantized_rc2])
        imp_data.append((name, rc0_q, rc1_q, rc2_q))

    for beta_idx in range(3):
        plt.figure(figsize=[14, 6])

        rc_orig = [rc0, rc1, rc2][beta_idx]
        plt.plot(t, rc_orig, 'black', linewidth=2.6, label='Original flotante')

        for j, (name, rc0_q, rc1_q, rc2_q) in enumerate(imp_data):
            rc_q = [rc0_q, rc1_q, rc2_q][beta_idx]
            ancho = [3.0, 1.5, 1.5][j]
            plt.plot(t, rc_q, color=colores_imp[j], linewidth=ancho,
                     linestyle='--', label=name)

        plt.title(
            f'Respuesta al impulso {label_grupo} - $\\beta={beta[beta_idx]}$')
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
        plt.grid(True)
        plt.legend(fontsize=9)
        plt.tight_layout()
        plt.savefig(
            f"../images/cuantizaciones/impulso_{label_grupo}_beta{beta_idx}.png")
        plt.close()

# 5.2 Respuesta en frecuencia cuantizada

colores = ['orange', 'green', 'blue']

for label_grupo, grupo in [('truncado', runs_trunc), ('redondeado', runs_round)]:

    freq_data = []
    for name, quantized_rc0, quantized_rc1, quantized_rc2 in grupo:
        rc0_q = np.array([c.fValue for c in quantized_rc0])
        rc1_q = np.array([c.fValue for c in quantized_rc1])
        rc2_q = np.array([c.fValue for c in quantized_rc2])

        [H0_q, _, F0_q] = resp_freq(rc0_q, Ts, Nfreqs)
        [H1_q, _, F1_q] = resp_freq(rc1_q, Ts, Nfreqs)
        [H2_q, _, F2_q] = resp_freq(rc2_q, Ts, Nfreqs)

        freq_data.append((name, H0_q, H1_q, H2_q, F0_q))

    for beta_idx in range(3):
        plt.figure(figsize=[14, 6])

        # Original flotante
        orig_H = [H0, H1, H2][beta_idx]
        plt.semilogx(F0, 20*np.log10(orig_H), 'black', linewidth=2.6,
                     label='Original flotante')

        # Cada cuantización del grupo
        for j, (name, H0_q, H1_q, H2_q, F) in enumerate(freq_data):
            H_q = [H0_q, H1_q, H2_q][beta_idx]
            ancho = [3.0, 1.5, 1.5][j]
            plt.semilogx(F, 20*np.log10(H_q), colores[j % len(colores)],
                         linewidth=ancho, label=f'{name}')

        plt.axvline(x=(1.0/Ts)/2.0, color='k', linewidth=1.5,
                    linestyle='--', label=r'$F_s/2$')
        plt.axvline(x=(1.0/T)/2.0, color='gray', linewidth=1.5,
                    linestyle=':', label=r'$F_{baud}/2$')
        plt.axhline(y=20*np.log10(0.5), color='k',
                    linewidth=1.5, linestyle='-.', label='-6 dB')
        plt.legend(loc=3, fontsize=8)
        plt.grid(True)
        plt.title(
            f'Respuesta en frecuencia {label_grupo} - $\\beta={beta[beta_idx]}$')
        plt.xlim(F2[1], F2[-1])
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dB]')
        plt.tight_layout()
        plt.savefig(
            f"../images/cuantizaciones/frecuencia_{label_grupo}_beta{beta_idx}.png")
        plt.close()

# 5.3 Convolución de los símbolos con los filtros cuantizados

colores_conv = ['orange', 'green', 'blue']

for label_grupo, grupo in [('truncado', runs_trunc), ('redondeado', runs_round)]:

    conv_data = []
    for name, quantized_rc0, quantized_rc1, quantized_rc2 in grupo:
        rc0_q = np.array([c.fValue for c in quantized_rc0])
        rc1_q = np.array([c.fValue for c in quantized_rc1])
        rc2_q = np.array([c.fValue for c in quantized_rc2])

        out0I = np.convolve(rc0_q, zsymbI, 'same')
        out0Q = np.convolve(rc0_q, zsymbQ, 'same')
        out1I = np.convolve(rc1_q, zsymbI, 'same')
        out1Q = np.convolve(rc1_q, zsymbQ, 'same')
        out2I = np.convolve(rc2_q, zsymbI, 'same')
        out2Q = np.convolve(rc2_q, zsymbQ, 'same')

        conv_data.append((name, out0I, out0Q, out1I, out1Q, out2I, out2Q))

    for beta_idx in range(3):
        plt.figure(figsize=[14, 6])

        # Original flotante
        orig_I = [symb_out0I, symb_out1I, symb_out2I][beta_idx]
        orig_Q = [symb_out0Q, symb_out1Q, symb_out2Q][beta_idx]

        plt.subplot(2, 1, 1)
        plt.plot(orig_I, 'black', linewidth=2.6, label='Original flotante')

        # Cada cuantización del grupo
        for j, (name, out0I, out0Q, out1I, out1Q, out2I, out2Q) in enumerate(conv_data):
            out_I = [out0I, out1I, out2I][beta_idx]
            ancho = [3.0, 1.5, 1.5][j]
            plt.plot(out_I, color=colores_conv[j], linewidth=ancho,
                     linestyle='--', label=f'{name}')

        plt.xlim(1000, 1250)
        plt.grid(True)
        plt.legend(fontsize=8)
        plt.title(f'Convolución I - {label_grupo} - $\\beta={beta[beta_idx]}$')
        plt.ylabel('Magnitud')

        plt.subplot(2, 1, 2)
        plt.plot(orig_Q, 'black', linewidth=2.6, label='Original flotante')

        # Cada cuantización del grupo
        for j, (name, out0I, out0Q, out1I, out1Q, out2I, out2Q) in enumerate(conv_data):
            out_Q = [out0Q, out1Q, out2Q][beta_idx]
            ancho = [3.0, 1.5, 1.5][j]
            plt.plot(out_Q, color=colores_conv[j], linewidth=ancho,
                     linestyle='--', label=f'{name}')

        plt.xlim(1000, 1250)
        plt.grid(True)
        plt.legend(fontsize=8)
        plt.title(f'Convolución Q - {label_grupo} - $\\beta={beta[beta_idx]}$')
        plt.xlabel('Muestras')
        plt.ylabel('Magnitud')

        plt.tight_layout()
        plt.savefig(
            f"../images/cuantizaciones/convolucion_{label_grupo}_beta{beta_idx}.png")
        plt.close()

# 5.4 Constelación con filtros cuantizados

for grupo_nombre, grupo in [('truncado', runs_trunc), ('redondeado', runs_round)]:
    # Computo las convoluciones con los filtros cuantizados
    out0I_q = []
    out0Q_q = []
    out1I_q = []
    out1Q_q = []
    out2I_q = []
    out2Q_q = []

    for idx, (_, qrc0, qrc1, qrc2) in enumerate(grupo):
        rc0_q = np.array([c.fValue for c in qrc0])
        rc1_q = np.array([c.fValue for c in qrc1])
        rc2_q = np.array([c.fValue for c in qrc2])

        out0I_q.append(np.convolve(rc0_q, zsymbI, 'same'))
        out0Q_q.append(np.convolve(rc0_q, zsymbQ, 'same'))
        out1I_q.append(np.convolve(rc1_q, zsymbI, 'same'))
        out1Q_q.append(np.convolve(rc1_q, zsymbQ, 'same'))
        out2I_q.append(np.convolve(rc2_q, zsymbI, 'same'))
        out2Q_q.append(np.convolve(rc2_q, zsymbQ, 'same'))

    for beta_idx in range(3):

        if beta_idx == 0:
            origI, origQ = symb_out0I, symb_out0Q
            outI_q, outQ_q = out0I_q, out0Q_q
        elif beta_idx == 1:
            origI, origQ = symb_out1I, symb_out1Q
            outI_q, outQ_q = out1I_q, out1Q_q
        else:
            origI, origQ = symb_out2I, symb_out2Q
            outI_q, outQ_q = out2I_q, out2Q_q

        # Downsampling con fase optima
        pts_origI = origI[100+offset:len(origI)-(100-offset):os]
        pts_origQ = origQ[100+offset:len(origQ)-(100-offset):os]

        pts_qI = []
        pts_qQ = []
        for k in range(3):
            pts_qI.append(outI_q[k][100+offset:len(outI_q[k])-(100-offset):os])
            pts_qQ.append(outQ_q[k][100+offset:len(outQ_q[k])-(100-offset):os])

        # Limites comunes para comparar
        todos = np.concatenate([pts_origI, pts_origQ] + pts_qI + pts_qQ)
        lim = np.max(np.abs(todos)) * 1.15

        fig, axs = plt.subplots(2, 2, figsize=[10, 10])

        axs[0, 0].plot(pts_origI, pts_origQ, 'k.', markersize=3)
        axs[0, 0].set_title('Original flotante')
        axs[0, 0].set_xlim(-lim, lim)
        axs[0, 0].set_ylim(-lim, lim)
        axs[0, 0].set_aspect('equal')
        axs[0, 0].grid(True)

        axs[0, 1].plot(pts_qI[0], pts_qQ[0], '.', color='orange', markersize=3)
        axs[0, 1].set_title('S(8,7)')
        axs[0, 1].set_xlim(-lim, lim)
        axs[0, 1].set_ylim(-lim, lim)
        axs[0, 1].set_aspect('equal')
        axs[0, 1].grid(True)

        axs[1, 0].plot(pts_qI[1], pts_qQ[1], '.', color='green', markersize=3)
        axs[1, 0].set_title('S(3,2)')
        axs[1, 0].set_xlim(-lim, lim)
        axs[1, 0].set_ylim(-lim, lim)
        axs[1, 0].set_aspect('equal')
        axs[1, 0].grid(True)

        axs[1, 1].plot(pts_qI[2], pts_qQ[2], '.', color='blue', markersize=3)
        axs[1, 1].set_title('S(6,4)')
        axs[1, 1].set_xlim(-lim, lim)
        axs[1, 1].set_ylim(-lim, lim)
        axs[1, 1].set_aspect('equal')
        axs[1, 1].grid(True)

        plt.suptitle(
            f'Constelación {grupo_nombre} - $\\beta={beta[beta_idx]}$')
        plt.tight_layout()
        plt.savefig(
            f"../images/cuantizaciones/constelacion_{grupo_nombre}_beta{beta_idx}.png")
        plt.close()
