import pandas as pd

# This code currently takes in manifest (testcase) and outputs a new file with the balanced manifest
# TODOLIST:
    # Greedy Movement for optimizing
    # Generate steps for the operator to follow

def load_manifest(file_path):
    with open(file_path, 'r') as f:
        data = [line.strip().split(', ') for line in f.readlines() if line.strip()]
    manifest = pd.DataFrame(data, columns=['Position', 'Weight', 'Container'])
    return manifest

def parse_weight(weight_str):
    return int(weight_str.strip('{}'))

def calculate_side_weights(manifest):
    manifest['Weight_Int'] = manifest['Weight'].apply(parse_weight)
    
    left_positions = r'\[[0-8]{2},(?:0[1-6])\]'
    right_positions = r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]'
    
    left_weight = manifest[manifest['Position'].str.contains(left_positions)]['Weight_Int'].sum()
    right_weight = manifest[manifest['Position'].str.contains(right_positions)]['Weight_Int'].sum()
    
    return left_weight, right_weight

def rebalance_manifest(manifest, threshold=0.1):
    left_weight, right_weight = calculate_side_weights(manifest)
    total_weight = left_weight + right_weight
    moved_containers = set()  

    while abs(left_weight - right_weight) / total_weight > threshold:
        heavier_side = 'Left' if left_weight > right_weight else 'Right'
        lighter_side = 'Right' if heavier_side == 'Left' else 'Left'
        
        side_columns = r'\[[0-8]{2},(?:0[1-6])\]' if heavier_side == 'Left' else r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]'
        heavy_containers = manifest[
            (manifest['Position'].str.contains(side_columns)) & 
            (manifest['Container'] != 'UNUSED') & 
            (manifest['Container'] != 'NAN')
        ].sort_values(by='Weight_Int', ascending=False)
        
        lighter_columns = r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]' if lighter_side == 'Right' else r'\[[0-8]{2},(?:0[1-6])\]'
        unused_slot = manifest[
            (manifest['Position'].str.contains(lighter_columns)) & 
            (manifest['Container'] == 'UNUSED')
        ]
        
        if not unused_slot.empty and not heavy_containers.empty:
            heaviest_container = heavy_containers.iloc[0]
            if heaviest_container['Container'] in moved_containers:
                print(f"Container {heaviest_container['Container']} already moved. Skipping...")
                break  

            unused_idx = unused_slot.index[0]
            print(f"Moving container {heaviest_container['Container']} "
                  f"from {heaviest_container['Position']} to {manifest.loc[unused_idx, 'Position']}")

            manifest.at[unused_idx, 'Weight'] = heaviest_container['Weight']
            manifest.at[unused_idx, 'Container'] = heaviest_container['Container']
            manifest.at[heaviest_container.name, 'Weight'] = '{00000}'
            manifest.at[heaviest_container.name, 'Container'] = 'UNUSED'

            moved_containers.add(heaviest_container['Container'])
        else:
            print("No valid moves available. Stopping rebalancing...")
            break  

        left_weight, right_weight = calculate_side_weights(manifest)

    return manifest

def save_manifest(manifest, output_file):
    with open(output_file, 'w') as f:
        for _, row in manifest.iterrows():
            f.write(f"{row['Position']}, {row['Weight']}, {row['Container']}\n")

def process_manifest(file_path, output_file):
    print(f"Processing {file_path}...")
    manifest = load_manifest(file_path)
    
    print("\nBefore rebalancing:")
    print(manifest)
    
    balanced_manifest = rebalance_manifest(manifest)
    
    print("\nAfter rebalancing:")
    print(balanced_manifest)
    
    save_manifest(balanced_manifest, output_file)
    print(f"Balanced manifest saved to {output_file}")

if __name__ == "__main__":
    input_file = "case6.txt"
    output_file = "balanced_case6.txt"
    
    process_manifest(input_file, output_file)
