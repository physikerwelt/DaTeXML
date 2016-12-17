#!/usr/bin/python2.7
import glob
import argparse
import subprocess


def process_folder(inp, out, together):
    fout = open(together, "w")
    for f in glob.glob(inp + "/*.tex"):
        print "processing file : " + f
        fdir = out + "/" + f + "/"
        dest = fdir + "xml.xml"
        subprocess.call(["latexml", "--includestyles", f, "--destination=" + dest])
        subprocess.call(
            ["latexmlpost", "--format", "xhtml", "--cmml", "--pmml", "--mathtex",
             "--destination=" + dest + ".xhtml",
             "--splitnaming=id", "--nocrossref",
             "--splitpath=//ltx:section | //ltx:subsection | //ltx:bibliography | //ltx:appendix | //ltx:index | //ltx:para",
             "--navigationtoc=none", "--dbfile=db.bd", "--nographicimages", "--nographicimages", dest])
        for p in glob.glob(fdir + "p*.xhtml"):
            fout.write("<ARXIVFILESPLIT Filename=\"" + p + "\">\n")
            with open(p) as infile:
                for line in infile:
                    fout.write(line)
            fout.write("\n</ARXIVFILESPLIT>")
    fout.close()


if __name__ == '__main__':  # When the script is self run
    parser = argparse.ArgumentParser(description='converts a folder with TeX files to NTCIR math XHTML format',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inp', help='The file with the TeX files',
                        default='.')
    parser.add_argument('--out', help='the directory name where the files go',
                        default='./XML')
    parser.add_argument('--together', help='the directory name where the arxivfilesplit file goes to',
                        default='./together.xml')
    args = parser.parse_args()
    process_folder(args.inp, args.out, args.together)
