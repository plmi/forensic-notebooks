#!/usr/bin/env python3

class FatDate:
  def __init__(self, date: int):
    """Representation of a date in a FAT file system

    Keyword arguments:
    date -- 16 bit value for a date
    """
    self.__date: int = date
    self.__year: int = self.__extract_from_date(0, 7) + 1980
    self.__month: int = self.__extract_from_date(7, 11)
    self.__day: int = self.__extract_from_date(11, 16)

  def __extract_from_date(self, start: int, end: int) -> int:
    """Extract number from the binary representation of the date value

    Keyword arguments:
    start -- start position
    end -- end position (exclusive)
    """
    binary_date: str = format(self.__date, 'b').rjust(16, '0')
    return int(binary_date[start:end], 2)

  def __str__(self):
    """Forms string representation of date as TT.MM.JJJJ"""
    return f'{self.__day:02}.{self.__month:02}.{self.__year}'

# from hexdump: 8132
# print(FatDate(0x3281))
# 01.04.2005
