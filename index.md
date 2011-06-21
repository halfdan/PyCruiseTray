---
layout: base
title: Home
---

PyCruiseTray is a simple GNOME 2 widget that shows the status of your builds on a CruiseControl Server.

Its user interface is easy to use and shows all the important details about the status of your project builds.

## News

{% for post in site.posts limit:1 %}

### {{ post.date | date_to_long_string }}

[{{ post.title }}](/beanstalkd{{ post.url }})

{% endfor %}

[More news...](news.html)

## Run It


## Use It


## Bugs

Please report any bugs to the [issue tracker][github issues] at GitHub.

## Thanks



[github issues]: http://github.com/halfdan/PyCruiseTray/issues
