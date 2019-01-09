#!/usr/bin/env python

import xml.etree.ElementPath as EP
import xml.etree.ElementTree as ET
import asyncio


def xmlinsert(xpath, xmlfile, tag='', findall=False):
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
            asyncio.run(elementinsert(token_iter, element))
    else:
        asyncio.run(elementinsert(token_iter, root.find(tag)))
    tree.write(xmlfile)
    return xmlfile

    # [tag] add to direct descendents
    # [tag='text'] add subelements with an xpath as text
    # [position] add subelement at this position
    # add to all descendents
    # // insert in all nodes in the document handled by the pattern arg
    # don't see a reason to support "." or ".." current and parent contexts


async def elementinsert(token_iter, xmlelement):
    """takes element and adds subelements

    Args
        xpath (str): xml elements separated by back slash
        xmlelement (obj): element class from elementtree package

    Returns:
        Element Class

    Notes:
        Supports simple xpath syntax
    """
    try:
        token = next(token_iter)
    except StopIteration:
        return
    # if delimiter is a '/' skip token
    if token[0] == '/':
        await elementinsert(token_iter, xmlelement)
    elif token[0] == "" and len(token[1]) > 0:
        xmlelement = ET.SubElement(xmlelement, token[1])
    elif token[0] == "[":
        xmlelement = await add_predicate[token[0]](
                              token_iter, xmlelement)
    await elementinsert(token_iter, xmlelement)


async def add_predicate(token_iter, xmlelement, attribute_flag):
    """takes element and updates values

    Args
        xmlelement (obj: 'str'): element class from elementtree package
        token_iter (obj): iterator type object containing tuples of strings
        attribute_flag (str): determines whether input is attribute of
    Returns:
        (obj: 'str'): element class

    Notes:
        when we hit either ] or "and" we take stock
        we use signature to determine the course of action
          if signature has @ it's an attribute,
          if signature has () it's a value of the tag
          if signature has / or empty or [ it's an xpath
    """
    predicate = []
    modifiers = []
    try:
        token = next(token_iter)
    except StopIteration:
        return xmlelement
    if token[0] == "]":
        signature = "".join(modifiers)
        if signature == "@=":
            xmlelement.attrib["".join(attrib_key)] = "".join(attrib_value)
        elif signature in {"", "/"}:

        return xmlelement
    elif 
    elif token == ('', ''):
        # ignore whitespace possibly change to pass
        pass
    elif token[0] == '':
        predicate.append(token[1])
    elif token[1] == '':
        modifiers.append(token[0])
    else:
        raise SyntaxError("invalid character")
    return await add_predicate(xmlelement, token, token_iter)
