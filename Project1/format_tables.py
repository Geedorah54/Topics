# PURPOSE: Create tables for front-end

def render_homepage_table(rows):
    # displays dynamic table of all data
    table_html = """
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Patient ID</th>
          <th scope="col">First Name</th>
          <th scope="col">Last Name</th>
          <th scope="col">Age</th>
          <th scope="col">Appointment Date & Time</th>
        </tr>
      </thead>
      <tbody>
    """

    for row in rows:
        table_html += "<tr>"
        for column in row:
            table_html += f"<td>{column}</td>"
        table_html += "</tr>"

    table_html += """
      </tbody>
    </table>
    """

    return table_html

def render_visits_table(schedule):
    # Displays dynamic table of booked appointments
    if not schedule:
        return "<p>No appointments booked.</p>"

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
          <td>{appointment[0]}</td>
          <td>{appointment[4]}</td>
          <td>
            <form action="/delete-appointment" method="post" style="display: inline;">
              <input type="hidden" name="email" value="{appointment[0]}">
              <button type="submit">Delete</button>
            </form>
          </td>
        </tr>
        """

    table_html += """
      </tbody>
    </table>
    """

    return table_html
