# This code currently:
    # correctly identify all blocking crates
    # correctly move the blocking crates 

import pandas as pd
from itertools import combinations
import re
import heapq

def load_manifest(file_path):
    with open(file_path, 'r') as f:
        data = [line.strip().split(', ') for line in f.readlines() if line.strip()]

    manifest = pd.DataFrame(data, columns=['Position', 'Weight', 'Container'])
    manifest['Weight_Int'] = manifest['Weight'].apply(lambda w: int(w.strip('{}')) if w != '{00000}' else 0)
    manifest['Position'] = manifest['Position'].fillna('')
    manifest['Row'] = manifest['Position'].apply(lambda p: int(re.findall(r'\[(\d+),', p)[0]) if p else None)
    manifest['Col'] = manifest['Position'].apply(lambda p: int(re.findall(r',(\d+)\]', p)[0]) if p else None)

    return manifest

def calculate_estimated_moves(manifest, combo):
    estimated_moves = 0
    for container in combo:
        row, col = container.Row, container.Col
        estimated_moves += (12 - col) 
    return estimated_moves

def calculate_side_weights(manifest):
    left_positions = r'\[[0-8]{2},(?:0[1-6])\]'
    right_positions = r'\[[0-8]{2},(?:0[7-9]|1[0-2])\]'

    left_weight = manifest[manifest['Position'].str.contains(left_positions, na=False)]['Weight_Int'].sum()
    right_weight = manifest[manifest['Position'].str.contains(right_positions, na=False)]['Weight_Int'].sum()

    return left_weight, right_weight

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def move_crate(manifest, from_pos, to_pos, output_file):
    from_index = manifest[(manifest['Row'] == from_pos[0]) & (manifest['Col'] == from_pos[1])].index[0]
    if manifest.loc[from_index, 'Container'] == 'UNUSED':
        return manifest  

    to_index = manifest[(manifest['Row'] == to_pos[0]) & (manifest['Col'] == to_pos[1])].index[0]

    container = manifest.loc[from_index, 'Container']
    weight = manifest.loc[from_index, 'Weight_Int']

    print(f"Moving container {container} from {manifest.loc[from_index, 'Position']} to {manifest.loc[to_index, 'Position']} with weight {weight}")

    manifest.loc[to_index, 'Weight'] = f"{{{str(weight).zfill(5)}}}"
    manifest.loc[to_index, 'Container'] = container
    manifest.loc[from_index, 'Weight'] = '{00000}'
    manifest.loc[from_index, 'Container'] = 'UNUSED'

    # Save after each move
    save_manifest(manifest, output_file)  

    return manifest

def clear_path(manifest, target_position, output_file):
    target_row, target_col = target_position
    blocking_positions = []

    for row in range(target_row + 1, 9):
        blocking_pos = (row, target_col)
        if manifest[(manifest['Row'] == row) & (manifest['Col'] == target_col) & (manifest['Container'] != 'UNUSED')].empty:
            break

        blocking_positions.append(blocking_pos) 

    if blocking_positions:
        print("Crates blocking the path:", [f"[{row},{col}]" for row, col in blocking_positions])

    for blocking_pos in reversed(blocking_positions): 
        unused_slots = manifest[manifest['Container'] == 'UNUSED']
        if unused_slots.empty:
            print(f"No available slots to move blocking crate at [{blocking_pos[0]},{blocking_pos[1]}].")
            return manifest

        best_slot = None
        min_distance = float('inf')

        for _, slot in unused_slots.iterrows():
            slot_pos = (slot['Row'], slot['Col'])
            distance = manhattan_distance(blocking_pos, slot_pos)
            if distance < min_distance:
                min_distance = distance
                best_slot = slot_pos
        
        best_row, best_col = best_slot
        while best_row > 0:
            next_row = best_row -1
            
            if manifest[(manifest['Row'] == next_row) & (manifest['Col'] == best_col) & (manifest['Container'] == 'UNUSED')].empty:
                break
            else:
                best_row = next_row
                
        best_slot = (best_row, best_col)

        manifest = move_crate(manifest, blocking_pos, best_slot, output_file)

    return manifest

def rebalance_manifest(manifest, output_file):
    updated_manifest = manifest
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

    best_combinations = []  
    max_combinations_to_track = 100 
    max_containers_in_combination = 48  

    # find a good combination 
    for r in range(1, min(len(left_containers) + 1, max_containers_in_combination + 1)):
        for combo in combinations(left_containers.itertuples(), r):
            combo_weight = sum(container.Weight_Int for container in combo)

            new_left_weight = left_weight - combo_weight
            new_right_weight = right_weight + combo_weight
            difference = abs(new_left_weight - new_right_weight)

            if difference > 0.5 * (left_weight + right_weight) :
                continue

            estimated_moves = calculate_estimated_moves(manifest, combo)
            priority = difference + 0.1 * estimated_moves 

            if len(best_combinations) < max_combinations_to_track:
                heapq.heappush(best_combinations, (priority, combo))
            elif priority < best_combinations[0][0]:
                heapq.heapreplace(best_combinations, (priority, combo))

    if not best_combinations:
        print("No valid combination found to balance the ship.")
        return updated_manifest

    best_combination = heapq.heappop(best_combinations)[1]

    unused_slots_df = updated_manifest[(updated_manifest['Position'].str.contains(right_positions, na=False)) &
                                     (updated_manifest['Container'] == 'UNUSED')].copy().reset_index(drop=True)

    for container in best_combination:
        current_position = (container.Row, container.Col)
        updated_manifest = clear_path(updated_manifest, current_position, output_file) 

        if not unused_slots_df.empty:
            slot = unused_slots_df.iloc[0]
            slot_pos = (slot['Row'], slot['Col'])

            updated_manifest = move_crate(updated_manifest, current_position, slot_pos, output_file)
            unused_slots_df = unused_slots_df.iloc[1:].reset_index(drop=True)
        else:
            print("Ran out of available unused slots")

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

    balanced_manifest = rebalance_manifest(manifest, output_file)
    left_weight, right_weight = calculate_side_weights(balanced_manifest)

    print("\nAfter rebalancing:")
    print(f"Left Weight: {left_weight}, Right Weight: {right_weight}")

if __name__ == "__main__":
    input_file = "case6.txt"
    output_file = "balanced_case6.txt"
    process_manifest(input_file, output_file)