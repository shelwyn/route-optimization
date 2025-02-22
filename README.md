# Route Optimization Tool for Bangalore Locations

## Overview
This project implements a route optimization solution using Python, specifically designed to find the most efficient path between multiple locations in Bangalore. It solves the Traveling Salesman Problem (TSP) using Google OR-Tools and provides an interactive visualization using Folium maps.

## Features
- Optimizes delivery routes between multiple locations
- Calculates accurate geodesic distances between points
- Generates interactive map visualization
- Provides detailed route information in a table format
- Shows cumulative distance calculations
- Exports results to a single HTML file with side-by-side view

## Prerequisites
- Python 3.8 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shelwyn/route-optimization.git

cd route-optimization-bangalore
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Update the locations in the code:
```python
outlets = [
    (13.0378748,77.6017724),  # Hebbal
    (13.0215944,77.5508614),  # Yeshwantpur
    (12.9781839,77.6398741),  # Indiranagar
    (12.8583418,77.7808364),  # Sarjapura
    (13.0075813,77.6919984)   # KR Puram
]
outlet_names = ["Hebbal", "Yeshwantpur", "Indiranagar", "Sarjapura", "KR Puram"]
```

2. Run the script:
```bash
python app.py
```

3. Open the generated HTML file:
```bash
optimized_route_map.html
```

## Output
The script generates an HTML file containing:
- Interactive map with numbered markers and route visualization
- Table showing route details including:
  - Starting and ending points for each segment
  - Distance between consecutive points
  - Cumulative distance traveled

## Project Structure
```
route-optimization/
│
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
└── optimized_route_map.html  # Generated output (after running script)
```

## How It Works
1. **Distance Calculation**: Uses GeoPy to calculate accurate geodesic distances between locations
2. **Route Optimization**: Implements TSP solution using Google OR-Tools
3. **Visualization**: Creates interactive map using Folium and generates an HTML table
4. **Output Generation**: Combines map and table into a single HTML file with side-by-side layout

## Customization
- Modify the `outlets` list to include different locations
- Adjust the map styling in the `plot_route_on_map` function
- Customize the table appearance in the CSS section of `create_complete_html`

## Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Google OR-Tools for the optimization engine
- Folium for map visualization
- GeoPy for distance calculations

## Contact
For any queries or suggestions, please reach out to [Your Name/Email]
