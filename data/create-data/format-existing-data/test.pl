#!/usr/bin/perl

my $line = "   hellod world !  \n    ";

print ">".$line."<\n";

$line =~ s/[\s]*$//;
print ">".$line."<\n";


$line = "\"documentation_url\": \"https://github.com/senchalabs/jQTouch/wiki\"|\"https://github.com/senchalabs/jQTouch/wiki\",";
#$line = "\"documentation_url\": \"httpssdvsvsv\"";
$line =~ s/"//g;
$line =~ s/,//g;
@fields = split(':',$line, 2);


print ">".$line."<\n";
print $fields[0] . " " . $fields[1];
