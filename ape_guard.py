import requests
from bs4 import BeautifulSoup
import re
from solidity_parser import parser
import numpy as np
keyword_list ={"AggregatorV3Interface" : "use chainlink oracle Ape like it",
               "UniswapV2OracleLibrary" : "Uniswap oracle - be careful",
               "migrate": "Why Migration - Ape not a bird we don't like migration!"}


def get_bsc_codes(address):
    res = requests.get(f"https://bscscan.com/address/{address}#code")
    soup = BeautifulSoup(res.content)
    return soup.find_all(id='editor')


def clean_sol_comment(sol_code):
    clean = []
    status = "X"
    for l in sol_code.split('\n'):
        if status == "code":
            if l.find('/*') > -1:
                status = "comment"
                com = l.find('/*')
            else:
                com = l.find('//')
                if com > -1:
                    clean.append(l[0:com])
                else:
                    clean.append(l[0:])
        if status == "comment":
            if l.find('*/') > -1:
                ucon = l.find('*/')
                clean.append(l[(ucon + 2):])
                status = "code"
        if (status == "X") and ("pragma" in l):
            clean.append(l)
            status = "code"
    clean = [x.strip() for x in clean if len(x.strip()) > 0]
    return clean


def big_magic_file(codes):
    the_code = []
    for c in codes:
        the_code += clean_sol_comment(c.text)
    return the_code


def clean_call(sol_code):
    # clean call function syntax for parser <- shitty parser - not up to date LOL
    clear = [l for l in sol_code.split("\n") if l.find("call{") < 0]
    return "\n".join(clear)


def parse_sol(sol_code):
    sourceUnit = parser.parse(sol_code)
    sourceUnitObject = parser.objectify(sourceUnit)
    return sourceUnitObject


def do_magic(address):
    magic = {}
    magic['score'] = 8
    codes = get_bsc_codes(address)
    magic['no_files'] = len(codes)
    big_magic = big_magic_file(codes)
    magic['no_line'] = len(big_magic)
    object = parse_sol(clean_call("\n".join(big_magic)))
    return method_name(magic, object)

def do_magic_2(text):
    magic = {}
    magic['score'] = 8
    object = parse_sol(clean_call(text))
    return method_name(magic, object)

def method_name(magic, object):
    magic['no_contract'] = len(object.contracts.keys())
    magic['no_function'] = 0
    magic['risks'] = []
    magic['comment'] = []
    for ck in object.contracts.keys():
        magic['no_function'] += len(object.contracts[ck].functions.keys())
        for fk in object.contracts[ck].functions.keys():
            if fk is None:
                continue
            if fk.find("migrate") > -1:
                if keyword_list["migrate"] not in magic['risks']:
                    magic['score'] -= 5
                    magic['risks'].append(keyword_list["migrate"])
    for imp in object.imports:
        if imp['path'].find("UniswapV2OracleLibrary"):
            if keyword_list["UniswapV2OracleLibrary"] not in magic['risks']:
                magic['score'] -= 1
                magic['risks'].append(keyword_list["UniswapV2OracleLibrary"])
        if imp['path'].find("AggregatorV3Interface"):
            magic['comment'].append(keyword_list["AggregatorV3Interface"])
    magic['risks'] = np.unique(magic['risks'])
    magic['comment'] = np.unique(magic['comment'])
    return magic




