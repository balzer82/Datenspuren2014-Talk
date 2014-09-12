# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sb # for plt styling
%matplotlib inline

# <headingcell level=2>

# Load Data from CSV files

# <codecell>

von = 6.0
bis = 14.0
dt = 0.02
laufen = pd.read_csv('Laufen_mit_Telefon_in_der_Hand.csv', index_col='recordtime')
laufen = laufen[(laufen.index<=bis) & (laufen.index>=von)]
joggen = pd.read_csv('Joggen_mit_Telefon_in_der_Hose.csv', index_col='recordtime')
joggen = joggen[(joggen.index<=bis) & (joggen.index>=von)]
radfahren = pd.read_csv('Radfahren_mit_Telefon_in_der_Hosentasche.csv', index_col='recordtime')
radfahren = radfahren[(radfahren.index<=bis) & (radfahren.index>=von)]
sitzen = pd.read_csv('Sitzen_mit_Telefon_in_der_Hand.csv', index_col='recordtime')
sitzen = sitzen[(sitzen.index<=bis) & (sitzen.index>=von)]

# <codecell>

laufen.tail(5)

# <codecell>

# Put everything in a Dictionary to enumerate through it for easy plotting
data = {}
data['laufen'] = laufen
data['joggen'] = joggen
data['radfahren'] = radfahren
data['sitzen'] = sitzen

# <headingcell level=2>

# Beschleunigungen

# <codecell>

ylim = 2.4

f, ax = plt.subplots(4, sharex=True, figsize=(9,4.5))
for i, activity in enumerate(data):
    data[activity].accelerationX.plot(label='X', ax=ax[i])
    data[activity].accelerationY.plot(label='Y', ax=ax[i])
    data[activity].accelerationZ.plot(label='Z', ax=ax[i])

    ax[i].set_ylabel('[$g$]')
    ax[i].set_title('%s' % activity, fontsize=10) 
    ax[i].set_ylim(-ylim, ylim)
    ax[i].set_xlabel('')

plt.xlabel('Zeit [$s$]')
plt.tight_layout()
plt.savefig('accelerations.png', dpi=150)

# <codecell>


# <headingcell level=2>

# Klassifikator (1)

# <markdowncell>

# $|a| = \sqrt{a_x^2 + a_y^2 + a_z^2}$
# 
# $\Delta a = |a|_{max} - |a|_{min}$ (aus 0.5sek Untervall)

# <codecell>

interval = 0.5

# <codecell>

def acc_classify(ax,ay,az):
    n = interval/dt
    messdauer = ax.index[-1] - ax.index[1]
    
    ares = np.sqrt(ax.values**2 + ay.values**2 + az.values**2)
    
    amean = []
    adiff = []
    for k in range(int(messdauer/interval)+1):
        #print('%.1f - %.1f' % (k*n+1, k*n+n))
        aresk = ares[(k*n+1):(k*n+n)]
        
        amean.append(np.mean(aresk))

        amin = np.min(aresk)
        amax = np.max(aresk)
        
        adiff.append(amax - amin)
        
    return amean, adiff

# <codecell>

colors = ['#FF6700', '#CAF278', '#3E3D2D', '#94C600']


plt.figure(figsize=(9, 4.5))
for i, activity in enumerate(data):
    amean, adiff = acc_classify(data[activity].accelerationX, data[activity].accelerationY, data[activity].accelerationZ)
    plt.scatter(adiff, amean, s=120, edgecolor='k', c=colors[i], label=activity, alpha=0.8)

plt.legend(loc=2)
plt.xlabel(r'$|a|_{max} - |a|_{min}$ in [$g$]')
plt.ylabel(r'$|a|$ in [$g$]')
plt.savefig('scatter.png', dpi=150)

# <codecell>


# <headingcell level=2>

# Drehraten

# <codecell>

ylim = 2.4

f, ax = plt.subplots(4, sharex=True, figsize=(9,4.5))
for i, activity in enumerate(data):
    data[activity].motionRotationRateX.plot(label='um X', ax=ax[i])
    data[activity].motionRotationRateY.plot(label='um Y', ax=ax[i])
    data[activity].motionRotationRateZ.plot(label='um Z', ax=ax[i])

    ax[i].set_ylabel(r'[$\frac{rad}{s}$]')
    ax[i].set_title('%s' % activity, fontsize=10) 
    ax[i].set_ylim(-ylim, ylim)
    ax[i].set_xlabel('')

plt.xlabel('Zeit [$s$]')
plt.tight_layout()
plt.savefig('rotationrates.png', dpi=150)

# <headingcell level=2>

# Klassifikator (2)

# <codecell>

def rot_classify(rx,ry,rz):
    interval = 2.05
    n = interval/dt
    messdauer = rx.index[-1] - rx.index[1]
    
    Rxk = []
    for k in range(int(messdauer/interval)+1):
        #print('%.1f - %.1f' % (k*n+1, k*n+n))
        rxk = rx.values[(k*n+1):(k*n+n)]
        
        hann = np.hanning(len(rxk)) # Anti-Aliasing Fensterung
        Rxk.append(np.fft.fft(hann*rxk)) # FFT
        
    return Rxk

# <codecell>

plt.figure(figsize=(9, 4.5))
for i, activity in enumerate(data):
    
    if activity == 'radfahren' or activity == 'laufen':
        Rxk = rot_classify(data[activity].motionRotationRateX, data[activity].motionRotationRateY, data[activity].motionRotationRateZ)

        # Frequenzachse
        N = len(Rxk[0])/2.0+1
        fa = 1.0/dt
        f = np.linspace(0, fa/2.0, N, endpoint=True)

        # Amplitude
        R = 2.0*np.abs(Rxk[1][:N]/N)

        plt.bar(f, R, width=0.5, label=activity, color=colors[i], alpha=0.7, edgecolor='k', align='center')

plt.xlabel(r'Frequenz [$Hz$]')
plt.xlim(0, np.max(f))
plt.ylabel(r'Amplitude [$rad/s$]')
    
plt.legend()
plt.savefig('FFT.png', dpi=150)

