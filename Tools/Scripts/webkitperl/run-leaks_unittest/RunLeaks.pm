#!/usr/bin/perl -w

# Copyright (C) 2011 Apple Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1.  Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Imports run-leaks into a package for easy unit testing.

package RunLeaks;

use strict;
use warnings;

use English;
use File::Spec;
use FindBin;
use lib File::Spec->catdir($FindBin::Bin, "..", "..");
use webkitdirs;

use base 'Exporter' ;
use vars qw( @EXPORT @EXPORT_OK %EXPORT_TAGS $VERSION ) ;

@EXPORT = ();
@EXPORT_OK = ();
%EXPORT_TAGS = ();
$VERSION = '1.0';

sub readFile($);

my $runLeaksPath = File::Spec->catfile(sourceDir(), "Tools", "Scripts", "run-leaks");
eval "sub {" . readFile($runLeaksPath) . "}";

sub readFile($) {
    local $INPUT_RECORD_SEPARATOR = undef; # Read in the whole file at once.
    open FILE, "<", shift || die $!;
    my $contents = <FILE>;
    close FILE || die $!;
    return $contents;
};

1;