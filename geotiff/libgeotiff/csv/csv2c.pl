#!/usr/bin/perl
if ($#ARGV < 0) { die "usage: csv2c table\n"; }
my $line = 0; my $cnt = 0;
my $table = $ARGV[0];
open(CSV, "cat ${table}.csv|");
open(COUT, "> ${table}.c");
print COUT "#include \"defs.h\"\n";
while(<CSV>) {
    $line++;
    chomp;
    
    print COUT "datafile_rows_t ${table}_row_${line}\[\] = {";
    print COUT $_;
    print COUT ",NULL};\n";
}
print COUT "datafile_rows_t *${table}_rows[] = {";
while ($cnt < $line) {
    $cnt++;
    print COUT "${table}_row_${cnt},";
}
print COUT "NULL};\n";
close(CSV);
close(COUT);
