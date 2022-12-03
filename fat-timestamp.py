#!/usr/bin/env python3

from decimal import Decimal

class FatTimestamp:
  def __init__(self, hh_mm_ss: int, milliseconds: int):
    """Representation of a timestamp (HH:MM:SS.MSE) in a FAT file system

    Keyword arguments:
    hh_mm_ss -- timestamp value as 2 byte integer
    milliseconds -- milliseconds value as 1 byte integer
    """
    self.__hh_mm_ss: int = hh_mm_ss
    self.__hours: int = self.__extract_from_timestamp(0, 5)
    self.__minutes: int = self.__extract_from_timestamp(5, 11)
    self.__seconds: int = self.__extract_from_timestamp(11, 16) * 2
    whole_seconds, self.__milliseconds = self.__calculate_milliseconds(milliseconds)
    self.__seconds = self.__seconds + whole_seconds

  def __extract_from_timestamp(self, start: int, end: int) -> int:
    """Extract number from the binary representation of the timestamp

    Keyword arguments:
    start -- start position
    end -- end position (exclusive)
    """
    hh_mm_ss_binary: str = format(self.__hh_mm_ss, 'b').rjust(16, '0')
    return int(hh_mm_ss_binary[start:end], 2)

  def __calculate_milliseconds(self, number: int) -> tuple[int, int]:
    """Calculate whole seconds and milliseconds from milliseconds

    Keyword arguments:
    number -- milliseconds as 1 byte value
    """
    seconds_with_milliseconds: Decimal = Decimal(number * 10 / 1000)
    whole_seconds: int = int(seconds_with_milliseconds)
    milliseconds = int((seconds_with_milliseconds % 1) * 1000)
    return whole_seconds, milliseconds

  def __str__(self):
    """Forms string representation of timestamp as HH:MM:SS.MSE"""
    return f'{self.__hours:02}:{self.__minutes:02}:{self.__seconds:02}:{self.__milliseconds:03}'

# from hexdump: a0f653
# print(FatTimestamp(0x53f6, 0xa0))
# 10:31:45:600
