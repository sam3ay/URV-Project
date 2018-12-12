#!/usr/bin/env python

import xml.etree.ElementPath as EP
import xml.etree.ElementTree as ET


def xmlinsert(xpath, xmlfile, tag='/', findall=False):
    """Inserts elements from an xpath

    refs: xml.etree.ElementPath
          https://github.com/python/cpython/blob/3.7/Lib/xml/etree/ElementPath.py

    Args:
        xpath (str): xml elements separated by back slash
            (no whitespace outside of attributes)
        xmlfile (str): path to xml file; created if it doesn't exist
        tag (str): xml element to serve as parent (/ or . = root)
        findall (bool): If true finds all matching itmes matching tag
            and inserts xml elements from xpaths after deepest member
    Returns:
        str: location of updated xml file

    Notes:
        xpath (str): expects paths which only descend.  And supports
            the following symbols in xpath /[=@
            ex. a[bar=/hello/world]/b[foo]/c[@nope=there]/d

        tag (str): used by implementation of Elementree's iterfind function
            so see xml.etree.elementree for limitations.

    dev:
        if no pattern is provided:
        split string into list by delimiter /  xpath.split('/')
        loop through list try to append subelement from previous subelement
        except catches failure and creates initial subelement in the
        in the specified root
        else:
        findall patterns of that satisfy pattern and add subelements to these
        use ET.Element.iterfind()
    """
    # import xml and convert to element
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    # no absolute paths
    if xpath[0] == '/':
        raise SyntaxError("Can't create another root directory in an xml file")
    token_iter = EP.xpath_tokenizer(xpath)
    # check recursive
    if findall:
        for element in root.iterfind(tag):
            elementinsert(token_iter, element)
    else:
        elementinsert(token_iter, root.find(tag))
    tree.write(xmlfile)
    return xmlfile

    # / if first character then absolute path
    # [tag] add to direct descendents
    # [tag='text'] add subelements with an xpath as text
    # [position] add subelement at this position
    # add to all descendents
    # // insert in all nodes in the document handled by the pattern arg
    # don't see a reason to support "." or ".." current and parent contexts


def elementinsert(token_iter, xmlelement):
    """takes element and adds subelements

    Args
        xpath (str): xml elements separated by back slash
        xmlelement (obj): element class from elementtree package

    Returns:
        Element Class

    Notes:
        Supports simple xpath syntax
    """
    operations = {
            "": add_subelement,  # child elements
            "[": add_predicate
            }
    try:
        token = next(token_iter)
    except StopIteration:
        return
    try:
        new_element = ops[token[0]](xmlelement, token)
    except KeyError:
        raise  # invalid character
    elementinsert(token_iter, new_element)
