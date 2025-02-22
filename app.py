import folium
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from geopy.distance import geodesic

# Retail outlet coordinates and names remain the same
outlets = [
    (13.0378748,77.6017724),  # Hebbal
    (13.0215944,77.5508614),  # Yeshwantpur
    (12.9781839,77.6398741),  # Indiranagar
    (12.8583418,77.7808364),  # Sarjapura
    (13.0075813,77.6919984)   # KR Puram
]
outlet_names = ["Hebbal", "Yeshwantpur", "Indiranagar", "Sarjapura", "KR Puram"]

# Previous functions remain the same
def compute_distance_matrix(locations):
    matrix = []
    for from_coord in locations:
        row = []
        for to_coord in locations:
            distance_km = geodesic(from_coord, to_coord).kilometers
            row.append(int(distance_km * 1000))
        matrix.append(row)
    return matrix

def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)
    
    if solution:
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        total_distance = solution.ObjectiveValue() / 1000
        return route, total_distance
    return None, None

def generate_route_table(route, distance_matrix):
    route_info = []
    cumulative_distance = 0.0
    
    for i in range(len(route) - 1):
        from_idx = route[i]
        to_idx = route[i + 1]
        distance = distance_matrix[from_idx][to_idx] / 1000
        cumulative_distance += distance
        route_info.append(
            (outlet_names[from_idx], outlet_names[to_idx], distance, cumulative_distance)
        )
    
    return route_info

def generate_html_table(route_table, total_distance):
    """Generate HTML table with route information."""
    table_html = """
    <div class="route-info">
        <h2>Optimized Route Table</h2>
        <table>
            <thead>
                <tr>
                    <th>From</th>
                    <th>To</th>
                    <th>Distance (km)</th>
                    <th>Cumulative (km)</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for row in route_table:
        table_html += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]:.2f}</td>
                    <td>{row[3]:.2f}</td>
                </tr>
        """
    
    table_html += f"""
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="3"><strong>Total Distance:</strong></td>
                    <td><strong>{total_distance:.2f} km</strong></td>
                </tr>
            </tfoot>
        </table>
    </div>
    """
    return table_html

def create_complete_html(map_html, table_html):
    """Combine map and table into a side-by-side layout."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Optimized Delivery Route</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                display: flex;
                height: 100vh;
            }}
            .map-container {{
                flex: 1;
                height: 100%;
            }}
            .table-container {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background-color: #f5f5f5;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            h2 {{
                color: #333;
                margin-bottom: 20px;
            }}
            tfoot td {{
                font-weight: bold;
                background-color: #f0f0f0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="map-container">
                {map_html}
            </div>
            <div class="table-container">
                {table_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def plot_route_on_map(route, coordinates, outlet_names):
    """Create the map with the optimized route."""
    m = folium.Map(location=coordinates[0], zoom_start=10)
    
    for idx_in_route, node in enumerate(route[:-1], 1):
        icon_html = f"""
        <div style="
            width: 25px; height: 25px;
            border-radius: 50%;
            background-color: white;
            border: 2px solid black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12pt;
            font-weight: bold;
            color: black;
        ">
            {idx_in_route}
        </div>
        """
        
        folium.Marker(
            coordinates[node],
            popup=outlet_names[node],
            icon=folium.DivIcon(html=icon_html)
        ).add_to(m)
    
    route_coords = [coordinates[i] for i in route]
    folium.PolyLine(route_coords, color="blue", weight=3, opacity=0.8).add_to(m)
    
    return m._repr_html_()

# Main execution
distance_matrix = compute_distance_matrix(outlets)
route, total_distance = solve_tsp(distance_matrix)
route_table = generate_route_table(route, distance_matrix)

# Generate map and table HTML
map_html = plot_route_on_map(route, outlets, outlet_names)
table_html = generate_html_table(route_table, total_distance)

# Create and save the complete HTML file
complete_html = create_complete_html(map_html, table_html)
with open("optimized_route_map.html", "w", encoding="utf-8") as f:
    f.write(complete_html)

print("Map and route table saved as optimized_route_map.html")
