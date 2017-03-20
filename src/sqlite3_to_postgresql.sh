# patch the sqlite3 dump so it can be loaded by postgresql

echo drop table traffic\;
echo drop table wards\;
cat traffic.sql | grep -v PRAGMA | sed 's/\[//g' | sed 's/\]//g'
