---
title: snATACSeq Processed Data Annotation Template
parent: Metadata Templates
datatable: true
layout: page
permalink: docs/metadata_templates/sn_atac_seq_processed_data_annotation_template.html
date: 2025-12-05
---
{% assign mydata=site.data.csv.metadata_templates.sn_atac_seq_processed_data_annotation_template %}
{% include content/sn_atac_seq_processed_data_annotation_template.md %}
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
      columnDefs: [
        {
          targets: 0,
          orderable: false,
          render : function(data, type, row, meta){
              return $('<a>')
                   .attr('href','../attributes/'+data)
                   .text(data)
                   .wrap('<div></div>')
                   .parent()
                   .html();
          }
        },
        {
          targets: [1,2,3],
          orderable: false
        }
      ]
    });
  });
</script>
