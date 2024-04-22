# PURPOSE: Create tables for front-end
from flask import Flask, request, jsonify

app = Flask(__name__)

# HOME PAGE TABLE FORMATING
@app.route('/homepage', methods=['POST'])
def homepage_format():
    data = request.get_json()  # This parses the incoming JSON into a Python dictionary
    rows = data.get('rows')
    print("homepage row", rows)
    if not rows:
        return jsonify({"error": "Missing rows data"}), 400

    # Assuming 'rows' is a list of lists, where each list represents a row in the table
    try:
        table = render_homepage_table(rows)
        return table, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def render_homepage_table(rows):
    # Base structure for the table, including headers
    table_html = """
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Patient ID</th>
          <th scope="col">Username</th>
          <th scope="col">Password</th>
          <th scope="col">Email</th>
          <th scope="col">Role</th>
          <th scope="col">Appointment Time</th>
          <th scope="col">Amount Due</th>
        </tr>
      </thead>
      <tbody>
    """
    
    try:
        for row in rows:
            table_html += "<tr>"
            for column in row:
                table_html += f"<td>{column}</td>"
            table_html += "</tr>"
    except Exception as e:
        table_html += """
        <tr>
          <td colspan="8" style="text-align: center;">An error occurred while generating the table: {e}</td>
        </tr>
        """.format(e=e)
    
    table_html += "</tbody></table>"
    return table_html

# VISITS PAGE TABLE FORMATING
@app.route('/visits_table', methods=['POST'])
def visits_format():
    data = request.get_json()  # This parses the incoming JSON into a Python dictionary
    rows = data.get('rows')
    print("visit rows", rows)
    if not rows:
        return jsonify({"error": "rows empty"}), 400

    # Assuming 'rows' is a list of lists, where each list represents a row in the table
    try:
        table = render_visits_table(rows)
        print('Visits table', table)
        return table, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def render_visits_table(schedule):
# Start building the table HTML
    table_html = """
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Email</th>
          <th scope="col">Appointment Date and Time</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
    """
    for appointment in schedule:
        table_html += f"""
            <tr>
              <td>{appointment[3]}</td>
              <td>{appointment[7]}</td>
              <td>
                <form action="http://127.0.0.1:5009/delete-appointment" method="post" style="display: inline;">
                  <input type="hidden" name="email" value="{appointment[3]}">
                  <button type="submit">Delete</button>
                </form>
              </td>
            </tr>
            """

    # Close the table tags
    table_html += """
      </tbody>
    </table>
    """

    return table_html

# PATIENT BILLING TABLE FORMATING
@app.route('/billing_table', methods=['POST'])
def billing_format():
    data = request.get_json()  # This parses the incoming JSON into a Python dictionary
    rows = data.get('rows')
    print("visit rows", rows)
    if not rows:
        return jsonify({"error": "rows empty"}), 400

    # Assuming 'rows' is a list of lists, where each list represents a row in the table
    try:
        table = render_billing_table(rows)
        return table, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def render_billing_table(schedule):
# Start building the table HTML
    table_html = """
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Email</th>
          <th scope="col">Amount Due</th>
          <th scope="col">Actions (do nothing currently)</th>
        </tr>
      </thead>
      <tbody>
    """
    for appointment in schedule:
        table_html += f"""
            <tr>
              <td>{appointment[3]}</td>
              <td>${ "{:,.2f}".format(appointment[9]) }</td>  <!-- Formats integer into $ amount with 2 decimals -->
              <td>
                <form action="http://127.0.0.1:5008/billing" method="post" style="display: inline;">
                  <input type="hidden" name="email" value="#">
                  <button type="submit">Increase</button>
                </form>
                <form action="http://127.0.0.1:5008/billing" method="post" style="display: inline;">
                  <input type="hidden" name="email" value="#">
                  <button type="submit">Decrease</button>
                </form>
              </td>
            </tr>
            """

    # Close the table tags
    table_html += """
      </tbody>
    </table>
    """

    return table_html

if __name__ == '__main__':
    app.run(port=5006, debug=True)
