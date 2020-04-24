# gebruik: perl logbookHourCounter.pl bestandsnaam1.csv bestandsnaam2.csv bestandsnaamX.csv "bestandsnaam met spaties.csv"
# aantal bestandsnamen is vrij te kiezen
foreach $filename (@ARGV) {
	$total_minutes = 0;
	open(my $in, "<", $filename);
	while(<$in>) {
		if($_ =~ /(\d+):(\d+),(\d+):(\d+)/) {
			$total_minutes += ($3*60+$4)-($1*60+$2);
		}
	}
	print($filename, ": ", int($total_minutes/60)," uren en ",$total_minutes%60," minuten gewerkt\n");
}
