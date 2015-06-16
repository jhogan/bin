#! /usr/bin/perl
use strict;
use Net::SMTP;
# Configuration
#----------------------------------------
my $DestRepos = "/root/reposBK";
my $DumpDir = "/root/reposDumps";
my $FromAddr = 'admin@xxxxxxxxxxx.com';
my $Site = 'xxxxxxxxxxxx.com';
my $SMTPHost = "smtp.west.cox.net";
my @ToAddr = qw/ jhogan@XXXXXXX.com/;
my $Subject = "Subversion backup failure";
#----------------------------------------

my $ToAddrs;
my $DestYoungest;
my $File;
my @Files;
my $FilePath;

eval{
	die;
	# Open dir of dump files
	opendir DH, $DumpDir;

	# Put dump files into @Files
	foreach $File (readdir DH){
		next unless $File =~ /^\d+\.dmp$/;
		push @Files, $File;
	}

	# **Numerically** sort files so we can apply
	# the revisions in the correct order
	@Files = sort { $a <=> $b } @Files;

	if (@Files > 0){

		# Get the backup repository's latest revision number
		$DestYoungest = `svnlook youngest $DestRepos`;

		$Files[0] =~ /^(\d+)\.dmp$/; 
		if ($1 != $DestYoungest + 1){
			die "Dump file senquencing error.\nDump file revision: $1\nBackup repos's youngest revision: $DestYoungest\n"
		}
		foreach $File (@Files){
			$FilePath = "$DumpDir/$File";
			`svnadmin load $DestRepos < $FilePath`;
			unlink $FilePath;
			print "$File\n";
		}
	}
};

my $ErrMsg = $@;
my $MailMsg = "An error occured in the Subversion incremental backup script:\n$ErrMsg";
if ($ErrMsg){
	foreach my $Addr (@ToAddr){$ToAddrs = $ToAddrs . "$Addr, ";}
	$ToAddrs =~ s/, $//;
	print $ErrMsg;
	my $smtp = Net::SMTP->new($SMTPHost); #, Hello => $Site);
	$smtp->mail($FromAddr); $smtp->to(@ToAddr); $smtp->data();
	$smtp->datasend("From: $FromAddr\n");
	$smtp->datasend("To: $ToAddrs\n");
	$smtp->datasend("Subject: $Subject\n");
	$smtp->datasend($MailMsg);
	$smtp->dataend(); $smtp->quit();
}

