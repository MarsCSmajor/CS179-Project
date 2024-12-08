import pandas as pd
from itertools import combinations

def load_manifest(file_path):
    with open(file_path, 'r') as f:
        data = [line.strip().split(', ') for line in f.readlines() if line.strip()]

    manifest = pd.DataFrame(data, columns=['Position', 'Weight', 'Container'])
    manifest['Weight_Int'] = manifest['Weight'].apply(lambda w: int(w.strip('{}')) if w != '{00000}' else 0)
    manifest['Position'] = manifest['Position'].fillna('')

    return manifest

def calculate_side_weights(manifest):
    left_positions = r'\[[0-8]{2},(?:0[1-6])\]'
    right_positions = r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]'

    left_weight = manifest[manifest['Position'].str.contains(left_positions, na=False)]['Weight_Int'].sum()
    right_weight = manifest[manifest['Position'].str.contains(right_positions, na=False)]['Weight_Int'].sum()

    return left_weight, right_weight

def rebalance_manifest(manifest):
    updated_manifest = manifest.copy()
    left_weight, right_weight = calculate_side_weights(updated_manifest)

    left_positions = r'\[[0-8]{2},(?:0[1-6])\]'
    left_containers = updated_manifest[
        (updated_manifest['Position'].str.contains(left_positions, na=False)) &
        (updated_manifest['Container'] != 'UNUSED') &
        (updated_manifest['Container'] != 'NAN')
    ]
    right_positions = r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]'
    unused_slots = updated_manifest[
        (updated_manifest['Position'].str.contains(right_positions, na=False)) &
        (updated_manifest['Container'] == 'UNUSED')
    ]

    if unused_slots.empty:
        print("No available slots on the right side to move containers.")
        return updated_manifest

    best_combination = None
    min_difference = float('inf')

    for r in range(1, len(left_containers) + 1):
        for combo in combinations(left_containers.itertuples(), r):
            combo_weight = sum(container.Weight_Int for container in combo)
            new_left_weight = left_weight - combo_weight
            new_right_weight = right_weight + combo_weight
            difference = abs(new_left_weight - new_right_weight)

            if difference <= 0.1 * (new_left_weight + new_right_weight):
                if difference < min_difference:
                    min_difference = difference
                    best_combination = combo

    if best_combination is None:
        print("No valid combination found to balance the ship.")
        return updated_manifest

    for container, (_, slot) in zip(best_combination, unused_slots.iterrows()):
        print(f"\nMoving container {container.Container} from {container.Position} "
              f"to {slot['Position']} with weight {container.Weight_Int}")
        updated_manifest.loc[slot.name, 'Weight'] = f"{{{str(container.Weight_Int).zfill(5)}}}"
        updated_manifest.loc[slot.name, 'Container'] = container.Container
        updated_manifest.loc[container.Index, 'Weight'] = '{00000}'
        updated_manifest.loc[container.Index, 'Container'] = 'UNUSED'

    updated_manifest['Weight_Int'] = updated_manifest['Weight'].apply(lambda w: int(w.strip('{}')))
    return updated_manifest

def save_manifest(manifest, output_file):
    with open(output_file, 'w') as f:
        for _, row in manifest.iterrows():
            position = row['Position']
            weight = row['Weight']
            container = row['Container']
            f.write(f"{position}, {weight}, {container}\n")

def process_manifest(file_path, output_file):
    manifest = load_manifest(file_path)
    left_weight, right_weight = calculate_side_weights(manifest)

    print("\nBefore rebalancing:")
    print(f"Left Weight: {left_weight}, Right Weight: {right_weight}")

    balanced_manifest = rebalance_manifest(manifest)
    left_weight, right_weight = calculate_side_weights(balanced_manifest)

    print("\nAfter rebalancing:")
    print(f"Left Weight: {left_weight}, Right Weight: {right_weight}")

    save_manifest(balanced_manifest, output_file)

if __name__ == "__main__":
    input_file = "case4.txt"
    output_file = "balanced_case4.txt"
    process_manifest(input_file, output_file)
