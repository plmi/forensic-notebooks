# Digital Forensics CTF

## IT-forensische Software

### 3_Crazy_Pigeon (5)

> Laden Sie sich das Bild meeting.jpeg herunter und erstellen Sie eine Arbeitskopie des Bildes. Das **Flag** ist der SHA-256-Hashwert des Bildes.

SHA-256 Prüfsumme berechnen
```bash
$ sha256sum meeting.jpeg
148025cc28ade72f0155c009297342a6c6547f195a340aa062b8b815f878908a  meeting.jpeg
```

**Flag**: `148025cc28ade72f0155c009297342a6c6547f195a340aa062b8b815f878908a`

### 3_JPEG_Head (5)

> Nennen Sie die Signatur (Format 0xFFFF) mit welcher jede JFIF-Datei gemäß dem JPEG-Standard beginnt.

Dateiheader auslesen
```bash
$ xxd -l 16 meeting.jpeg
00000000: ffd8 ffe0 0010 4a46 4946 0001 0100 0048  ......JFIF.....H
```

**Flag**: `0xFFD8`

### 3_JPEG_Head (5)

> Wie ist die Bezeichnung für das erste Marker-Segment einer JFIF-Datei (Angabe als Akronym).

| FF xx | Symbol | Bezeichnung |
| ------| ------ | ----------- |
| FF D8	| SOI	| Start Of Image |

**Flag**: `SOI`

### 3_Hashvalue_1

> Wir betrachten einen USB-Stick, der unter /dev/sdb in das Dateisystem eingehängt ist. Nennen Sie den Befehl um für alle 'Dateien' /dev/sdb* (d.h. den USB-Stick selber sowie alle darauf enthaltenen Partitionen) den jeweiligen Hashwert in die Datei hashvalues.txt zu schreiben.

**Flag**: `sha256sum /dev/sdb* > hashvalues.txt`

### 3_Hashvalue_2

> Sie vermuten Ihr Kollege hat Änderungen an der Partition sdb1 vorgenommen. Wie können Sie mittels des Kommandos sha256sum die zuvor in hashvalues.txt gespeicherten Werte erneut überprüfen?

**Flag**: `sha256sum -c hashvalues.txt`

### 3_dd_Skills_1 (5)

> Schreiben Sie die erste Partition von /dev/sdb in die Datei image.dd. Nennen Sie den dafür verwendeten Befehl.

**Flag**: `dd if=/dev/sdb1 of=image.dd`

### 3_File_Carving_1 (5)

> Nennen Sie den absoluten Pfad der Scalpel Konfigurationsdatei.

**Flag**: `/etc/scalpel/scalpel.conf`

### 3_STRINGs_Theory (6)

> Untersuchen Sie die Bilddatei meeting.jpeg auf merkwürdige Spuren. Schränken Sie die Suche auf Zeichenketten ein, welche aus (mindestens) 10 Byte bestehen. Wieviele Zeichenketten können Sie aus der Bilddatei extrahieren? (Eingabe Anzahl im Format [0-9])

Anzahl der Zeichenketten der Länge >= 10 ausgeben
```bash
$ strings -n 10 meeting.jpeg | wc -l
49
```

**Flag**: 49

### 3_dd_Skills_2 (9)

> Sie suchen nach einer alternativen Möglichkeit die erste Partition herauszuschreiben und schauen sich dafür die Partitionstabelle der Gerätedatei /dev/sdb genauer an (s. partition_table.png).

> Geben Sie den dd-Befehl an um die Partition 002 in image.dd zu sichern. Die Blockgröße ist Default=512 und muss somit nicht explizit angegeben werden.

![partition_table.png](./3_dd_Skills_2/partition_table.png)

**Flag**: `dd if=/dev/sdb of=image.dd skip=2048 count=50331648`

### 3_File_Carving_2 (10)

> Stellen Sie den File Carver Scalpel so ein, dass lediglich jpg-Dateien gecarved werden.

> Können Sie versteckte Bilddateien finden? Falls ja, was ist darauf abgebildet?

Filecarving auf Abbild
```bash
$ scalpel -o filecarving image.dd
```

**Flag**: `dog`

### 3_File_Carving_3 (9)

> Sie wissen bereits, dass jpg-Dateien mit einer bestimmten Byte-Signatur beginnen, d.h. Sie können auch ohne File-Carving den Offset der Bilddatei bestimmen. Nennen Sie den bytegenauen Offset (in Dezimal).

Nach JPEG Byte-Signatur suchen
```bash
$ xxd image.dd | grep ffd8\ ff
00100000: ffd8 ffe0 0010 4a46 4946 0001 0101 012c  ......JFIF.....,

$ echo $((16#100000))
1048576
```

**Flag**: `1048576`

### 3_File_Carving_4 (10)

> Angenommen Sie hätten selbst gerne die Bilddatei dog.jpg in image.dd ab Offset 1 MiB versteckt. Beide Dateien liegen im aktuellen Verzeichnis.

> Welchen dd-Befehl hätten Sie hierfür verwendet? Die Blocksize wird hier fix mit 512 vorgegeben und muss daher nicht explizit angegeben werden!

Binärdaten des Bildes in Abbild an Position 0x100000 schreiben
```bash
$ echo $((16#100000))
1048575
$ echo "ibase=10; 1048576 / 512" | bc
2048
$ dd if=dog.jpg of=image.dd seek=2048 conv=notrunc
```

**Flag**: `dd if=dog.jpg of=image.dd seek=2048 conv=notrunc`

### 3_STRINGs_Theory_2

> Bestimmen Sie das erste Auftreten des Strings "Copyright" innerhalb der Bilddatei. (Tipp: Nutzen Sie dazu wieder das Kommando strings)
> Lösung: Vervollständigen Sie den unten stehenden Befehl um die Zeichenkette zu extrahieren (ersetzen Sie ## mit dem passenden Hexadezimalwert).
> dd bs=2 count=5 skip=$((####)) if=meeting.jpeg of=temp


Offset einer Zeichenkette bestimmen
```bash
$ strings -n 10 -t x meeting.jpeg | grep -i copy
    192 Copyright Apple Inc., 2017
```
Offset in Hex für Blockgröße 2 berechnen
```python
> hex(int(0x192 / 2))
0xc9
```

Zeichenkette extrahieren
```bash
$ dd bs=2 count=5 skip=$((0xc9)) if=meeting.jpeg of=temp
```

**Flag**: `dd bs=2 count=5 skip=$((0xc9)) if=meeting.jpeg of=temp`

### 3_BASICS_cipher (12)

> "Entschlüsseln" Sie die folgende Zeichenfolge:
> "#123#1010011#4f#1010011#1000101#100000#062#060#49#071#33#100000#87#101#108#1100011#0157#6d#0145#33#7d"

**Flag**: `{S0SE 2019! Welcome!}`


### 3_JPEG_Hydra (15)

> Anhand der vorherigen Auswertungen der Bilddatei meeting.jpeg sollten Ihnen ein paar Unstimmigkeiten aufgefallen sein.
> Extrahieren Sie den vielfrässigen Protagonisten (zur korrekten Anzeige), welcher nicht zu dem geheimen Taubentreffen eingeladen war. 
> Bestimmen Sie seine SHA256-Hashsumme.

Filecarving auf Bilddatei anwenden
```bash
$ binwalk --dd='.*' meeting.jpeg
$ sha256sum 1246D
08cd0be5260b8b5e660c3c5225cffbdb88f749b1e3674025a91d52b23daf506b  1246D
```

## FAT-Dateisystem

### 6_FAT_Bootsector_1 (5)

> Sie erhalten den Hexdump des Bootsektors einer FAT-formatierten Dateiystempartition.
> Bestimmen Sie die Größe eines Clusters in Bytes. Die Eingabe erfolgt als natürliche Zahl ohne Trennzeichen für Tausender (also z.B. 10000).

```
00000000: eb3c 904d 5344 4f53 352e 3000 0210 0800  .<.MSDOS5.0.....
00000010: 0200 0200 00f8 9400 3f00 ff00 0018 0000  ........?.......
00000020: 0040 0900 8000 29e8 b8da 3c4e 4f20 4e41  .@....)....NO NA
00000030: 4d45 2020 2020 4641 5431 3620 2020 33c9  ME    FAT16   3.
00000040: 8ed1 bcf0 7b8e d9b8 0020 8ec0 fcbd 007c  ....{.... .....|
*
000001f0: 0000 0000 0000 0000 0000 00ac c4d3 55aa  ..............U.
```

Größe eines Clusters in Bytes berechnen
```
- Werte aus Bootsektor auslesen:
- Clustergröße in Sektoren @ Offset 0x0d (13): 0x10 (16)
- Sektorgröße in Bytes @ Offset 0x0b-0x0c (11-12): 00 02 = 0x0200 (512)
- Clustergröße in Bytes = 16 * 512 = 8192 Bytes
```

### 6_FAT_Bootsector_2 (5)

> Sie erhalten den Hexdump des Bootsektors einer FAT-formatierten Dateisystempartition.
> Bestimmen Sie die Größe der Reserved Area in Sektoren.

Größe des reservierter Datenbereich in Sektoren berechnen
```
- Werte aus Bootsektor auslesen:
- Größe des reservierten Datenbereiches in Sektoren (14-15): 08 00 = 0x08 (8)
- Sektorgröße: 512 Bytes
- Größe reservierter Datenbereich in Bytes = 8 * 512 = 4096 Bytes
```

**Flag**: `8`

### 6_FAT_Bootsector_3 (5)

> Sie erhalten den Hexdump des Bootsektors einer FAT-formatierten Dateisystempartition.
> Bestimmen Sie die Größe einer FAT in Sektoren. Die Eingabe erfolgt als natürliche Zahl (z.B. 1234).

Größe einer FAT in Sektoren berechnen
```
- Werte aus Bootsektor auslesen:
- Anzahl Sektoren pro FAT in Sektoren @ Offset 22-23: 0x0094 (148)
- Sektorgröße: 512 Bytes
= Größe FAT = 148 * 512 Bytes = 75776 Bytes
```

**Flag**: `148`

### 6_FAT_Bootsector_4 (7)

> Sie erhalten den Hexdump des Bootsektors eines FAT-formatierten Datenträgers.
> Bestimmen Sie die Größe des Wurzelverzeichnisses in Bytes. Die Eingabe erfolgt als natürliche Zahl ohne Trennzeichen für die Tausender (z.B. 123456).

Größe des Wurzelverzeichnisses in Bytes berechnen
```
- Werte aus Bootsektor auslesen:
- Max. Anzahl Einträge im Wurzelverzeichnis @ Offset 17-18: 00 02 = 0x0200 (512)
- Größe eines Eintrags: 32 Byte
- Größe Wurzelverzeichnis = 512 Einträge * 32 Bytes = 16384 Bytes
```

**Flag**: `16384`

### 6_FAT_Bootsector_5 (7)

> Sie erhalten den Hexdump des Bootsektors eines FAT-formatierten Datenträgers.
> Bestimmen Sie die Größe des gesamten Dateisystems in Sektoren. Die Eingabe erfolgt als natürliche Zahl ohne Trennzeichen für Tausender oder Millionen (z.B. 12345678).

Größe des gesamten Dateisystems in Sektoren berechnen
```
- Werte aus Bootsektor auslesen:
- Größe des Dateisystems in Sektoren 16-Bit Wert @ (19-20): 00 00
- Größe des Dateisystems in Sektoren 32-Bit Wert @ (32-35): 00 40 09 00 = 0x00094000 (606208)
```

**Flag**: `606208`

### 6_FAT_Layout_1 (10)

> Nach Ihren Untersuchung des Bootsektors sind Sie in der Lage das Layout des FAT-Dateisystems zu skizzieren. Bestimmen Sie die LBA vom Start des Wurzelverzeichnisses (Variable v).

```
LBA
0     8      v          w       x      y ...              z
|     |      |          |       |      |
-----------------------------------------------------------
|Res. | FAT  | Root     | Cluster                         |
|Area | Area | Dir      | Area                            |
-----------------------------------------------------------
                        |       |      |
Cluster address         2       3      4 ....
```

Start-LBA des Wurzelverzeichnisses berechnen
```
- v = Größe Datenbereich in Sektoren + 2 * Größe FAT in Sektoren
- Datenbereich in Sektoren = 8
- FAT in Sektoren = 148
- v = 8 + 2 * 148 = 304 LBA
```

**Flag**: `304`

### 6_FAT_Layout_2 (10)

> Nach Ihrer Untersuchung des Bootsektors sind Sie in der Lage das Layout des FAT-Dateisystems zu skizzieren. Bestimmen Sie die LBA vom Start der Cluster Area (Variable w).

```
LBA
0     8      304        w       x      y ...              z
|     |      |          |       |      |
-----------------------------------------------------------
|Res. | FAT  | Root     | Cluster                         |
|Area | Area | Dir      | Area                            |
-----------------------------------------------------------
                        |       |      |
Cluster address         2       3      4 ....
```


Start-LBA des Clusterbereiches berechnen
```
- w = Start-LBA Wurzelverzeichnis + Größe Wurzelverzeichnis in Sektoren
- Größe Wurzelverzeichnis in Sektoren = (Anzahl Einträge * Größe pro Eintrag (32 Bytes)) / Sektorgröße
- Größe Wurzelverzeichnis in Sektoren = (512 * 32 Bytes) / 512 Bytes Sektorgröße = 32 Sektoren
- w = 304 + 32 = 336 LBA
```

**Flag**: `336`

### 6_FAT_Layout_3 (10)

> Nach Ihren Untersuchung des Bootsektors sind Sie in der Lage das Layout des FAT-Dateisystems zu skizzieren. Bestimmen Sie die LBA für Cluster 4 (Variable y).

```
LBA
0     8      304        336     x      y ...              z
|     |      |          |       |      |
-----------------------------------------------------------
|Res. | FAT  | Root     | Cluster                         |
|Area | Area | Dir      | Area                            |
-----------------------------------------------------------
                        |       |      |
Cluster address         2       3      4 ....
```


Start-LBA des Cluster 4 berechnen. Die Clusteradressen beginnen ab 2!
```
- y = Start-LBA Clusterbereich + 2 * (Größe Cluster in Sektoren)
- Clustergröße in Sektoren: 16
- y = 336 + (2 * 16) = 368
```

**Flag**: `368`

### 6_FAT_Layout_4 (10)

> Nach Ihren Untersuchung des Bootsektors sind Sie in der Lage das Layout des FAT-Dateisystems zu skizzieren. Bestimmen Sie die Adresse des letzten Sektors des Dateisystems (Variable z in Schaubild unten). Die Eingabe erfolgt als natürliche Zahl ohne Trennzeichen für Tausender (z.B. 123456).

```
LBA
0    8       304        336     352    368 ...            z
|    |       |          |       |      |
-----------------------------------------------------------
|Res. | FAT  | Root     | Cluster                         |
|Area | Area | Dir      | Area                            |
-----------------------------------------------------------
                        |       |      |
Cluster address         2       3      4 ....
```

LBA des letzten Sektors des Dateisystems berechnen
```
- Größe des Dateisystems in Sektoren: 606208
- z = 606208 - 1 = 606207
```

### 6_FAT_Timestamp_1

> Sie durchqueren gerade das Wurzelverzeichnis der FAT-Partition. Dabei kommt Ihnen ein suspekter Eintrag in die Hände, bei dem das Datum des Zeitstempels created mit dem Hexadezimalwert 0x3281 kodiert ist.

> Sie möchten der Sache auf den Grund gehen und bestimmen das genaue Datum in der Form TT.MM.JJJJ

created: `0x3281`

Das Datum ist in FAT als 16-Bit Wert kodiert.
```python
# ipython
[ins] In [18]: "{0:b}".format(0x3281)
Out[18]: '11001010000001'

# 2 bit padding required to be 16 bit
0011001010000001

Jahr (7 bit)  | Monat: (4 bit)  | Tag: (5 bit)
0011001       | 0100            | 00001

[ins] In [19]: int('0011001', 2)
Out[19]: 25

[ins] In [20]: int('0100', 2)
Out[20]: 4

[ins] In [21]: int('00001', 2)
Out[21]: 1

# Jahr = 1980 + Wert = 1980 + 25 = 2005
# TT.MM.JJJJ = 01.04.2005
```

**Flag**: `01.04.2005`

### 6_FAT_Timestamp_2 (15)

> Sie durchqueren gerade das Wurzelverzeichnis der FAT-Partition. Dabei kommt Ihnen ein suspekter Eintrag in die Hände, bei dem die Uhrzeit des Zeitstempels created mit dem Hexdump A0F653 (Offset 13 bis 15 des Basis-Verzeichniseintrags) kodiert ist.

> Sie möchten der Sache auf den Grund gehen und bestimmen die genaue Uhrzeit in der Form HH:MM:SS.MSE (wobei MSE für Millisekunden steht).

created: `A0F653`

Die Uhrzeit ist in FAT als 16-Bit Wert kodiert. Die Millisekunden als 8-Bit Wert.

```
                      Millisekunden 8-Bit | Uhrzeit HH:MM:SS 16-Bit
Hexdump (big endian): A0                  | F653
little endian:        0xA0                | 0x53F6
```

HH:MM:SS berechnen
```python
format(0x53F6, 'b').rjust(16, '0')
'0101001111110110'

# Stunden (5 bit) | Minuten: (6 bit)  | Sekunden: (5 bit) * 2
# 01010           | 011111            | 10110
# 10              | 31                | 22 * 2 = 44
```

MSE berechnen
```python
# Sekunden = Hexwert Millisekunden * 10ms / 1000
0xa0 * 10 / 1000
1.6 # Sekunden

# 10:31:22 + 1.6s = 10:31:45.600
```

**Flag**: `10:31:45.600`

## DOS Partitionsschema

### 4_Working_Copy_Hash (3)

> Sie erhalten das Datenträgerabbild image_ws.dd als Zip-Archiv.
> Berechnen Sie die SHA-256 Hashsumme Ihrer Workingcopy.

```bash
$ sha256sum image_ws.dd*
666915b67f959a0b114a36d8f7b25d41474d9a29c8c7e8a6df39088ecb400596  image_ws.dd
3193d97aa466a006aafb38bdef0b86824639ec3b23465970ac634afc5901c962  image_ws.dd.zip
```

Arbeitskopie erstellen
```bash
$ dd if=image_ws.dd of=image_wc.dd bs=4096
250000+0 records in
250000+0 records out
1024000000 bytes (1.0 GB, 977 MiB) copied, 0.765093 s, 1.3 GB/s
$ sha256sum image_wc.dd
666915b67f959a0b114a36d8f7b25d41474d9a29c8c7e8a6df39088ecb400596  image_wc.dd
```

**Flag**: `666915b67f959a0b114a36d8f7b25d41474d9a29c8c7e8a6df39088ecb400596`

### 4_Extract_Partition_1 (3)

> Nennen Sie den dd-Befehl zum Extrahieren der ersten primären Partition des Images image_ws.dd in die Datei partition1.dd .
> Hinweis: Die Blocksize entspricht bei dd standardmäßig 512 Byte und muss daher nicht explizit angegeben werden.

Partitionsschema des Abbildes auflisten
```bash
$ mmls image_ws.dd
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000309247   0000307200   DOS FAT16 (0x06)
003:  -------   0000309248   0000333823   0000024576   Unallocated
004:  Meta      0000331776   0001999999   0001668224   DOS Extended (0x05)
005:  Meta      0000331776   0000331776   0000000001   Extended Table (#1)
006:  001:000   0000333824   0000940031   0000606208   DOS FAT16 (0x06)
007:  -------   0000940032   0001999999   0001059968   Unallocated
```

1. Partition extrahieren mit `dd`

```bash
$ dd if=image_ws.dd of=partition1.dd skip=2048 count=307200
$ sha256sum partition1.dd
256f5f3c67be7a362fec3f6f5717328c30e2c1a8c0786c9a7006babde9f67c51  partition1.dd
```

1. Partition extrahieren mit `mmcat`

```bash
$ mmcat image_ws.dd 2 > partition1.dd.bak
```

### 4_Extract_Partition_2 (3)

> Nennen Sie den dd-Befehl zum Extrahieren der sekundären Dateisystempartition in die Datei partition2.dd. Verwenden Sie die folgende Reihenfolge der dd-Optionen: dd if=xxx of=yyy skip=zzz count=aaa
> Hinweise: Die Blockgröße entspricht bei dd standardmäßig 512 Byte und muss daher nicht explizit angegeben werden.

2. Partition (sekundäre Dateisystempartition) extrahieren

```bash
$ dd if=image_ws.dd of=partition2.dd skip=333824 count=606208
$ sha256sum partition2.dd
d21e344ef27b38c302dd926529bdf93b01b69ccb0437dc89dd3f1c53b900afc6  partition2.dd
```

### 4_Partition_Table_1 (3)

> Wieviele sekundäre Dateisystempartitionen finden Sie in der Partitionstabelle des Images image_ws.dd?

**Flag**: `1`

### 4_Partition_Table_3 (3)

> Ist die Angabe des Partitionstyps im Eintrag einer Partitionstabelle verlässlich?

> Antworten Sie mit "Ja" oder "Nein".

**Flag**: `Nein`

### 4_Partition_Table_4 (5)

> Ihnen ist bekannt, dass die Angabe des Partitionstyps nicht essenziell ist. Daher überprüfen Sie nochmal genauer um welches Dateisystem es sich bei der ersten primären Partition handelt.

> Nennen Sie das korrekte Dateisystem.

`mmls` verwendet den Partitionstyp im Partitionstabelleneintrag des MBR.  
Besser ist es den Startsektor der Partition mit `mmls` zu ermitteln und den Partitionstyp anhand des Bootsektors mit `fsstat` zu interpretieren.
```bash
$ fsstat -o 2048 image_ws.dd
FILE SYSTEM INFORMATION
--------------------------------------------
File System Type: FAT32

OEM Name: MSDOS5.0
Volume ID: 0x9c1ceb2bA
[REMOVED]
```

**Flag**: `FAT32`

### 4_Partition_Table_2 (7)

> Welche Größe (in Sektoren) hat der zweite nichtallozierte Bereich?

Die nicht-allozierte Partition fängt mit dem Beginn der ersten nicht-allozierten an, endet aber mit dem Start der erweiterten Dateisystempartition
```bash
[REMOVED]
003:  -------   0000309248   0000333823   0000024576   Unallocated
004:  Meta      0000331776   0001999999   0001668224   DOS Extended (0x05)
[REMOVED]

331776 - 309248 = 22528
```

**Flag**: `22528`

### 4_Extended_Partition_Table_1

> Finden Sie die logische Partition in der erweiterten Partitionstabelle im Image image_ws.dd.

> Geben Sie den entsprechenden Eintrag hexadezimal an (Form: FF FF FF ... FF).

Logische Partition = sekundäre Dateisystempartition.  
Ersten Partitionstabelleneintrag der erweiterten Partitionstabelle auslesen.  
Die erweiterte Partitionstabelle steht in LBA 331776. Ein Sektor ist 512 Byte.

```bash
$ dd if=image_ws.dd count=1 bs=1 skip=$((331776 * 512 + 446)) count=16 status=none | xxd -g 1
00000000: 00 c6 33 14 06 83 09 3a 00 08 00 00 00 40 09 00  ..3....:.....@..
```

**Flag**: `00 c6 33 14 06 83 09 3a 00 08 00 00 00 40 09 00`

### 6_FAT_File_Recovery_1 (5)

> Im Wurzelverzeichnis von partition2.dd stoßen Sie auf folgenden Eintrag:
> Ist die Datei gelöscht? Antworten Sie mit "Ja" oder "Nein".

```
00000240: e559 4e54 4845 7e31 5044 4620 0067 b875  .YNTHE~1PDF .g.u
00000250: 6f48 6f48 0000 326f 6543 8605 d509 0c00  oHoH..2oeC......
```

Eintrag startet mit `e5` = gelöschte Datei

**Flag**: `Ja`

### 6_FAT_Pointer_Position (5)

> Geben Sie das Offset des Zeigers an der FAT-Adresse 42 relativ zum Beginn der FAT in einem FAT32-Dateisystem an.

Jeder Eintrag der FAT in FAT32 ist 4 Byte groß.
```
Relatives Offset = 42 * 4 = 168
```

**Flag**: `168`

### 6_Root_Directory_1 (5)

> Betrachten Sie den Bootsektor von partition1.dd.
> Ermitteln Sie die Clusteradresse des ersten Clusters des Wurzelverzeichnisses.

Clusteradresse des ersten Clusters im Wurzelverzeichnis an Offset 44-47 im Bootsektor von partition1.dd auslesen
```
- Wert: 0200 0000 = 0x00000002 (2)
```
Das Wurzelverzeichnis in diesem Fall, wie bei FAT12/16, zusammen mit dem Datenbereich.

**Flag**: `2`

### 6_Root_Directory_2 (5) 

> Betrachten Sie das Wurzelverzeichnis von partition1.dd.
> Wurde der Verzeichniseintrag mit der Metadatenadresse 28 bereits genutzt? Falls ja, ist dieser aktuell alloziert oder gelöscht?
> Antworten Sie mit "ungenutzt", "alloziert" oder "gelöscht".

```bash
$ istat partition1.dd 28 | less
Directory Entry: 28
Allocated
File Attributes: File, Archive
Size: 1462448
Name: LAGEBE~1.PDF
```

**Flag**: `alloziert`

### 6_Root_Directory_4 (5)

> Betrachten Sie das Wurzelverzeichnis von partition1.dd.

> Bestimmen Sie die Dateigröße der Datei aus der Aufgabe 6_Root_Directory_2 in Bytes (Verzeichniseintrag mit der Metadatenadresse 28).

Lässt sich aus `istat` entnehmen
```bash
$ istat partition1.dd 28 | less
[REMOVED]
Size: 1462448
```

Lässt sich auch manuell berechnen. Verzeichniseintrag 28 aus Wurzelverzeichnis auslesen. Dateigrösse an Offset 28-31
```bash
$ icat fat32_partition.dd 2 | dd bs=32 skip=$((28-3)) count=1 status=none | xxd
00000000: 4c41 4745 4245 7e31 5044 4620 0074 8d79  LAGEBE~1PDF .t.y
00000010: 6f48 6f48 0000 9179 6f48 0500 b050 1600  oHoH...yoH...P..
```

```python
> 0x001650b0
1462448
```

**Flag**: `1462448`


Der Eintrag beinhaltet einen Long File Name (LFN) zu erkennen an `0x0f` an Offset 11. Die Einträge mit jeweils 13 Zeichen des Long File Name folgen über dem Basiseintrag.
```bash
$ dd if=partition1.dd skip=8192 count=2 | xxd -c32 | less
[REMOVED]
# Verzeichniseintrag n - 2 speichert die nächsten 13 Zeichen
00000360: e56e 0065 002e 006a 0070 000f 7dd0 6700 0000 ffff ffff ffff ffff 0000 ffff ffff  .n.e...j.p..}.g.................
# Verzeichniseintrag: n - 1 speichert die ersten 13 Zeichen
00000380: e54d 0065 0074 0068 0061 000f 00d0 6d00 7000 6800 6500 7400 6100 0000 6d00 6900  .M.e.t.h.a....m.p.h.e.t.a...m.i.
# Basiseintrag n
000003a0: e545 5448 414d 7e31 4a50 4720 00a1 fc79 7148 7148 0000 f36a 6a48 d802 049b 0000  .ETHAM~1JPG ...yqHqH...jjH......
```

Metadatenadresse berechnen
```
> Offset 0x3e0 / 32 Byte pro Eintag + 1
Metadatenadresse: 32
```

**Flag**: `32`

### 6_FAT_Pre1_Slackline (5)

> Bestimmen Sie die FAT-Größe der partition1.dd.
> Hinweis: Eingabe in Bytes.

Größe der FAT in Bytes berechnen
```
- Anzahl Sektoren pro FAT @ Offset 36-39 bei FAT32: 0x0249 (585)
- Sektorgröße: 512
- Größe der FAT in Bytes = 585 * 512 = 299520
```

**Flag**: `299520`

### 6_FAT_Pre2_Slackline (3)

> Bestimmen Sie die Anzahl an FATs für partition1.dd.
> Achtung: Max. 1 Versuch!

Es gibt für gewöhnlich 2 FATs
```bash
$ fsstat partition1.dd | grep "* FAT"
* FAT 0: 7022 - 7606
* FAT 1: 7607 - 8191
```

**Flag**: `2`

### 6_Root_Directory_3 (7)

> Betrachten Sie das Wurzelverzeichnis von partition1.dd.
> Bestimmen Sie die Clusteradresse des ersten Clusters der Datei aus der Aufgabe 6_Root_Directory_2 (Verzeichniseintrag mit der Metadatenadresse 28).

Erste Clusteradresse einer Datei bestimmen. Hierzu den LBA des ersten Sektors den `istat` liefert in eine Clusteradresse umrechnen
```bash
- Clusteradresse = (LBA erster Sektor - Sektor der 2. Clusteradresse) / (Größe Cluster in Sektoren / Sektorgröße) + 2
- (8204 - 8192) / (2048 / 512) + 2 = 5
```

**Flag**: `5`

### 6_FSINFO_Sector_1 (10)

> Betrachten Sie den FSINFO-Sektor von partition1.dd. Bestimmen Sie die Anzahl nicht-allozierter Cluster.

FSINFO Datenstruktur in LBA 2 auslesen. Anzahl nicht-allozierter Cluster an Offset 488-491
```bash
00000000: 5252 6141 0000 0000 0000 0000 0000 0000  RRaA............
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
*
000001e0: 0000 0000 7272 4161 e514 0100 d802 0000  ....rrAa........
000001f0: 0000 0000 0000 0000 0000 0000 0000 55aa  ..............U.
```

```python
> 0x000114e5
70885
```

**Flag**: `70885`

### 6_Verify_File_Allocation_1 (10)

> Bestimmen Sie für partition1.dd, welche Sektoren von Cluster 3567 belegt werden. Antworten Sie bitte in der Form: x-y (wobei x = erster Sektor, y = letzter Sektor).

> Hint: Die Umrechnung von Cluster in Sektoren erfolgt gemäß der Formel: SClk = (Clk - 2) * n + SCl2
> d.h. (gegebener Cluster k minus 2) multipliziert mit Anzahl n (Sektoren pro Cluster) plus Sektoradresse von Cluster 2.

Sektoren eines Clusters berechnen
```
(3567 - 2) * (2048 / 512) + 8192 = 22452
- Start: 22452
- Ende: 22452 + 3 weitere Sektoren = 22455 
```

### 6_Verify_File_Allocation_3

> Nennen Sie den Dateinamen der Datei, die den Cluster 3567 alloziert.

```bash
$ istat partition1.dd 50
```

**Flag**: `WEBKUR~1.PDF`

### 6_FSINFO_Sector_2 (7)

> Betrachten Sie den FSINFO-Sektor von partition1.dd. Bestimmen Sie die Clusteradresse des ersten nicht-allozierten Clusters.

Wert aus FSINFO Struktur an LBA 2 auslesen
```bash
- Wert an Offset 492-495: 0x000002d8 (728)
```

**Flag**: `728`

### 6_Verify_File_Allocation_2

> Welche Metadatenadresse (Inode) hat die gesuchte Datei in Cluster 3567 (vgl. Aufgabe 6_Verify_File_Allocation_1)?

**Flag**: `50`

### 6_FAT_Entries_1 (10)
> Betrachten Sie die File Allocation Table von partition2.dd. Ist Cluster 16 der erste Cluster der Cluster Chain oder nicht?
> Antworten Sie mit "Ja" oder "Nein".

> Hint: Verwenden Sie das Tool blkcat um innerhalb des Images zum ersten Sektor der FAT zu springen.

Eintrag 16 in FAT auslesen
```bash
$ dd if=partition2.dd skip=8 | dd bs=2 skip=16 count=1 status=none | xxd -c2

00000000: 1100  ..
```

Mit `blkcat` den 8ten Sektor des FAT16 Dateisystems ausgeben lassen.  
`1100` ist der zweite Eintrag.
```bash
 blkcat partition2.dd 8 | xxd
00000000: f8ff ffff 0300 0400 0500 0600 0700 0800  ................
00000010: 0900 0a00 0b00 0c00 0d00 0e00 0f00 1000  ................
00000020: 1100 1200 1300 1400 1500 1600 1700 1800  ................
00000030: 1900 1a00 1b00 1c00 1d00 1e00 1f00 ffff  ................
```

Inode mit Start-Clusteradresse `1000` finden

---

```
$ icat partition1.dd 2 | dd bs=32 skip=$((32-3)) count=1 status=none | xxd
00000000: e545 5448 414d 7e31 4a50 4720 00a1 fc79  .ETHAM~1JPG ...y
00000010: 7148 7148 0000 f36a 6a48 d802 049b 0000  qHqH...jjH......

# Niederwertige Bytes der Clusteradresse 0x02d8 (728)
# Wie Clusteradressen adressieren bzw. sonst umrechnen

000002d8: b700 0000  ....
```

### 6_FAT_Entries_2 (10)

> Betrachten Sie die File Allocation Table von partition2.dd. Welchen Wert hat der Zeiger von Cluster 31?
> Antworten Sie in der Form 0xABCD.

FAT16, Cluster-Zeiger sind daher 16-Bit. Wert des 31. Eintrag der FAT auslesen
```bash
# * FAT 0: 8 - 155
dd if=partition2.dd skip=8 | dd bs=2 skip=31 count=1 status=none | xxd -c2
00000000: ffff  ..
```

**Flag**: `0xFFFF`

### 6_FAT_Entries_3

> Sie wissen nun, dass die zugehörige Cluster Chain bei Cluster 31 endet (vgl. Aufgabe 6_FAT_Entries_2).

> Wieviele Sektoren umfasst die Cluster Chain insgesamt?

Die Cluster-Chain lautet: `2-3-..-30-31`. Die Kette umfasst 30 Cluster. Ein Cluster umfasst 8192 / 512 = 16 Sektoren.  
Anzahl umfasster Sektoren = 30 * 16 = 480
```bash
$ xxd -c2 -a fat0-part2.dd| nl | less
# ignorieren
 1  00000000: f8ff  ..
# ignorieren
 2  00000002: ffff  ..
# 2. Eintrag verweist auf Cluster 3
 3  00000004: 0300  ..
 4  00000006: 0400  ..
 5  00000008: 0500  ..
 6  0000000a: 0600  ..
 7  0000000c: 0700  ..
 8  0000000e: 0800  ..
 9  00000010: 0900  ..
10  00000012: 0a00  ..
11  00000014: 0b00  ..
12  00000016: 0c00  ..
13  00000018: 0d00  ..
14  0000001a: 0e00  ..
15  0000001c: 0f00  ..
16  0000001e: 1000  ..
17  00000020: 1100  ..
18  00000022: 1200  ..
19  00000024: 1300  ..
20  00000026: 1400  ..
21  00000028: 1500  ..
22  0000002a: 1600  ..
23  0000002c: 1700  ..
24  0000002e: 1800  ..
25  00000030: 1900  ..
26  00000032: 1a00  ..
27  00000034: 1b00  ..
28  00000036: 1c00  ..
29  00000038: 1d00  ..
30  0000003a: 1e00  ..
31  0000003c: 1f00  ..
# Cluster 31 mit EOF-Label gehört noch zur Cluster-Chain!
32  0000003e: ffff  ..
```

Es ist die erste Cluster-Chain in `fsstat`.
```bash
$ fsstat partition2.dd
[REMOVED]
FAT CONTENTS (in sectors)
--------------------------------------------
336-815 (480) -> EOF
```

**Flag**: `480`

### 6_FAT_File_Recovery2_2 (10)

> Stellen Sie die gelöschte Datei "Methamphetamine.jpg" wieder her. Benennen Sie deren SHA-256 Hashsumme.

Die Metadatenadresse lautet 32. `istat` zeigt die betroffenen Sektoren an, welche von den allozierten Clustern der Datei umfasst werden.
```bash
$ istat partition1.dd 32
Directory Entry: 32
Not Allocated
File Attributes: File, Archive
Size: 39684
Name: _ETHAM~1.JPG
[REMOVED]
Sectors:
11096 11097 11098 11099 11100 11101 11102 11103
11104 11105 11106 11107 11108 11109 11110 11111
[REMOVED]
```

Sektoren aneinanderfügen und Bild wiederherstellen
```bash
$ icat partition1.dd 32 > recovered_image.jpg
$ sha256sum recovered_image.jpg
34fbe8499bb18a5ad96ea30fcba588d59c5f42cc4cd2b454bc21672aa38ad4a4  recovered_image.jpg
```

**Flag**: `34fbe8499bb18a5ad96ea30fcba588d59c5f42cc4cd2b454bc21672aa38ad4a4`

### 6_Root_Directory_5 (15)

> Betrachten Sie das Wurzelverzeichnis von partition1.dd.

> Aus wie vielen weiteren Datencluster besteht die Datei aus der Aufgabe 6_Root_Directory_2 (Verzeichniseintrag mit der Metadatenadresse 28)?

Datei liegt im Root-Verzeichnis (Metadatenadresse 2). Ihre Verzeichniseinträge ausgeben. Startclusteradresse der Date mit Metadatenadresse 28 ist 5
```bash
$ icat partition1.dd 2 | xxd -c32
00000320: 4c41 4745 4245 7e31 5044 4620 0074 8d79 6f48 6f48 0000 9179 6f48 0500 b050 1600  LAGEBE~1PDF .t.yoHoH...yoH...P..
```

Die Cluster-Chain der Datei lautet `5-6-...-718-719`
```bash
$ xxd -c4 fat0.dd | nl -v0
[REMOVED]
5  00000014: 0600 0000  ....
6  00000018: 0700 0000  ....
[REMOVED]
718  00000b38: cf02 0000  ....
719  00000b3c: ffff ff0f  ....
[REMOVED]
```

Die allozierten Cluster lauten 5-719. Diese liegen innerhalb der Sektoren 8204-11063.
```bash
$ python3 cluster2sectors.py 5 4 8192
Cluster 5 includes sectors 8204-8207
$ python3 cluster2sectors.py 719 4 8192
Cluster 719 includes sectors 11060-11063
```

Das stimmt mit der Angabe aus `fsstat` überein. Die Datei besteht auf `719-5+1 = 715` Clustern.
```bash
$ fsstat partition1.dd
FAT CONTENTS (in sectors)
--------------------------------------------
[REMOVED]
8204-11063 (2860) -> EOF
[REMOVED]
# (11063-8204 + 1) / 4 Sektoren pro Cluster = 715
```

**Flag**: `715`

### 6_FAT_File_Recovery_2 (15)

> Im Wurzelverzeichnis von partition2.dd stoßen Sie auf folgenden Eintrag:

```
00000240: e559 4e54 4845 7e31 5044 4620 0067 b875  .YNTHE~1PDF .g.u
00000250: 6f48 6f48 0000 326f 6543 8605 d509 0c00  oHoH..2oeC......
```

> Stellen Sie die entsprechende Datei mittels blkcat wieder her und speichern Sie sie als "recovered_file" ab.

> Nennen Sie den zugehörigen blkcat Befehl in der Form: blkcat partition2.dd x y > recovered_file

Es handelt sich um eine gelöschte Datei mit einem Long File Name
```bash
$ dd if=partition2.dd skip=304 count=$((335-304+1)) | xxd -c32 
[REMOVED]
00000180: e542 0065 0068 0061 0076 000f 0079 6900 6f00 7200 7300 2e00 7000 0000 6400 6600  .B.e.h.a.v...yi.o.r.s...p...d.f.
000001a0: e56d 0020 0053 0075 0073 000f 0079 7000 6900 6300 6900 6f00 7500 0000 7300 2000  .m. .S.u.s...yp.i.c.i.o.u...s. .
000001c0: e566 0069 0063 0061 0074 000f 0079 6900 6f00 6e00 7300 2000 6600 0000 7200 6f00  .f.i.c.a.t...yi.o.n.s. .f...r.o.
000001e0: e54d 0061 006c 0077 0061 000f 0079 7200 6500 2000 5300 7000 6500 0000 6300 6900  .M.a.l.w.a...yr.e. .S.p.e...c.i.
00000200: e54e 0065 0061 0072 002d 000f 0079 4f00 7000 7400 6900 6d00 6100 0000 6c00 2000  .N.e.a.r.-...yO.p.t.i.m.a...l. .
00000220: e553 0079 006e 0074 0068 000f 0079 6500 7300 6900 7a00 6900 6e00 0000 6700 2000  .S.y.n.t.h...ye.s.i.z.i.n...g. .
00000240: e559 4e54 4845 7e31 5044 4620 0067 b875 6f48 6f48 0000 326f 6543 8605 d509 0c00  .YNTHE~1PDF .g.uoHoH..2oeC......
[REMOVED]
```

Anhand des LNF lässt sich die Datei mit `fls` finden (Metadatenadresse 21)
```bash
$ fls -r partition2.dd
r/r 10: Outside the Closed World_ On Using Machine Learning for Network Intrusion Detection.pdf
r/r 14: studie_voipsec-bso-2005.pdf
r/r * 21:       Synthesizing Near-Optimal Malware Specifications from Suspicious Behaviors.pdf
```
```bash
$ istat partition2.dd 21
[REMOVED]
Size: 788949
Name: _YNTHE~1.PDF
[REMOVED]
Sectors:
22928 22929 22930 22931 22932 22933 22934 22935
22936 22937 22938 22939 22940 22941 22942 22943
```

Die angegebene Größe stimmt nicht mit der Anzahl der Sektoren überein. Für 788949 Byte müssten es `ceil(788949 / 512) = 1541` Sektoren sein
```bash
$ blkcat partition2.dd 22928 1541 > recovered_file
$ sha256sum recovered_file
b3e427ce6229947c96cba95046a7166f3c59f8bbb3a9a23594adc8ff8a2eefd6  recovered_file
```

**Flag**: `blkcat partition2.dd 22928 1541 > recovered_file`

### 6_FAT_Flag_Slackline (40)

> Finden Sie das versteckte Token. Achten Sie auf Bereiche welche normalerweise nicht vom Dateisystem verwendet werden (Slack).

> Hinweis: Alle Flags sind in der FAT32-Partition versteckt. Token in der Form flag{ABC}. Tokens können verschleiert sein.

FAT-Slack: Bereich zwischen letztem FAT-Eintrag und nächstem Datenbereich. Nächste FAT-Tabelle oder Datenbereich.

FAT0 extrahieren
```bash
# * FAT 0: 7022 - 7606
$ dd if=partition1.dd of=fat0.dd skip=7022 count=$((7606+1-7022))
$ sha256sum fat0.dd
c2191c67a5b32cc5f68e3d22aacf19e048092d1a8671d9fc78506699c47f4120  fat0.dd
```

Die letzte allozierte Cluster-Chain ist: `18056-23863 (5808) -> EOF`. Sektor `23863` liegt in Cluster 3919
```bash
$ python3 sector2cluster.py 23863 8192 4
Sector 23863 is in cluster 3919
```

Die restlichen FAT-Eintrage 3920-74879 werden nicht benutzt
```bash
[REMOVED]
 3918  00003d38: 4f0f 0000  O...
 3919  00003d3c: ffff ff0f  ....
 3920  00003d40: 0000 0000  ....
 3921  00003d44: 0000 0000  ....
[REMOVED]
74879  000491fc: 3000 3d00  0.=.
```

Damit lässt sich der FAT-Slack extrahieren
```bash
$ dd if=fat0.dd of=fat0.slack.dd bs=4 skip=$((3920)) count=$((74879+1-3920))
```

Am Ende des FAT-Slack finden sich ASCII Zeichen mit einer offensichtlichen Zeichenbreite von 16-bit
```bash
$ strings -e l fat0.slack.dd
ZmxhZ3tGQVRzbEFjS30=
$ echo -n 'ZmxhZ3tGQVRzbEFjS30=' | base64 -d
flag{FATslAcK}
```

**Flag**: `flag{FATslAcK}`

### 6_FAT_Flag_Looking_For_a_Name (40)

> Finden Sie das versteckte Token.

> Hinweis: Alle Flags sind in der FAT32-Partition versteckt. Token in der Form flag{ABC}. Tokens können verschleiert sein.

Nach Flag suchen. Das Offset `0x400301` zeigt in Sektor `ceil(0x400301 / 512) = 8194` und somit in das Wurzelverzeichnis.
```bash
# *** Root Directory: 8192 - 8195
$ strings -t x partition1.dd | grep flag
 400301 flag{Se
```

Wurzelverzeichnis extrahieren und ausgeben
```bash
$ dd if=partition1.dd of=partition1.rootdir.dd skip=8192 count=$((8195+1-8192))
$ sha256sum partition1.rootdir.dd
9c825c3163bfa395a6c7c4cb0f2c5074e4c3acae3bace4911b8525e11894a44b  partition1.rootdir.dd

```

Es existiert ein Eintrag mit einem Long File Name.  
Metadatenadresse `27` hat die die Sequenznummer 1.  
Metadatenadresse `26` hat die letzte Sequenznummer. Sie wird mit der Konstanten `0x40` exklusiv ODER vernknüpft `0x42 ^ 0x40 = 2`.
```bash
$ xxd -c32 partition1.rootdir.dd | nl -v3 | less
[REMOVED]
26  000002e0: 4231 0035 002e 0070 0064 000f 00fa 6600 0000 ffff ffff ffff ffff 0000 ffff ffff  B1.5...p.d....f.................
27  00000300: 0166 6c61 677b 5365 0062 000f 00fa 6500 7200 6900 6300 6800 7400 0000 3200 3000  .flag{Se.b....e.r.i.c.h.t...2.0.
28  00000320: 4c41 4745 4245 7e31 5044 4620 0074 8d79 6f48 6f48 0000 9179 6f48 0500 b050 1600  LAGEBE~1PDF .t.yoHoH...yoH...P..
[REMOVED]
```

Zeichen die nicht zum Dateinamen gehören entfernen und UTF-16 Zeichenkette ausgeben
```
27  00000300: 01 66 6c 61 67 7b 53 65 00 62 00 0f 00 fa 65 00 72 00 69 00 63 00 68 00 74 00 00 00 32 00 30 00  .flag{Se.b....e.r.i.c.h.t...2.0.
27  00000300:                      65 00 62 00          65 00 72 00 69 00 63 00 68 00 74 00       32 00 30 00  .flag{Se.b....e.r.i.c.h.t...2.0.

26  000002e0: 42 31 00 35 00 2e 00 70 00 64 00 0f 00 fa 66 00 00 00 ff ff ff ff ff ff ff ff 00 00 ff ff ff ff  B1.5...p.d....f.................
26  000002e0:    31 00 35 00 2e 00 70 00 64 00          66 00                                                  B1.5...p.d....f.................
```
```bash
$ echo '6500620065007200690063006800740032003000310035002e00700064006600' | xxd -r -p
ebericht2015.pdf
```

## NTFS-Dateisystem

### 7_NTFS_Bootsector_0 (3)

> Mit welcher Metadatenadresse können Sie in einem NTFS-Dateisystem auf den Bootsektor zugreifen?

**Flag**: `7`

### 7_NTFS_Bootsector_1 (3)

> Sie erhalten den Hexdump des Bootsektors eines NTFS-formatierten Datenträgers. Bestimmen Sie die Adresse des ersten Clusters der MFT als Dezimalzahl (Eingabe ohne Trennzeichen für Tausender, Millionen, also beispielsweise 1234567).

```text
$ icat image-ntfs.dd 7 | xxd
0000000: eb52 904e 5446 5320 2020 2000 0208 0000 .R.NTFS .....
0000010: 0000 0000 00f8 0000 3f00 ff00 0008 0000 ........?.......
0000020: 0000 0000 8000 8000 ff1f 0300 0000 0000 ................
0000030: 5521 0000 0000 0000 0200 0000 0000 0000 U!..............
0000040: f600 0000 0100 0000 b2f4 d5cc 2cd6 cce8 ............,...
0000050: 0000 0000 fa33 c08e d0bc 007c fb68 c007 .....3.....|.h..
0000060: 1f1e 6866 00cb 8816 0e00 6681 3e03 004e ..hf......f.>..N
0000070: 5446 5375 15b4 41bb aa55 cd13 720c 81fb TFSu..A..U..r...
0000080: 55aa 7506 f7c1 0100 7503 e9dd 001e 83ec U.u.....u.......
0000090: 1868 1a00 b448 8a16 0e00 8bf4 161f cd13 .h...H..........
00000a0: 9f83 c418 9e58 1f72 e13b 060b 0075 dba3 .....X.r.;...u..
[REMOVED]
```

Die Clusteradresse ist der 8 Byte Wert ab Offset 0x30.

**Flag:** `8533`

### 7_NTFS_Timestamp_1 (3)

> In NTFS werden Zeitstempel an verschiedenen Stellen gespeichert.  
> Welches NTFS-Attribut enthält die relevanten Zeitstempel?

**Flag:** `$STANDARD_INFORMATION`

### 7_NTFS_Fixup_Array_1 (3)

> Wie viele Einträge hat das Fixup Array aus dem $DATA Attribut des ersten Eintrages in der MFT?

```text
0000000: 4649 4c45 3000 0300 4ba7 6401 0000 0000
0000010: 0100 0100 3800 0100 b801 0000 0004 0000
0000020: 0000 0000 0000 0000 0600 0000 0000 0000
0000030: 5800 0000 0000 0000 1000 0000 6000 0000
[REMOVED]
```

Die Anzahl der Fixup-Einträge ist an Offset `0x06 - 0x07`.

**Flag:** `3`

### 7_NTFS_FS_Files_1 (3)

> Mittels welcher Datei im NTFS Dateisystem können Sie herausfinden, ob ein Cluster alloziert ist?

**Flag:** `$Bitmap`

### 7_NTFS_FS_Files_2 (3)

> Welche Datei im NTFS Dateisystem enthält Informationen zu Clustern mit beschädigten Sektoren?

**Flag:** `$BadClus`

### 7_NTFS_Index_Records_1 (3)

> Wie viele Kindknoten kann ein NTFS B-tree Knoten maximal besitzen?
> a) 1 
> b) 2  
> c) mehr als 2  
> d) keine  

Es sind 4 Kindknoten.

**Flag:** `c`

### 7_NTFS_Bootsector_3 (5)

> Sie erhalten den Hexdump des Bootsektors eines NTFS-formatierten Datenträgers. Bestimmen Sie die Größe eines Index-Records als Dezimalzahl in Byte (Eingabe ohne Trennzeichen für Tausender, Millionen, also beispielsweise 1234567).

```bash
$ icat image-ntfs.dd 7 | xxd
0000000: eb52 904e 5446 5320 2020 2000 0208 0000 .R.NTFS .....
0000010: 0000 0000 00f8 0000 3f00 ff00 0008 0000 ........?.......
0000020: 0000 0000 8000 8000 ff1f 0300 0000 0000 ................
0000030: 5521 0000 0000 0000 0200 0000 0000 0000 U!..............
0000040: f600 0000 0100 0000 b2f4 d5cc 2cd6 cce8 ............,...
0000050: 0000 0000 fa33 c08e d0bc 007c fb68 c007 .....3.....|.h..
0000060: 1f1e 6866 00cb 8816 0e00 6681 3e03 004e ..hf......f.>..N
0000070: 5446 5375 15b4 41bb aa55 cd13 720c 81fb TFSu..A..U..r...
0000080: 55aa 7506 f7c1 0100 7503 e9dd 001e 83ec U.u.....u.......
0000090: 1868 1a00 b448 8a16 0e00 8bf4 161f cd13 .h...H..........
00000a0: 9f83 c418 9e58 1f72 e13b 060b 0075 dba3 .....X.r.;...u..
[REMOVED]
```

Die Größe steht an Offset `0x44`: `0x01`. Die Einheit ist Cluster.  
Die Größe eines Clusters in Sektoren steht an Offset `0x0d`: `0x08`  
Ein Sektor ist 512 Byte.
```text
1 * 8 * 512 =  4096
```

**Flag:** `4096`

### 7_NTFS_Fixup_Array_2 (5)

> Der Fixup Array eines MFT Eintrags sei ABCD EF00 0102.
> Welchen Bytestring finden Sie an Offset 1022 bis 1023 dieses MFT-Eintrags?

**Flag:** `ABCD`

### 7_NTFS_File_Address_1 (5)

> Bestimmen Sie für ein NTFS-Dateisystem Ihrer Wahl die Dateiadressen der ersten vier MFT-Einträge.
> Wie häufig unterscheidet sich hierbei die Sequenznummer von der Metadatenadresse?

Sie unterscheidet sich nur für den ersten Eintrag mit Metadatenadresse `0`. Dort ist sie `1`.

```bash
$ dd if=ntfs1.dd count=$((2 * 4)) skip=$((8533 * 8)) | xxd
00000400: 4649 4c45 3000 0300 3023 1000 0000 0000  FILE0...0#......
00000410: 0100 0100 3800 0100 5801 0000 0004 0000  ....8...X.......

$ istat ntfs1.dd 0
MFT Entry Header Values:
Entry: 0        Sequence: 1
```

**Flag:** `1`

### 7_NTFS_Flag_Values_3 (5)

> Welche Informationen erhalten Sie über einen Index-Eintrag, wenn Sie in dessen Flag-Feld (also Offset 12 bis 15) den Wert 0x03 finden?
> a) Eintrag verweist auf Kindknoten
> b) Letzter Index-Eintrag in diesem Index-Record
> c) Letzter Eintrag und Verweis auf Kindknoten

**Flag:** `c`

### 7_NTFS_Cluster_Runlist_1 (5)

> Wir betrachten das Default-$DATA-Attribut der Datei hidden.txt . Wie viele Cluster belegen die Inhaltsdaten?

```text
0000000: 8000 0000 6000 0000 0100 4000 0000 0100 ....`.....@.....
0000016: 0000 0000 0000 0000 ef20 0000 0000 0000 ......... ...... 
0000032: 4000 0000 0000 0000 00c0 8300 0000 0000 @............... 
0000048: 00c0 8300 0000 0000 00c0 8300 0000 0000 ................ 
0000064: 32c0 1eb5 3a05 2170 1b1f 2290 015f 7e31 2...:.!p..".._~1 
```
0000080: 2076 ed00 2110 8700 00b0 6e82 4844 7e82 v..!.....n.HD~.
