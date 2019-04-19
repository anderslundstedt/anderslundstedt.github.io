---
layout: default
title: "Necessarily non-analytic induction—summary"
---
## {{ page.title }}
{% assign files = site.static_files | where: "non_analytic_induction_summary", true %}
{% for file in files %}
– [{{ file.name }}]({{ file.path }})
{% endfor %}
