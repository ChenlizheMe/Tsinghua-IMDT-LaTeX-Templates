$pdf_mode = 5;
$xelatex = 'internal imdt_xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';
$bibtex = 'bibtex %O %B';
$bibtex_use = 1;
$max_repeat = 5;
@default_files = ('imdt-proposal-report.tex', 'imdt-topic-work-plan.tex');

# Discard only the generated root .aux when its entry/mode changes. This
# also handles reference <-> writing mode on the same report entry.
sub imdt_xelatex {
    my @args = @_;
    my $source = $$Psource;
    $source =~ s{.*[/\\]}{};
    return system('xelatex', @args) unless
        $source =~ /^imdt-(?:proposal-report|topic-work-plan)\.tex$/;
    require File::Spec;
    my $aux = File::Spec->catfile($aux_dir || '.', "$$Pbase.aux");
    my $mode = 'form';
    if ($source eq 'imdt-proposal-report.tex') {
        open(my $options, '<', 'config/project-options.tex')
            or die 'Cannot read report mode';
        my $settings = do { local $/; <$options> };
        close($options);
        $mode = $settings =~ /^\s*\\IMDTReferenceReportfalse\b/m ? 'writing' : 'reference';
    }
    my $marker = "% imdt-main: $source; mode: $mode";
    if (-f $aux) {
        open(my $read, '<', $aux) or die "Cannot read generated auxiliary file: $aux";
        my $contents = do { local $/; <$read> };
        close($read);
        if (index($contents, $marker) < 0) {
            unlink($aux) or die "Cannot reset generated auxiliary file: $aux";
            print "IMDT: reset shared root auxiliary file for $source\n";
        }
    }
    my $status = system('xelatex', @args);
    if ($status == 0 && -f $aux) {
        open(my $write, '>>', $aux) or die "Cannot mark generated auxiliary file: $aux";
        print {$write} "\n$marker\n";
        close($write);
    }
    return $status;
}
