# -*- coding: utf-8 -*-
#
#  i18n module
#  Created by LulzLoL231 at 23/11/22
#
import os
import json
import logging
from typing import Dict


log = logging.getLogger('i18n')


class Language:
    def __init__(self, language: str, lang_dict: Dict[str, str]) -> None:
        '''Класс языка.

        Args:
            language (str): Название языка.
            lang_dict (Dict[str, str]): Словарь языка.
        '''
        self._language = language
        self._lang_dict = lang_dict

    def t(self, word: str) -> str:
        '''Возвращает текст по ключу.

            Args:
                word (str): Ключ к тексту.
        '''
        if word in self._lang_dict.keys():
            return self._lang_dict[word]
        else:
            log.error(
                f'For language "{self._language}" not found word "{word}"!'
            )
            return f'%{word}'

    def __getattr__(self, key: str) -> str:
        '''Функция для получения текстов по ключам в виде атрибутов к классу.
        '''
        return self.t(key)

    def __repr__(self) -> str:
        return f'<Язык "{self.language}" ({self._language}.json)>'


class Languages:
    def __init__(self, path: str = 'i18n') -> None:
        '''Класс сбора языков.

        Args:
            path (str, optional): Путь к папке с языками. Defaults to 'i18n'.
        '''
        self.language = 'ru'
        self.dicts: Dict[str, Dict[str, str]] = {}
        for file in os.listdir(path):
            if file.endswith('.json'):
                path = os.path.join(path, file)
                with open(path, 'r', encoding='utf-8') as f:
                    self.dicts.update(
                        {file.replace('.json', ''): json.loads(f.read())})

    def get_available(self) -> list:
        '''Ворзвращает список доступных языков.

        Returns:
            list: Language list.
        '''
        return list(self.dicts.keys())

    def get_language(self, language: str = '') -> Language:
        '''Возвращает класс нужного языка.

        Args:
            language (str): language name. Defaults: "".

        Returns:
            Language: language class.
        '''
        if language:
            if language in list(self.dicts.keys()):
                return Language(language, self.dicts[language])
            else:
                log.error(
                    f'Not found language "{language}". '
                    'Using default language: "ru"'
                )
        return Language('ru', self.dicts['ru'])
