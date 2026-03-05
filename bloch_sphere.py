import random
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector
base_dict = {
    'Z': [[0, 0, 1], [0, 0, -1]], # |0> ,|1>
    'X': [[1, 0, 0], [-1, 0, 0]]  # |+>,|->
}

bits = [0, 1, 0, 1]

# Start interactive plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
print("State: |0>")
plot_bloch_vector([0, 0, 1], title="Alice's Current State", ax=ax)
plt.draw()
plt.pause(1)

for b in bits:
    basis_choice = random.choice(list(base_dict.keys()))
    coords = base_dict[basis_choice][b]
    ax.clear() 
    print(f"Basis: {basis_choice}, Bit: {b}")
    plot_bloch_vector(coords, title=f"Basis: {basis_choice} | Bit: {b}", ax=ax)
    plt.draw()   
    plt.pause(1) 

plt.ioff()
plt.show()
