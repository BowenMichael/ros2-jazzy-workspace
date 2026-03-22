import sys
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rosbags.highlevel import AnyReader

def extract_joint_states(bag_path):
    """Extract joint states from an MCAP bag file into a Pandas DataFrame."""
    data = []
    # Open the bag using AnyReader
    # AnyReader handles all message type registration automatically
    with AnyReader([pathlib.Path(bag_path)]) as reader:
        for connection, timestamp, rawdata in reader.messages():
            if connection.topic == '/joint_states':
                msg = reader.deserialize(rawdata, connection.msgtype)
                # Save timestamp (seconds) and the two joint positions
                data.append({
                    'time': timestamp * 1e-9, 
                    'pos0': msg.position[0], 
                    'pos1': msg.position[1]
                })
    return pd.DataFrame(data)

def analyze_chaos(run_a_path, run_b_path):
    # Load data
    df_a = extract_joint_states(run_a_path)
    df_b = extract_joint_states(run_b_path)
    
    # Ensure they have the same number of messages for comparison
    min_len = min(len(df_a), len(df_b))
    df_a = df_a.iloc[:min_len]
    df_b = df_b.iloc[:min_len]
    
    # Calculate absolute difference (divergence)
    diff = np.abs(df_a['pos0'] - df_b['pos0'])
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df_a['time'] - df_a['time'].iloc[0], df_a['pos0'], color='red', label='run_a (Joint 2)')
    plt.plot(df_a['time'] - df_a['time'].iloc[0], df_b['pos0'], color='green', label='run_b (Joint 2)')
    plt.plot(df_a['time'] - df_a['time'].iloc[0], diff, color='blue', label='Divergence (Joint 2)')
    plt.title('Double Pendulum: Simulation Chaos (Divergence Analysis)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle Difference (radians)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Automatically find all recording folders
    import os
    folders = sorted([f for f in os.listdir('runs') if f.startswith('chaos_recording_')])
    
    if len(folders) >= 2:
        print(f"Comparing {folders[-2]} vs {folders[-1]}")
        analyze_chaos('runs/' + folders[-2], 'runs/' + folders[-1])
    else:
        print(f"Found only {len(folders)} folders. Need at least two.")
        print("Folders found:", folders)
