# AdFor CTF

## Windows Artefakte

### 1_SID_Validity

> Ist die SID S-1-5-21-4650571544-2262814165-2515253795-500 eine gültige SID?
> Hinweis: Antwortmöglichkeiten: "ja" / "nein"

**Flag**: `nein`

### 1_Artefacts_Thumbcache_1

> Unter welchem Pfad finden Sie seit Windows Vista die Thumbcache-Dateien (englisches Windows-Betriebssystem)?

**Flag**: `%UserProfile%\AppData\Local\Microsoft\Windows\Explorer`

### 1_Artefacts_Thumbcache_2

> Lassen sich auf Basis der Thumbcachedateien Informationen zur originalen Bilddatei (Dateiname, Pfad, etc.) eines Vorschaubildes auf dem System ermittteln?

**Flag**: `nein`

### 1_Artefacts_Thumbcache_5

> Nennen Sie die Länge in Bytes für einen Thumbcache Index Eintrag.

Die Größe eines Eintrags ist 32 Byte.

**Flag**: `32`

### 1_Artefacts_Thumbcache_3

> In wieviel verschiedenen Auflösungen stehen in folgendem Beispiel Vorschaubilder zur Verfügung?

```bash
$ ls -l /mnt/Users/eve/AppData/Local/Microsoft/Windows/Explorer
[REMOVED]
-rwxrwxrwx 2 root root 24 Feb 17 14:42 thumbcache_1024.db
-rwxrwxrwx 2 root root 2097152 Feb 17 14:42 thumbcache_256.db
-rwxrwxrwx 2 root root 1048576 Mär 10 10:44 thumbcache_32.db
-rwxrwxrwx 2 root root 2097152 Feb 17 14:42 thumbcache_96.db
-rwxrwxrwx 2 root root 6488 Mär 10 12:04 thumbcache_idx.db
-rwxrwxrwx 2 root root 24 Feb 17 14:42 thumbcache_sr.db
```

Es sind 3 Auflösungen verfügbar, da in `thumbache_1024.db` nur der Header (24 Byte) steht.

**Flag**: `3`


### 1_Artefacts_Prefetch_1

> Bestimmen Sie anhand folgendem Hexdump die Dateigröße der Prefetch-Datei in Byte.

```bash
$ xxd /mnt/Windows/Prefetch/TOR.EXE-7C6B6C7F.pf

00000000: 1700 0000 5343 4341 1100 0000 74b5 0100  ....SCCA....t...
00000010: 5400 4f00 5200 2e00 4500 5800 4500 0000  T.O.R...E.X.E...
00000020: b716 0000 0000 0000 d9e5 a582 c03c f2a0  .............<..
00000030: bbe6 a582 0100 0000 2894 2786 1100 0000  ........(.'.....
00000040: 2894 2786 1097 2786 0000 0000 7f6c 6b7c  (.'...'......lk|
[REMOVED]
```

0x0001b574 = 111988 Byte

**Flag**: `111988`

### 1_Artefacts_Recycle.bin_1

> Sie betrachten den Inhalt eines nutzerspezifischen Papierkorbs. Wieviele gelöschte Dateien finden Sie darin?

```cmd
$ ls -l /mnt/$Recycle.Bin/S-1-5-21-2676350820-1773932353-647818126-1001
total 31241
drwxr-xr-x 1 501 dialout      416 Nov 13  2017  .
drwxr-xr-x 1 501 dialout      128 Nov  9  2018  ..
-rwxr-xr-x 1 501 dialout      544 Nov  9  2017 '$I64Z8MM.exe'
-rwxr-xr-x 1 501 dialout      544 Nov  9  2017 '$IDUBO0X.exe'
-rwxr-xr-x 1 501 dialout      544 Nov 13  2017 '$IKXFDA9.lnk'
-rwxr-xr-x 1 501 dialout      544 Nov 13  2017 '$IR6G8S2.jpg'
-rwxr-xr-x 1 501 dialout      544 Nov 13  2017 '$ITJS14V.py'
-rwxr-xr-x 1 501 dialout 29625696 Nov  9  2017 '$R64Z8MM.exe'
-rwxr-xr-x 1 501 dialout  2348216 Nov  9  2017 '$RDUBO0X.exe'
-rwxr-xr-x 1 501 dialout     2929 Nov  9  2017 '$RKXFDA9.lnk'
-rwxr-xr-x 1 501 dialout     3197 Nov 13  2017 '$RR6G8S2.jpg'
-rwxr-xr-x 1 501 dialout     2070 Nov 10  2017 '$RTJS14V.py'
-rwxr-xr-x 1 501 dialout      129 Dec  7  2016  desktop.ini
```

Die Metadaten einer gelöschten Datei sind jeweils 544 Byte groß.

**Flag**: `5`

### 1_Artefacts_Recycle.bin_2

> Sie betrachten gerade den Hexdump einer Metadaten-Datei im Ordner $Recycle.bin. Geben Sie den absoluten Pfad samt Dateiname der Original-Datei an.

```bash
$ xxd $IR6G8S2.jpg | less
00000000: 0100 0000 0000 0000 7d0c 0000 0000 0000  ........}.......
00000010: 90c6 f4f9 6f5c d301 4300 3a00 5c00 5500  ....o\..C.:.\.U.
00000020: 7300 6500 7200 7300 5c00 7500 7300 6500  s.e.r.s.\.u.s.e.
00000030: 7200 5c00 4400 6500 7300 6b00 7400 6f00  r.\.D.e.s.k.t.o.
00000040: 7000 5c00 5300 6100 7400 6500 6c00 6c00  p.\.S.a.t.e.l.l.
00000050: 6900 7400 6500 5f00 6900 6d00 6100 6700  i.t.e._.i.m.a.g.
00000060: 6500 5f00 6f00 6600 5f00 4600 7200 6100  e._.o.f._.F.r.a.
00000070: 6e00 6300 6500 5f00 6900 6e00 5f00 4100  n.c.e._.i.n._.A.
00000080: 7500 6700 7500 7300 7400 5f00 3200 3000  u.g.u.s.t._.2.0.
00000090: 3000 3200 2e00 6a00 7000 6700 0000 0000  0.2...j.p.g.....
```

**Flag**: `C:\Users\user\Desktop\Satellite_image_of_France_in_August_2002.jpg`

### 1_Artefacts_Prefetch_6

>Wieviele Prefetch Dateien können pro Anwendung existieren?
> a) Immer genau eine Prefetch Datei.
> b) Mehrere Prefetch Dateien.
> Antwortmöglichkeiten:
> "a" / "b"

Es kann mehrere Prefetch Dateien geben.

**Flag**: `b`

## SQLite Forensik

### 2_SQLite_Basics_1

**Flag**: `512`

### 2_SQLite_Basics_2

**Flag**: `65536`

### 2_SQLite_Basics_3

**Flag**: `4294967294`

### 2_SQLite_Basics_4

**Flag**: `Freelist`

### 2_SQLite_Basics_5

**Flag**: `Overflow-Seite`

### 2_SQLite_Basics_6

**Flag**: `B-Baum`

### 2_SQLite_BTree_1

**Flag**: `8`

### 2_SQLite_Header_1

**Flag**: `8`

