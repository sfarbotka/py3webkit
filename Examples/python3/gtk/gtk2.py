#!/usr/bin/env python3

import gi
gi.require_version("WebKit", "1.0")

from gi.repository import WebKit, Gtk, GObject

WebKit.init_python()
import pywebkit


def on_destroy(wnd):
    Gtk.main_quit()

def on_click(event):
    print('button click ', event)

def on_load_finished(webview, webframe):
    print('Load finished ({})'.format(webview.get_uri()))
    
    doc = pywebkit.GetDomDocument(webview)
    links = doc.getElementsByTagName('a')
    print('Links count: {}'.format(len(links)))
    for i, a in enumerate(links):
        print('\t{}) {}'.format(i+1, a.getAttribute('href')))

    button = doc.createElement('button')
    button.innerText = 'Click Me'
    button.onclick = on_click
    body = doc.getElementsByTagName('body')[0]
    body.appendChild(button)

def main():
    webview = WebKit.WebView()
    webview.connect("load-finished", on_load_finished)
    webview.load_uri("http://google.com")

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.props.hscrollbar_policy = Gtk.PolicyType.AUTOMATIC
    scrolled_window.props.vscrollbar_policy = Gtk.PolicyType.AUTOMATIC
    scrolled_window.add(webview)
    
    vbox = Gtk.VBox(spacing=1)
    vbox.pack_start(scrolled_window, True, True, True)
    
    window = Gtk.Window()
    window.add(vbox)
    window.set_default_size(800, 600)
    window.connect('destroy', on_destroy)
    window.show_all()

    Gtk.main()
    

if __name__ == '__main__':
    main()


