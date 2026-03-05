import random
from qiskit import QuantumCircuit
from qiskit import qpy
import socket
import yaml
import os
#Basis dictionary
#Z:  |0> ,|1>
#X:  |+>,|->
base_dict = {
    'Z': [[0, 0, 1], [0, 0, -1]],
    'X': [[1, 0, 0], [-1, 0, 0]]  
}

def generate_key(msg):
    key = []
    for i in range((len(msg)*8*2)+10):
        key.append(random.choice([0,1]))
    print(f"Total bits in key: {len(key)}")
    return key

def create_quantum_circuit(key):
    alice_bases = []
    alice_circuits = [] 
    for i in range(0, len(key), 8):
        #sub_key = key[i:i+8]
        if len(key[i:i+8]) < 8:
            break
        qc = QuantumCircuit(8, 8)
        for j in range(8):
            a_basis = random.choice(list(base_dict.keys()))
            alice_bases.append(a_basis)
            if a_basis == 'X':
                if key[j] == 1:
                    qc.x(j)  
                    qc.h(j)
                else:
                    qc.h(j)
            elif a_basis == 'Z':
                if key[j] == 1:
                    qc.x(j)
            print(f"Alice encoded byte: {key[i:i+8]}")
        alice_circuits.append(qc)
    return alice_circuits , alice_bases

msg = input("Enter message: ")
key = generate_key(msg)
alice_circuits , alice_bases = create_quantum_circuit(key)

print(f"\nAlice has generated {len(alice_circuits)} circuits (bytes) ready for transmission.")
print(f"key : {key}")
data = {'Basis': alice_bases,
        'Key': key,
        }
folder_path = "/media/faraaz/Data_faru_lnx/College/Physiquest"
qpy_file = os.path.join(folder_path, "alice_quantum.qpy")
yaml_file = os.path.join(folder_path, "alice_classical.yaml")
with open(qpy_file , "wb") as file:
    qpy.dump(alice_circuits, file)
with open(yaml_file, 'w') as file:
    yaml.dump(data,file)
files = [yaml_file, qpy_file]
HOST = 'localhost'
PORT = 8080
for file_path in files:
    with open(file_path, "rb") as f:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT)) 
        s.sendall(f.read())
        s.shutdown(socket.SHUT_WR) # Explicitly signal end of stream
        s.close()