import socket
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit import qpy
import yaml
simulator = AerSimulator()
class Receiver:
    print(f"in Receiver")
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        # Setup the listener once
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(1)
    
    def classic_channel(self):
        conn, addr = self.s.accept()
        full_data = b"" # Buffer to collect bytes
        with open('received.yaml', 'wb') as file: # Use wb for raw network bytes
            while True:
                chunk = conn.recv(4096)
                if not chunk: # This breaks the loop when Alice closes the socket
                    break
                full_data += chunk
                file.write(chunk)
                print(f"receiving yaml chunk...")
        #print(full_data)
        received_data = yaml.safe_load(full_data.decode('utf-8'))
        alice_bases = received_data['Basis']
        key = received_data['Key']
        conn.close() # Note: use conn.close(), not selfelf.conn.close()
        print("YAML received and parsed")
        return alice_bases, key

    def quantum_channel(self):
        conn, addr = self.s.accept()
        with open("received_file.qpy", "wb") as f:
            while True:
                data = conn.recv(4096)
                print(f"receiving qpy")
                if not data: 
                    break
                f.write(data)
        with open("received_file.qpy", "rb") as f:
            circuits = qpy.load(f)
            print(len(circuits))
        conn.close()
        print("QPY received")
        return circuits
    def close_receiver(self):
        self.s.close()
        
def receive_data():
    r = Receiver()
    alice_bases, key = r.classic_channel()
    circuits = r.quantum_channel()
    r.close_receiver()
    return alice_bases , key , circuits
    # --- Measurement Phase ---
def bob_measure(circuits):
    bob_bases = []
    bob_bits = []
    num_circuits = len(circuits)
    print(f"Bob is processing {num_circuits} circuits...")
    for i, qc in enumerate(circuits):
        # Bob chooses 8 random bases for the 8 qubits in this circuit
        bases =  [random.choice(['X', 'Z']) for _ in range(8)]
        bob_bases.extend(bases)
        # Apply basis transformation before measurement
        for qbit_idx in range(8):
            if bob_bases[qbit_idx] == 'X':
                qc.h(qbit_idx)
        qc.measure_all()
        # Execute
        job = simulator.run(transpile(qc, simulator), shots=1)
        result_dict = job.result().get_counts()
        # Extract bitstring (Qiskit LSB is on the right, so we reverse with [::-1])
        bitstring = list(result_dict.keys())[0][::-1]
        clean_bitstring = bitstring.replace(" ", "")[::-1]
        bits = [int(b) for b in clean_bitstring]
        bob_bits.extend(bits)
    return bob_bases , bob_bits
# --- Sifting Phase ---
# Compare alice_bases vs bob_bases
alice_bases, key , circuits = receive_data()
bob_bases, bob_bits = bob_measure(circuits)
final_key_bob = []
for i in range(len(alice_bases)):
    if alice_bases[i] == bob_bases[i]:
        final_key_bob.append(bob_bits[i])
# --- Results ---
print("\n--- Sifting Complete ---")
print(f"Initial bits: {len(bob_bits)}")
print(f"Sifted bits:  {len(final_key_bob)}")
  
    