#!/bin/sh
user="lucas"
pass="lucas"
db="kayak"
mysql -u "$user" -p"$pass" "$db"  <<EOF >out.txt
  select * from solutions;
  select * from providers;


  SELECT 'ID','DATECREATION','DEPDATE','RETDATE','ORIGIN','DEST','CIE','SYSTEM1','FARES1','PRICE1','SYSTEM2','FARES2','PRICE2', 'IDSOLUTION','DIFFPRICE','MINPRICE','TOTALMIN','MAXPRICE','TOTALMAX'  UNION (select * into  outfile '/tmp/HA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from generalHA);
  SELECT 'ID','DATECREATION','DEPDATE','RETDATE','ORIGIN','DEST','CIE','SYSTEM1','FARES1','PRICE1','SYSTEM2','FARES2','PRICE2', 'IDSOLUTION','DIFFPRICE','MINPRICE','TOTALMIN','MAXPRICE','TOTALMAX'  UNION (select * into  outfile '/tmp/UA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from generalUA);
  SELECT 'ID','DATECREATION','DEPDATE','RETDATE','ORIGIN','DEST','CIE','SYSTEM1','FARES1','PRICE1','SYSTEM2','FARES2','PRICE2', 'IDSOLUTION','DIFFPRICE','MINPRICE','TOTALMIN','MAXPRICE','TOTALMAX'  UNION (select * into  outfile '/tmp/F9.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from generalF9);


  SELECT 'ORIGIN','DEST','BEST1A','BESTITA','NBFLIGHTS','PriceAvg_1A','PriceAvg_ITA','Percent_1A','Percent_ITA' UNION (select * into  outfile '/tmp/PERCENTF9.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from percentF9);
  SELECT 'ORIGIN','DEST','BEST1A','BESTITA','NBFLIGHTS','PriceAvg_1A','PriceAvg_ITA','Percent_1A','Percent_ITA' UNION (select * into  outfile '/tmp/PERCENTHA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from percentHA);
  SELECT 'ORIGIN','DEST','BEST1A','BESTITA','NBFLIGHTS','PriceAvg_1A','PriceAvg_ITA','Percent_1A','Percent_ITA' UNION (select * into  outfile '/tmp/PERCENTUA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from percentUA);


SELECT 'NAME','TOTALBC1A','NB1A','TOTALBCITA','NBITA' UNION (select * into  outfile '/tmp/BCSUMMARYHA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from badclickHASummary);
SELECT 'NAME','TOTALBC1A','NB1A','TOTALBCITA','NBITA' UNION (select * into  outfile '/tmp/BCSUMMARYUA.csv' fields terminated by ',' OPTIONALLY ENCLOSED BY '"' from badclickUASummary);
