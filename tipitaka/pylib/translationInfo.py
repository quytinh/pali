#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import collections
# from pathInfo import xmlFilename2Info (cannot use because of circular import)
import pathInfo

# See setTranslationData.py
with open(os.path.join(os.path.dirname(__file__), 'json/translationInfo.json'), 'r') as f:
  d = json.JSONDecoder(object_pairs_hook = collections.OrderedDict)
  translationInfo = d.decode(f.read())


def isValidTranslation(xmlFilename, translationLocale, translator):
  if translationLocale in translationInfo:
    if xmlFilename in translationInfo[translationLocale]['canon']:
      for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
        if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
          return True

  return False


def getTranslatorSource(xmlFilename, translationLocale, translator):
  if xmlFilename in translationInfo[translationLocale]['canon']:
    for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
      if translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0] == translator.decode('utf-8'):
        return localeXmlTranslation['source']

  raise Exception('cannot find translator source %s %s %s' % (xmlFilename, translationLocale, translator))


def getTranslator(translationLocale, localeXmlTranslation):
  return translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0]


def getLocaleXmlTranslations(translationLocale, xmlFilename):
  localeXmlTranslations = []
  for localeXmlTranslation in translationInfo[translationLocale]['canon'][xmlFilename]:
    tmp = { 'source': localeXmlTranslation['source'],
            'translator': getTranslator(translationLocale, localeXmlTranslation) }

    # retrieve additional information if available
    if 'excerpt' in localeXmlTranslation:
      tmp['excerpt'] = localeXmlTranslation['excerpt']
    if 'URL' in localeXmlTranslation:
      tmp['URL'] = localeXmlTranslation['URL']
    if 'copyrightURL' in localeXmlTranslation:
      tmp['copyrightURL'] = localeXmlTranslation['copyrightURL']

    localeXmlTranslations.append(tmp)

  return localeXmlTranslations


def getI18nLinksTemplateValues(xmlFilename):
  i18nLinksTmpValue = { 'localeTranslations': [] }
  for translationLocale in translationInfo:
    localeTranslation = { 'translationLocale': translationLocale }
    if xmlFilename in translationInfo[translationLocale]['canon']:
      localeTranslation['localeXmlTranslations'] = \
        getLocaleXmlTranslations(translationLocale, xmlFilename)

    if 'localeXmlTranslations' in localeTranslation:
      i18nLinksTmpValue['localeTranslations'].append(localeTranslation)

  if len(i18nLinksTmpValue['localeTranslations']) > 0:
    i18nLinksTmpValue['xmlFilename'] = xmlFilename
    return i18nLinksTmpValue


def getAllLocalesTranslationsTemplateValues():
  localeTranslations = []
  for translationLocale in translationInfo:
    localeTranslation = { 'translationLocale': translationLocale }
    localeTranslation['translations'] = []
    for xmlFilename in translationInfo[translationLocale]['canon']:
      info = pathInfo.xmlFilename2Info(xmlFilename)
      translation = { 'xmlFilename': xmlFilename,
                      'path': info['path'],
                      'translatedCanonNames': info['translatedCanonNames'],
                      'canonNames': info['canonNames'] }
      translation['localeXmlTranslations'] = \
        getLocaleXmlTranslations(translationLocale, xmlFilename)
      localeTranslation['translations'].append(translation)

    if len(localeTranslation['translations']) > 0:
      localeTranslations.append(localeTranslation)

  return localeTranslations


def getXmlLocaleTranslationInfo(action, translationLocale, translator):
  trInfo = { 'isExcerpt': None,
           'translationURL': None,
           'translationCopyrightURL': None }

  xmlFilename = os.path.basename(action)
  localeXmlTranslations = translationInfo[translationLocale]['canon'][xmlFilename]
  for localeXmlTranslation in localeXmlTranslations:
    if translator.decode('utf-8') == translationInfo[translationLocale]['source'][ localeXmlTranslation['source'] ][0]:
      if 'excerpt' in localeXmlTranslation:
        trInfo['isExcerpt'] = True
      if 'copyrightURL' in localeXmlTranslation:
        trInfo['translationCopyrightURL'] = localeXmlTranslation['copyrightURL']
      if 'URL' in localeXmlTranslation:
        trInfo['translationURL'] = localeXmlTranslation['URL']

      return trInfo
