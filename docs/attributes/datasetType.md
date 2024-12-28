---
title: "datasetType"
parent: Attributes
datatable: true
layout: page
permalink: "docs/attributes/datasetType.html"
date: "2024-12-28"
params:
  title: ""
---
{% assign mydata=site.data.csv.attributes.datasetType %} 

{% include content/datasetType.md %}

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
