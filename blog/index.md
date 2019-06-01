---
layout: default
title: Blog
---
<div id="blog_header">
  <h2>Posts</h2>
  <span id="feed_link"><a class="nav_link" href="/feed.xml">feed</a></span>
</div>
<table>
  {% for post in site.posts %}
    <tr>
      <td class="post_date">
        {{ post.date | date: "%Y-%m-%d" }}
      </td>
      <td class="post_title">
        <a href="{{ post.url }}">{{ post.title }}</a>
        {% if post.tags %}
          <br>
        {% endif %}
        {% for tag in post.tags %}
          [{{ tag }}]
        {% endfor %}
      </td>
    </tr>
  {% endfor %}
</table>
