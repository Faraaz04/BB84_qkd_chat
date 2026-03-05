#!/home/faraaz/venv/bin/python3.12
import random
import matplotlib
matplotlib.use('GTK4Agg')
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_vector

base_dict = {
    'Z': [[0, 0, 1], [0, 0, -1]], # |0> ,|1>
    'X': [[1, 0, 0], [-1, 0, 0]]  # |+>,|->
}
# secret key
key = [0, 0, 1, 0, 1,1,1,0,1,1]
print(f"no. of bits in key: {len(key)}")
simulator = AerSimulator()
alice_bases = []
alice_results = []
bob_bases = []
bob_results = []
sifted_bases = []
final_key = []

# Start interactive plot
plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')
plot_bloch_vector([0, 0, 1], title="Alice's State", ax=ax1)
plot_bloch_vector([0, 0, 1], title="Bob's State", ax=ax2)
plt.draw()
plt.pause(1)

def basis_plot(basis,i, axis):
    coords = base_dict[basis][i]
    axis.clear() 
    print(f"Basis: {basis}, Bit: {i}")
    plot_bloch_vector(coords, title=f"Basis: {basis} | Bit: {i}", ax=axis)
    plt.draw()   
    plt.pause(1) 
def alice(bit):
    #bit = h 0010 1000
    a_basis = random.choice(list(base_dict.keys()))
    basis_plot(basis=a_basis,i=i,axis=ax1)
    alice_bases.append(a_basis)
    qc = QuantumCircuit(1, 1)
    if a_basis == 'X':
        if bit == 1:
            qc.x(0)  
            qc.h(0)
        else:
            qc.h(0)
    elif a_basis == 'Z':
        if bit ==1:
            qc.x(0)
  
    return qc
    
for i in key:
    qc= alice(i)
    b_basis = random.choice(list(base_dict.keys()))
    basis_plot(basis=b_basis,i=i,axis=ax2)
    bob_bases.append(b_basis)
    if b_basis == 'X':
        qc.h(0)
        qc.measure(0, 0)
    else:
        qc.measure(0,0)
 
    # qc.draw(output='mpl')
    # plt.show()
    
    #Run Simulation
    t_qc = transpile(qc, simulator)
    job = simulator.run(t_qc, shots=1, memory=True)
    result = job.result().get_memory()[0]

# Convert ['1','0'] to int 
    bob_results.append(int(result))
plt.ioff()
plt.show()
print(f"Alice Bases: {alice_bases}")
print(f"Bob Bases:   {bob_bases}")
for i in range(len(key)):
    print(f"matching bases , i: {i}")
    print(f"alice_bases[{i}]: {alice_bases[i]}, bob_bases[{i}]: {bob_bases[i]}")
    if alice_bases[i] == bob_bases[i]:
        sifted_bases.append(alice_bases[i])
        final_key.append(bob_results[i])
final_key = "".join(map(str,final_key))
final_key = bytes(final_key, 'utf-8')
print(f"final bases: {sifted_bases}")
print(f"Key:   {key}")
print(f"final key: {final_key}")

