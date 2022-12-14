"""
@author: smilex
THIS IS A STANDALONE CODE!
"""

#libraries
import numpy as np
import itertools
import matplotlib.pyplot as plt

#--------------------------------------------------
#parameters
J = 1
T = 1
ext = np.linspace(-1., 1., 50) #equally spaced values between -1 and 1 for the external magnetic field

#set total number of lattice points (N)
#N = 5 #fixed N - removed in final push
N = np.array([1, 5, 10, 20]) #considering 4 different values for N
Ninf = 500 #large N limit for the analytical calculation
#important remark: larges values of Ninf (even Ninf = 1000) results in NaN values for magnetisation.
#this needs to be investigated!
Ndep = np.arange(1, 21)
#--------------------------------------------------

#--------------------------------------------------
#functions
def ham(spins, h = 0):
    """"Given all possible spin states,
    this function returns an array containing the correspoding energies"""
    n = len(spins[0])
    Ha = -J*np.sum(spins[:,:n-1]*spins[:,1:], axis=1) - h*np.sum(spins, axis=1)
    return Ha

def partition(hamiltonian):
    """Given an array of energy of all possible spin states,
    this function returns the partition function"""
    Z = np.sum(np.exp(-1*hamiltonian/T))
    return Z

def mag_exact(N, h):
    """This function returns the analytical value of magnetisation,
    for a given number of lattice points and external field.
    courtesy: Dongjin"""
    return T*np.sinh(h/T)*( (np.sqrt(np.sinh(h/T)**2 + np.exp(-4*J/T)) + np.cosh(h/T))**N - (np.cosh(h/T) - np.sqrt(np.sinh(h/T)**2 + np.exp(-4*J/T)))**N ) \
 /( np.sqrt(np.sinh(h/T)**2 + np.exp(-4*J/T))* ((np.sqrt(np.sinh(h/T)**2 + np.exp(-4*J/T)) + np.cosh(h/T))**N + (np.cosh(h/T) - np.sqrt(np.sinh(h/T)**2 + np.exp(-4*J/T)))**N ) ) 
#--------------------------------------------------

#--------------------------------------------------
#magnetisation - numerical calculations
mag = np.zeros([len(N), len(ext)]) #create a zero matrix to store magnetisation values
for j in range(len(N)):
    #generate all possible spin states for the particular N
    spinstates = np.array([list(i) for i in itertools.product([-1, 1], repeat=N[j])])
    #calculate average spin
    avgspin = np.sum(spinstates, axis = 1)/N[j]
    #iterate over different values of the external field for a particular value of N
    for i in range(len(ext)):
        #calculate the energy of each state
        energy = ham(spinstates, ext[i]) #we have an array containing the energy corresponding to each state
        #calculate the probability of each state    
        probability = np.exp(-1*energy/T)/partition(energy)
        #sanity check below - removed in final push
        #print("Sanity Check: Total probability = ", np.sum(probability))
        mag[j, i] = np.sum(avgspin*probability) #every row contains the magnetisation values for a particular N

#magnetisation - analytical calucations
mag2 = np.zeros([len(N), len(ext)])
for j in range(len(N)):
    for i in range(len(ext)):
        mag2[j, i] = mag_exact(N[j], ext[i])

#magnetisation - analytical large N limit
maginf = np.zeros([len(ext)])
for i in range(len(ext)):
    maginf[i] = mag_exact(Ninf, ext[i])
#--------------------------------------------------

#--------------------------------------------------
#errors
print('Magnetisaion vs. External magnetic field --- Errors')
for i in range(len(N)):
    error = np.abs(np.mean((mag[i]-mag2[i])/mag2[i]))*100
    print(f'N={N[i]}: {np.round(error, 3)}%')
#--------------------------------------------------

#--------------------------------------------------
#magnetisation - N dependence
magN = np.zeros([len(Ndep)])
hNdep = 1 #set h value for N dependence - both numerical and analytical results
for j in range(len(Ndep)):
    spinstates = np.array([list(i) for i in itertools.product([-1, 1], repeat=Ndep[j])])
    avgspin = np.sum(spinstates, axis = 1)/Ndep[j]
    energy = ham(spinstates, hNdep)
    probability = np.exp(-1*energy/T)/partition(energy)
    magN[j] = np.sum(avgspin*probability)

#magnetisation - N dependence analytical
magN2 = np.zeros([len(Ndep)])
for j in range(len(Ndep)):
    magN2[j] = mag_exact(Ndep[j], hNdep)
#--------------------------------------------------

#--------------------------------------------------
#errors
print('Magnetisaion vs. Lattic size --- Errors')
for i in range(len(Ndep)):
    error = np.abs(np.mean((magN[i]-magN2[i])/magN2[i]))*100
    print(f'N={Ndep[i]}: {np.round(error, 3)}%')
#--------------------------------------------------

#--------------------------------------------------
#---PLOTS---
#analytical results
#magnetisation vs. external magnetic field
for i in range(len(N)):
    plt.plot(ext, mag2[i], label=f'N={N[i]}')
    plt.legend()
plt.xlabel('Externel magnetic field')
plt.ylabel('Magnetisation')
plt.title('Magnetisation (Analytical) vs. External magnetic field')
plt.show()

#magnetisation vs. lattice size
plt.plot(Ndep, magN2, 'o', label=f'h={hNdep}')
plt.legend()
plt.xlabel('Lattice size')
plt.xticks(range(0,21))
plt.ylabel('Magnetisation')
plt.title('Magnetisation (Analytical) vs. External magnetic field')
plt.grid()
plt.show()

#numerical results
#magnetisation vs. external magnetic field
for i in range(len(N)):
    plt.plot(ext, mag[i], label=f'N={N[i]}')
    plt.legend()
plt.plot(ext, maginf, label='N $\\to$ $\\infty$ (analytical)')
plt.legend()
plt.xlabel('Externel magnetic field')
plt.ylabel('Magnetisation')
plt.title('Magnetisation (Numerical) vs. External magnetic field')
plt.show()

#magnetisation vs. lattice size
plt.plot(Ndep, magN, 'o', label=f'h={hNdep}')
plt.legend()
plt.xlabel('Lattice size')
plt.xticks(range(0,21))
plt.ylabel('Magnetisation')
plt.title('Magnetisation (Numerical) vs. External magnetic field')
plt.grid()
plt.show()