import numpy as np


def haversine(coord1, coord2):
    lon1, lat1, lon2, lat2 = map(
        np.radians, [coord1[0], coord1[1], coord2[0], coord2[1]]
    )
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def nearest_neighbor_variant(dist_matrix, start_index, end_index):
    n = len(dist_matrix)
    visited = [False] * n
    path = [start_index]
    visited[start_index] = True

    current = start_index
    while len(path) < n - 1:  # Visit all but the last node (customer)
        next_city = np.argmin(
            [
                (
                    dist_matrix[current][j]
                    if not visited[j] and j != end_index
                    else float("inf")
                )
                for j in range(n)
            ]
        )
        path.append(next_city)
        visited[next_city] = True
        current = next_city

    path.append(end_index)  # Finally, add the customer location to the path
    return path


def calculate_shortest_distance(locations):

    keys = list(locations.keys())
    start_index = keys.index("start")
    end_index = keys.index("end")
    n = len(locations)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = haversine(
                    locations[keys[i]], locations[keys[j]]
                )
    path_indices = nearest_neighbor_variant(distance_matrix, start_index, end_index)
    total_distance = 0
    for i in range(len(path_indices) - 1):
        total_distance += distance_matrix[path_indices[i]][path_indices[i + 1]]
    return round(total_distance, 2)


# path_indices = nearest_neighbor_variant(distance_matrix, start_index, end_index)
# shortest_path = [keys[i] for i in path_indices]

# # Calculate the total distance


# print("Shortest Path:", shortest_path)
# print()
