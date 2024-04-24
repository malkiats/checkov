import json
import sys

def json_to_html(json_file, html_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    html_start = '''
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 10px;
        }
        .report-header {
            background-color: #3165D3; /* Sky blue background */
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 5px; /* Rounded corners */
            margin-bottom: 10px; /* Extra space below the header */
        }
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed; /* Better control over column widths */
            margin: 0 auto; /* Centering table */
            border: 1px solid #ddd; /* Grey border for the whole table */
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd; /* Horizontal line below each row */
        }
        th {
            background-color: #d3d3d3; /* Light gray background for the table header */
            color: black;
        }
        td {
            border-left: 1px solid #ddd; /* Vertical line between columns */
        }
        a {
            color: #007bff; /* Bootstrap default link color */
            text-decoration: none; /* Optional: removes underline from links */
        }
        a:hover {
            text-decoration: underline; /* Reintroduce underline on hover for better accessibility */
        }
    </style>
</head>
<body>
    <div class="report-header">
        <h1>Checkov Scan Results</h1>
    </div>
    <table>
        <thead>
            <tr>
                <th>Check ID</th>
                <th>Description</th>
                <th>File Path</th>
                <th>Line Range</th>
                <th>Result</th>
                <th>Guideline URL</th>
            </tr>
        </thead>
        <tbody>
    '''

    html_end = '''
        </tbody>
    </table>
</body>
</html>
    '''

    rows = ''
    for result in data.get('results', {}).get('failed_checks', []):
        check_id = result['check_id']
        file_path = result['file_path']
        line_range = result.get('file_line_range', [])
        line_range_text = f"{line_range[0]}-{line_range[1]}" if line_range else "No line info"
        result_status = result['check_result']['result']
        description = result['check_name']  # Assuming the description is in 'check_name'
        guideline_url = result.get('guideline', 'No guideline available')

        # Create a clickable link for the guideline URL
        guideline_link = f'<a href="{guideline_url}" target="_blank">{guideline_url}</a>' if guideline_url != 'No guideline available' else 'No guideline available'

        rows += f"<tr><td>{check_id}</td><td>{description}</td><td>{file_path}</td><td>{line_range_text}</td><td>{result_status}</td><td>{guideline_link}</td></tr>\n"

    html_content = html_start + rows + html_end

    with open(html_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    json_to_html(input_file, output_file)
