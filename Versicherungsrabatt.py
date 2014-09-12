# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

# <codecell>

import seaborn as sns
sns.set_style("whitegrid")

# <codecell>

def makebar(krankenkassenbeitrag, rabatt):
    
    if rabatt==-1:
        plt.figure(figsize=(9,4.5))
        plt.xlim(0, 120)
        plt.ylim(0, 10)
        plt.text(60,5,'#Quantifiedself \o/', size=55, ha='center', alpha=0.9)
        plt.savefig('krankenkassenbeitrag-%02d-rabatt.png' % (rabatt+1), dpi=150)
        return 'Done.'
    
    plt.figure(figsize=(9,4.5))
    plt.barh(range(10), krankenkassenbeitrag, edgecolor='k', label='Beitrag', color='#94C600')
    plt.xlim(0, 120)
    plt.xlabel('Krankenkassenbeitrag [%]')
    plt.ylabel('Person')
    plt.axvline(np.mean(krankenkassenbeitrag), label='Mittelwert')
    plt.legend(loc=3)
    
    # Annotations
    plt.text(50,9.1,'#Quantifiedself \o/', size=15, ha='center', alpha=0.9)
    for i in range(len(krankenkassenbeitrag)):
        plt.text(118,i+0.3,'%3.1f%%' % krankenkassenbeitrag[i] , size=10, ha='right', alpha=0.9)

    plt.savefig('krankenkassenbeitrag-%03d-rabatt.png' % (rabatt+1), dpi=150)
    plt.close()

# <codecell>

krankenkassenbeitrag = np.ones(10)*100.0
makebar(krankenkassenbeitrag, -1)

# <codecell>

maxrabatt = 100
for rabatt in range(maxrabatt):
    # Teilnehmerrabatt
    krankenkassenbeitrag[9]-=0.1
    
    # Alle anderen
    krankenkassenbeitrag[0:9]+=0.01
    
    makebar(krankenkassenbeitrag, rabatt)

# <codecell>


# <headingcell level=3>

# Make them to GIF

# <codecell>


# <codecell>

os.system('convert -delay 10 -loop 1 krankenkassenbeitrag*.png krankenkassenbeitrag.gif')
os.system('rm krankenkassenbeitrag*.png')

# <codecell>


