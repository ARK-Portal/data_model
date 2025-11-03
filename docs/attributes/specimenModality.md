---
title: specimenModality
parent: Attributes
datatable: true
layout: page
nav_order: 80
permalink: docs/attributes/specimenModality.html
date: 2025-11-03
---
{% assign mydata=site.data.csv.attributes.specimenModality %}
{% include content/specimenModality.md %}
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
      paging: false,
      order: [],
    });
  });
</script>
