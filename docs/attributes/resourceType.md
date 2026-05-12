---
title: resourceType
parent: Attributes
datatable: true
layout: page
nav_order: 78
permalink: docs/attributes/resourceType.html
date: 2026-05-12
---
{% assign mydata=site.data.csv.attributes.resourceType %}
{% include content/resourceType.md %}
<table id="myTable" class="display" style="width:100%">
    <thead>
    {% for column in mydata[0] %}
        <th>{{ column[0] }}</th>
    {% endfor %}
    </thead>
    <tbody>
    {% for row in mydata %}
        <tr>
        {% for cell in row %}
            <td>{{ cell[1] }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
<script type="text/javascript">
  $(document).ready(function () {
    $('#myTable').DataTable({
      responsive: true,
      deferRender: false,
      paging: true,
      pageLength: 50,
      lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
      order: [],
    });
  });
</script>
