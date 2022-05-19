#requires -PSEdition Core

# A script for performing a lot of auxiliary tasks for software development.
# This script does the following, in order:
#   - Installs packages required for the auxiliary tasks.
#   - Collect and build documentation using html Sphinx.
#   - Formats the python code according to the Black specification.
#   - Tests the code using pytest and provides code coverage using coverage.py.


###############################################################################

##### Installing needed packages.
Write-Output ""
Write-Output "=========================================="
Write-Output "===== Installing Auxiliary Packages ======"
Write-Output "=========================================="
Write-Output ""
# Making sure the needed packages are installed.
pip install --upgrade --force-reinstall --quiet --quiet `
black pytest coverage sphinx sphinx_rtd_theme 



##### Building the documentation.
Write-Output ""
Write-Output "=========================================="
Write-Output "===== Building Sphinx Documentation ======"
Write-Output "=========================================="
Write-Output ""
# Directories, stored as variables for shorter lines.
$src_ox = "./src/opihiexarata/"
$doc_dir = "./docs/"
$doc_src = $doc_dir + "source/"
$doc_bld = $doc_dir + "build/"
$doc_src_dscd = $doc_src + "code/"
$doc_bld_html = $doc_bld + "html/"
$doc_bld_dscd = $doc_bld_html + "code/"

# Rebuilding the docstring documentation files. Clearing the cache first 
# and building using Sphinx.
Remove-Item $doc_src_dscd -Recurse -Force
sphinx-apidoc -f -e -o $doc_src_dscd $src_ox

# Building the html documentation. We clear out the inital built just in case.
Remove-Item $doc_bld -Recurse -Force
sphinx-build -b html $doc_src $doc_bld_html


##### Formatting the code.
Write-Output ""
Write-Output "=========================================="
Write-Output "===== Formatting Code; black ============="
Write-Output "=========================================="
Write-Output ""
# Formatting of the code is done via Black. A first pass with future formatting
# allows for a smoother transition; but the formatting should still use the 
# default as the ultimate source.
black . --preview
black .


##### Testing the code.
Write-Output ""
Write-Output "=========================================="
Write-Output "===== Code Testing; pytest, coverage ====="
Write-Output "=========================================="
Write-Output ""
# Running pytest.
$pytest_cache_dir = "./.pytest/"
pytest . -o cache_dir=$pytest_cache_dir

# Running code coverage. We do not need another copy of pytest information 
# though, suppress it. (Watch out for the backtick linebreaks.)
$cov_result = $pytest_cache_dir + "coverage/results.bin"
coverage run --source=$src_ox --data-file=$cov_result -m pytest . `
--quiet --no-header --no-summary --show-capture="no" `
-p no:cacheprovider -o cache_dir=$pytest_cache_dir

# The result of the code coverage. We offload it to the documentation 
# directory because why not. The XML version is not really for human 
# consumption.
$cov_html_outdir = $doc_bld_dscd + ".coverage/"
$cov_xml_outfile = $pytest_cache_dir + "coverage/results.xml"
coverage html --data-file=$cov_result --directory=$cov_html_outdir
coverage xml -o $cov_xml_outfile --data-file=$cov_result --quiet
