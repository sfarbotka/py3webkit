Python3 WebKit DOM Binding
==========================

The Python 3 Webkit DOM Project makes python3 a full peer of javascript when
it comes to accessing and manipulating the full features available to
Webkit, such as HTML5.  Everything that can be done with javascript,
such as getElementsbyTagName and appendChild, event callbacks through
onclick, timeout callbacks through window.setTimeout, and even AJAX
using XMLHttpRequest, can also be done from python3.

Based on [Python Webkit DOM Bindings](http://www.gnu.org/software/pythonwebkit) project.

The work is in progress.
Currently only GTK+ port of WebKit is supported.

Examples
--------

Next example finds all "a" tags in a document and prints hrefs for each tag:

    def on_load_finished(webview, webframe):
        doc = pywebkit.GetDomDocument(webview)
        links = doc.getElementsByTagName('a')
        print('Links count: {}'.format(len(links)))
        for i, a in enumerate(links):
            print('\t{}) {}'.format(i+1, a.getAttribute('href')))

Next example inserts "Click Me" button and sets button *onclick* event: 

    def on_click(event):
        print('button click ', event)

    def on_load_finished(webview, webframe):
        doc = pywebkit.GetDomDocument(webview)

        button = doc.createElement('button')
        button.innerText = 'Click Me'
        button.onclick = on_click

        body = doc.getElementsByTagName('body')[0]
        body.appendChild(button)

You can see working examples in *Examples/python3* folder

Build
-----

To build WebKit with enabled python3 binding run next script:

    Tools/Scripts/build-webkit-python

This script places build products in WebKitBuild directory.

For more information please see [http://www.webkit.org/building/build.html](http://www.webkit.org/building/build.html)

