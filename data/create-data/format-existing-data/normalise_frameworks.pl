#!/usr/bin/perl

open(IN, "frameworks_in.json");


my $line="";
my %parameters;

while ($line = <IN>) {
  chomp($line);
  if(index($line,"{") < 0) {
    $line =~ s/"//g;
    $line =~ s/,//g;
    if(index($line,":") >= 0 ) {
      @fields = split(':',$line);
      
      $parameter = $fields[0];
      $parameter =~ s/[ |\t]+//g;
      
      if(index($parameter,"ASH") >=0) {
        print "************".$line;
      }
      
      if(! exists $parameters{$parameter}) {
        print "\t  new key ".$parameter."\n";
        $parameters{$parameter} = "1";
      }
    }
    #print "\t===============".$line."\n";

  } else {
    
    print "new framework \n";  
  }
}

close(IN);

my $key="";

# Provide key words you want removed from list. The list gets converted to hash for later use
print "\n\n*******Remove unwanted keys: \n";
my @myRemovedKeyWords = ("");
my %unWantedParameters = map { $_ => 1 } @myRemovedKeyWords;
foreach $key (keys %parameters) {
  if(exists($unWantedParameters{$key})) {
    print "Remove key: ".$key."\n";
    delete $parameters{$key};
  }
}


# Comment out to insert new key words in the hash
print "\n\n*******Insert new keys: \n";
my @myNewKeyWords = ("twitter");
foreach (@myNewKeyWords) {
  print "new keys: " . $_ . " \n";
  $parameters{$_} = "1";
}

# Show sorted list of current keywords
print "\n\n*******Show sorted keys: \n";
foreach my $key (sort keys %parameters) {
    print "\"".$key."\",\n";
}

my %flags;
my $temp;

printf ("\n\n START ------------------- \n\n");

open(IN,"frameworks_in.json");
open(OUT,">frameworks_out.json");

my $FRAMEWORK;
my $OUTLINE;

# Start OUTLINE
$OUTLINE = "[\n";

while ($line = <IN>) {
  chomp($line);
  if(index($line,"{") >= 0) {
    # we're starting a new framework
    undef %flags;
    foreach $key (keys %parameters) {
      $flags{$key} = "UNDEF";
    }
    $FRAMEWORK="  {\n";
  } elsif(index($line,"}") >= 0) {
    foreach $key (keys %flags) {
      
      
      if(length($flags{$key}) == 0) {
        #print "  ".$key." -> EMPTY\n";
        $FRAMEWORK .= "  \"".$key."\":\"EMPTY\",\n";
      } else {
        #print "  ".$key." -> ".$flags{$key}."\n";

        $FRAMEWORK .= "  \"".$key."\":\"".$flags{$key}."\",\n";
      }
    }
    $FRAMEWORK = substr($FRAMEWORK, 0, -2);
    $FRAMEWORK .= "\n  },\n";
    $OUTLINE .= $FRAMEWORK;
  } else {
    if(index($line,":") >= 0 ) {
      # there is parameter defined
      $line =~ s/"//g;
      $line =~ s/,//g;
      @fields = split(':',$line,2); # Only split on first occurence
      $parameter = $fields[0];
      $parameter =~ s/[ |\t]+//g;
      
      if(exists($unWantedParameters{$parameter})) {
        print "Removed: " . $parameter . "\n";
      } else {
        #if(length($fields[1]) < 2) {
        #  $flags{$parameter} = "empty_string";
        #} else {
        $temp = $fields[1];
        $temp =~ s/^[ |\t]+//; #strip start space off
        $temp =~ s/[\s]*$//;  #strip end space off

        $flags{$parameter} = $temp;
        #}
      }
    }
  }
}

# Strip last ',' and add closing tag
$OUTLINE = substr($OUTLINE, 0, -2);
$OUTLINE .= "\n]";
print OUT $OUTLINE;

print "FINISHED";

#print $OUTLINE;

close(IN);
close(OUT);


