#!/usr/bin/python

__requires__ = 'qrcode>=5.3'
import re
import sys, os
import qrcode
import argparse

from jinja2 import Template, Environment, FileSystemLoader

build_dir='_build'
template_tex = ('doc_', '.tex')

def create_qrcode_img(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.make_image()

def create_wifi_qrcode(ssid, pw, encryption='WPA'):
    txt = 'WIFI:S:{};T:{};P:{};;'.format(ssid, encryption, pw)
    return create_qrcode_img(txt)


def create_document(ssid, pw, encryption='WPA', language='de'):
    try:
        os.stat(build_dir)
    except:
        os.mkdir(build_dir) 

    template = Environment(loader = FileSystemLoader('./template')).get_template(template_tex[0] + language + template_tex[1])
    result = template.render(SSID=ssid, PASSWORD=pw)
    with open(build_dir + '/document.tex', 'w') as tex_file:
        tex_file.write(template.render(
                                        SSID=ssid, PASSWORD=pw, ENCRYPTION=encryption
                                      ))
    
    img = create_wifi_qrcode(ssid, pw, encryption)
    img.save(build_dir + '/wifi.png')

    print('Result is in directory "{}/".'.format(build_dir))
    print('Use "pdflatex document.tex" to build the pdf')

def parse_arguments():
    parser = argparse.ArgumentParser(description='CLI for creating a simple tex-document for a wifi connection '
                                                 'containing a qr-code to be scanned.')
    parser.add_argument('SSID', help='The SSID of the wifi.')
    parser.add_argument('PASSWORD', help='The password of the wifi.')
    parser.add_argument('-e', '--encryption', choices=['WPA', 'WEP'],
                        help='The encryption used by the wifi.', default='WPA')
    parser.add_argument('-d', '--destination', default=build_dir, required=False,
                        help='Destination of the document.')
    parser.add_argument('-l', '--language', choices=['de', 'en'],
                        help='Language of the resulting document.', default='de')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    create_document(args.SSID, args.PASSWORD, args.encryption)

